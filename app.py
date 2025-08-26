from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import random
import pandas as pd
import os
import requests
import json
import logging

# STEP 1: ADDED NEW IMPORTS
import google.generativeai as genai
from dotenv import load_dotenv

# STEP 2: LOAD ENVIRONMENT VARIABLES FROM .env FILE
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key-change-in-production')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# STEP 3: REPLACED THE OLD FUNCTION WITH THE NEW GEMINI-POWERED FUNCTION
def chat_with_fitness_ai(message, context=""):
    """
    Handles conversation with the Gemini API to provide fitness advice.
    """
    # Get the API key you stored in the .env file
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        logger.error("Gemini API key is not configured in .env file.")
        return "Error: The AI Coach is not configured correctly. Please contact the administrator."
    
    try:
        # Configure the Gemini library with your key
        genai.configure(api_key=api_key)
        
        # Define the AI's persona and instructions
        system_prompt = (
            "You are FitAI, a professional, friendly, and encouraging AI fitness coach. "
            "Your expertise includes workout routines, nutrition, injury prevention, and motivation. "
            "Provide safe, clear, and actionable advice. If a question is outside the scope of "
            "fitness, health, or nutrition, you must politely state that you can only answer fitness-related questions. "
            "Keep your responses focused and easy to understand."
        )
        
        # Combine your instructions with the user's actual question
        full_prompt = f"{system_prompt}\n\nUser's question: {message}"
        
        # Call the Gemini model to get a response
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(full_prompt)
        
        # Send the AI's text response back to the user
        return response.text
    
    except Exception as e:
        # This will catch any errors if the API fails for some reason
        logger.error(f"An error occurred with the Gemini API: {e}")
        return "Sorry, I'm having a little trouble connecting to my brain right now. Please try again in a moment."

def get_fitness_context(user_data=None):
    """
    Generate context based on user's fitness data
    """
    if user_data:
        return f"User context: Weight: {user_data.get('weight', 'N/A')}kg, Height: {user_data.get('height', 'N/A')}cm, Goal: {user_data.get('goal', 'general fitness')}"
    return ""

def load_exercises():
    """Load exercises with error handling"""
    try:
        if not os.path.exists('exercises.csv'):
            logger.error("exercises.csv file not found")
            return pd.DataFrame()  # Return empty DataFrame
        
        df = pd.read_csv('exercises.csv')
        
        # Validate required columns
        required_columns = ['category', 'exercise_name', 'reps_min', 'reps_max']
        missing_columns = set(required_columns) - set(df.columns)
        
        if missing_columns:
            logger.error(f"Missing columns in exercises.csv: {missing_columns}")
            return pd.DataFrame()
        
        return df
    
    except Exception as e:
        logger.error(f"Error loading exercises.csv: {e}")
        return pd.DataFrame()

# Routine generator logic using the dataset
def output(intensity):
    df = load_exercises()  # Load dataset
    
    if df.empty:
        logger.warning("No exercises data available, returning default routine")
        return ["Push-ups - 10 reps", "Squats - 15 reps", "Plank - 30 seconds"]
    
    routine_list = []
    
    def add_exercises(category, max_intensity_ratio):
        max_intensity = intensity * max_intensity_ratio
        current_sum = 0
        category_exercises = df[df['category'] == category]  # Filter by category
        
        if category_exercises.empty:
            logger.warning(f"No exercises found for category: {category}")
            return
        
        for _, exercise in category_exercises.iterrows():
            current_sum += 1  # Each exercise counts as one in the total
            if max_intensity > current_sum:  # FIXED: Changed &gt; to >
                reps_min = exercise['reps_min']
                reps_max = exercise['reps_max']
                
                if pd.notnull(reps_min) and pd.notnull(reps_max):
                    reps = random.randint(int(reps_min), int(reps_max))
                    routine_list.append(f"{exercise['exercise_name']} - {reps} reps")
                else:
                    routine_list.append(f"{exercise['exercise_name']} - Duration-based")
            else:
                break
    
    # Add warmup, main exercises, and cooldown
    add_exercises('warmup', 0.2)
    add_exercises('exercise', 0.6)
    add_exercises('cooldown', 0.2)
    
    return routine_list if routine_list else ["No exercises available"]

# Function to calculate BMI and adjust intensity
def calculate_intensity(weight, height):
    if height <= 0 or weight <= 0:
        return 50  # Default intensity for invalid inputs
        
    height_in_meters = height / 100
    bmi = weight / (height_in_meters ** 2)
    
    if bmi < 18.5:
        return 50  # Low intensity for underweight
    elif 18.5 <= bmi < 24.9:
        return 70  # Moderate intensity for normal weight
    elif 25 <= bmi < 29.9:
        return 60  # Moderate intensity for overweight
    else:
        return 40  # Lower intensity for obesity

@app.route('/gen')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        
        if weight <= 0 or height <= 0:
            flash("Please enter valid weight and height values", "error")
            return render_template('index.html')
        
        intensity = calculate_intensity(weight, height)
        routine = output(intensity)
        return render_template('index.html', routine=routine)
    
    except ValueError:
        flash("Please enter numeric values for weight and height", "error")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error generating routine: {e}")
        flash("An error occurred while generating your routine", "error")
        return render_template('index.html')

@app.route("/")
def diet():
    return render_template("Home.html")

# Load diet data from CSV
def load_diet_data():
    """Load diet data with error handling"""
    try:
        if not os.path.exists('diet_data.csv'):
            logger.error("diet_data.csv file not found")
            return pd.DataFrame()
        
        df = pd.read_csv('diet_data.csv')
        
        # Validate required columns
        required_columns = ['diet_type', 'meal_type', 'food_item', 'calories']
        missing_columns = set(required_columns) - set(df.columns)
        
        if missing_columns:
            logger.error(f"Missing columns in diet_data.csv: {missing_columns}")
            return pd.DataFrame()
        
        # Clean data
        df['meal_type'] = df['meal_type'].str.strip()
        df['diet_type'] = df['diet_type'].str.strip()
        
        return df
    
    except Exception as e:
        logger.error(f"Error loading diet_data.csv: {e}")
        return pd.DataFrame()

class WeeklyDietPlan:
    def __init__(self, age, height, weight, goal, duration, diet_type, gender, activity_level, health_conditions=None):
        self.age = age
        self.height = height
        self.weight = weight
        self.goal = goal
        self.duration = duration
        self.diet_type = diet_type
        self.gender = gender
        self.activity_level = activity_level
        self.health_conditions = health_conditions or []
        self.bmr = self.calculate_bmr()
        self.daily_calories = self.adjust_calories()
        self.diet_data = load_diet_data()  # Load dataset here
        
        # Validate data before proceeding
        if self.diet_data.empty:
            raise ValueError("Diet data could not be loaded. Please check diet_data.csv file.")
        
        self.plan = self.create_diet_plan()
    
    def calculate_bmr(self):
        if self.gender == 'male':
            return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
    
    def adjust_calories(self):
        if self.goal == 'weight gain':
            return self.bmr + 500
        elif self.goal == 'weight loss':
            return self.bmr - 500
        else:
            return self.bmr  # Maintenance
    
    def create_diet_plan(self):
        # Adjust diet based on health conditions
        adjusted_diet_type = self.adjust_diet_for_health_conditions()
        
        if self.diet_type == 'weight gain':
            return {f'Day {i+1}': self.get_meal_plan(i+1, 'weight_gain', adjusted_diet_type) for i in range(7)}
        elif self.diet_type == 'weight loss':
            return {f'Day {i+1}': self.get_meal_plan(i+1, 'weight_loss', adjusted_diet_type) for i in range(7)}
        else:
            return {f'Day {i+1}': self.get_meal_plan(i+1, 'maintenance', adjusted_diet_type) for i in range(7)}
    
    def adjust_diet_for_health_conditions(self):
        """Adjust diet recommendations based on health conditions"""
        if not self.health_conditions:
            return self.diet_type
        
        # Health condition specific adjustments
        if 'Diabetes' in self.health_conditions:
            return 'diabetic_friendly'
        elif 'High Blood Pressure' in self.health_conditions:
            return 'low_sodium'
        elif 'Heart Disease' in self.health_conditions:
            return 'heart_healthy'
        elif 'High Cholesterol' in self.health_conditions:
            return 'low_cholesterol'
        else:
            return self.diet_type
    
    def get_meal_plan(self, day, diet_type, adjusted_diet_type):
        # Filter the dataset by diet_type
        meals = self.diet_data[self.diet_data['diet_type'] == diet_type]
        
        # FIXED: Add validation for empty meals dataset
        if meals.empty:
            logger.warning(f"No meals found for diet type: {diet_type}")
            # Try with original diet_type if adjusted_diet_type failed
            if adjusted_diet_type != diet_type:
                meals = self.diet_data[self.diet_data['diet_type'] == self.diet_type]
            
            # If still empty, use any available meals
            if meals.empty:
                meals = self.diet_data
            
            # If completely empty, return default plan
            if meals.empty:
                return self.get_default_meal_plan()
        
        meal_plan = {}
        
        # Get available meal types from data
        available_meal_types = meals['meal_type'].unique()
        
        # Define preferred meal types (can be customized)
        preferred_meal_types = ['Breakfast', 'Mid-Morning', 'Lunch', 'Afternoon Snack', 'Dinner', 'Before Bed']
        
        # Use available meal types or fall back to preferred ones
        meal_types_to_use = []
        for meal_type in preferred_meal_types:
            if meal_type in available_meal_types:
                meal_types_to_use.append(meal_type)
        
        # If no preferred types available, use what's available
        if not meal_types_to_use:
            meal_types_to_use = list(available_meal_types)[:6]  # Limit to 6 meals max
        
        # Group meals by meal_type and generate the plan
        for meal_type in meal_types_to_use:
            meal_options = meals[meals['meal_type'] == meal_type]
            
            # FIXED: Check if meal options exist before sampling
            if not meal_options.empty:
                selected_meal = meal_options.sample(1).iloc[0]  # Pick one random meal for each type
                meal_plan[meal_type] = f"{selected_meal['food_item']} - {selected_meal['calories']} calories"
            else:
                # Provide a fallback meal
                meal_plan[meal_type] = f"Default {meal_type.lower()} - Contact nutritionist for specific recommendations"
        
        # Add health condition specific notes
        if adjusted_diet_type != diet_type:
            meal_plan['Health Notes'] = self.get_health_specific_notes(adjusted_diet_type)
        
        return meal_plan
    
    def get_default_meal_plan(self):
        """Return a default meal plan when no data is available"""
        return {
            'Breakfast': 'Oatmeal with fruits - 300 calories',
            'Mid-Morning': 'Mixed nuts - 150 calories',
            'Lunch': 'Grilled chicken with vegetables - 500 calories',
            'Afternoon Snack': 'Greek yogurt - 120 calories',
            'Dinner': 'Fish with quinoa - 450 calories',
            'Before Bed': 'Herbal tea - 0 calories',
            'Health Notes': 'Default plan - Please consult a nutritionist for personalized recommendations'
        }
    
    def get_health_specific_notes(self, adjusted_diet_type):
        """Get specific dietary notes based on health conditions"""
        # FIXED: Added missing closing brace
        notes = {
            'diabetic_friendly': 'Focus on low glycemic index foods, monitor carbohydrate intake',
            'low_sodium': 'Limit salt intake, avoid processed foods, use herbs for flavoring',
            'heart_healthy': 'Emphasize omega-3 fatty acids, limit saturated fats',
            'low_cholesterol': 'Reduce animal fats, increase fiber intake, focus on plant-based proteins'
        }
        
        return notes.get(adjusted_diet_type, '')

@app.route("/diet", methods=["GET", "POST"])
def diet_plan():
    diet_plan = None
    if request.method == "POST":
        try:
            age = int(request.form["age"])
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            goal = request.form["goal"]
            duration = int(request.form["duration"])
            diet_type = request.form["diet_type"]
            gender = request.form["gender"]
            activity_level = request.form["activity_level"]
            
            # Validate inputs
            if age <= 0 or height <= 0 or weight <= 0 or duration <= 0:
                flash("Please enter valid positive values for all fields", "error")
                return render_template("diet.html")
            
            # Get health conditions if provided
            health_conditions = []
            if "health_conditions" in request.form:
                try:
                    health_conditions = json.loads(request.form["health_conditions"])
                except (json.JSONDecodeError, KeyError):
                    health_conditions = []
            
            user = WeeklyDietPlan(age, height, weight, goal, duration, diet_type, gender, activity_level, health_conditions)
            diet_plan = user.plan
            
        except ValueError as e:
            if "a must be greater than 0" in str(e):
                flash("Unable to generate meal plan. Please check your dietary preferences.", "error")
            else:
                flash("Please enter valid numeric values", "error")
            logger.error(f"Diet plan generation failed: {e}")
            return render_template("diet.html")
        
        except Exception as e:
            flash("An error occurred while generating your meal plan. Please try again.", "error")
            logger.error(f"Diet plan generation failed: {e}")
            return render_template("diet.html")
    
    return render_template("diet.html", diet_plan=diet_plan)

@app.route('/sport', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        fitness_level = request.form.get('fitness_level')
        if fitness_level:
            return jsonify({
                'status': 'success',
                'level': fitness_level,
                'routine': True
            })
    return render_template('sports.html')

@app.route("/workout")
def work():
    return render_template("Sections.html")

@app.route("/GP")
def gp():
    return render_template("page5.html")

@app.route("/workout-plan")
def workout_plan():
    return render_template("workout_plan.html")

@app.route("/D1")
def d1():
    return render_template("day1.html")

@app.route("/D3")
def d3():
    return render_template("day3.html")

@app.route("/D4")
def d4():
    return render_template("day4.html")

@app.route("/D2")
def d2():
    return render_template("day2.html")

@app.route('/yoga')
def yoga():
    """Render the Yoga page"""
    return render_template('Yoga.html')

# AI Chatbot Routes
@app.route('/ai-coach')
def ai_coach():
    """Display the AI fitness coach chatbot interface"""
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """API endpoint for chatbot conversations"""
    try:
        data = request.json
        message = data.get('message', '').strip()
        user_context = data.get('context', {})
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Generate context from user data if available
        context = get_fitness_context(user_context)
        
        # Get AI response
        ai_response = chat_with_fitness_ai(message, context)
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/upload_medical_certificate', methods=['POST'])
def upload_medical_certificate():
    """Handle medical certificate upload and extract health conditions"""
    try:
        if 'medical_certificate' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['medical_certificate']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Check file type
        allowed_extensions = {'txt', 'pdf', 'docx'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_extension not in allowed_extensions:
            return jsonify({'success': False, 'error': 'File type not supported. Please upload PDF, DOCX, or TXT files.'}), 400
        
        # Extract text based on file type
        text_content = ""
        if file_extension == 'txt':
            # Handle text files
            try:
                text_content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                text_content = file.read().decode('latin-1')
                
        elif file_extension == 'pdf':
            # For PDFs, we'll return a message asking users to copy-paste text
            # This avoids heavy PyPDF2 dependency
            return jsonify({
                'success': False,
                'error': 'PDF processing requires text extraction. Please copy-paste the text content or convert to TXT format.'
            }), 400
            
        elif file_extension == 'docx':
            # For DOCX files, we'll return a message asking users to copy-paste text
            # This avoids heavy python-docx dependency
            return jsonify({
                'success': False,
                'error': 'DOCX processing requires text extraction. Please copy-paste the text content or convert to TXT format.'
            }), 400
        
        # Detect health conditions from text
        health_conditions = detect_health_conditions_from_text(text_content)
        
        # Format conditions for display
        conditions_text = ', '.join(health_conditions) if health_conditions else 'None'
        
        return jsonify({
            'success': True,
            'health_conditions': health_conditions,
            'conditions_text': conditions_text
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error processing file: {str(e)}'}), 500

def detect_health_conditions_from_text(text):
    """Detect health conditions from text content"""
    if not text:
        return []
    
    text_lower = text.lower()
    detected_conditions = []
    
    # Medical condition keywords mapping
    conditions = {
        "diabetes": "Diabetes",
        "diabetic": "Diabetes",
        "blood sugar": "Diabetes",
        "glucose": "Diabetes",
        "high blood pressure": "High Blood Pressure",
        "hypertension": "High Blood Pressure",
        "bp": "High Blood Pressure",
        "heart disease": "Heart Disease",
        "cardiac": "Heart Disease",
        "coronary": "Heart Disease",
        "asthma": "Asthma",
        "respiratory": "Respiratory Issues",
        "cancer": "Cancer",
        "tumor": "Cancer",
        "malignant": "Cancer",
        "kidney disease": "Kidney Disease",
        "renal": "Kidney Disease",
        "lung disease": "Lung Disease",
        "pulmonary": "Lung Disease",
        "arthritis": "Arthritis",
        "thyroid": "Thyroid Disorder",
        "cholesterol": "High Cholesterol",
        "migraine": "Migraine",
        "depression": "Depression",
        "anxiety": "Anxiety"
    }
    
    # Check for each condition
    for keyword, condition in conditions.items():
        if keyword in text_lower and condition not in detected_conditions:
            detected_conditions.append(condition)
    
    return detected_conditions

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal server error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)