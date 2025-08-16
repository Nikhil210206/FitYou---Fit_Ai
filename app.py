from flask import Flask, render_template, request, jsonify
import random
import pandas as pd
import os
import PyPDF2
from docx import Document
from werkzeug.utils import secure_filename
import tempfile
import requests
import json

app = Flask(__name__)

# Configuration for file uploads
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "YOUR_MODEL_NAME"  # Replace with your actual model name

# Read exercises from CSV dataset 
API_KEY = os.getenv('your_api_key')

# Medical Certificate Processing Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file):
    """Extract text from uploaded file based on its type."""
    try:
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension == 'pdf':
            return extract_text_from_pdf(file)
        elif file_extension == 'docx':
            return extract_text_from_docx(file)
        elif file_extension == 'txt':
            return file.read().decode('utf-8')
        else:
            return None
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return None

def extract_text_from_pdf(file):
    """Extract text from PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None

def extract_text_from_docx(file):
    """Extract text from DOCX file."""
    try:
        doc = Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading DOCX: {str(e)}")
        return None

def detect_health_conditions(text):
    """Detect health conditions from extracted text."""
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

# Ollama AI Chatbot Functions
def chat_with_ollama(message, context=""):
    """
    Send a message to Ollama API and get AI response
    """
    try:
        fitness_context = f"""
You are FitAI, an expert fitness and health coach. You provide personalized advice on:
- Workout routines and exercise techniques
- Nutrition and diet planning
- Fitness goal setting and motivation
- Health and wellness tips
- Form corrections and injury prevention

Always be encouraging, professional, and provide actionable advice. Keep responses concise but informative.

{context}

User: {message}
FitAI:"""
        
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": fitness_context,
            "stream": False
        }
        
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json().get('response', 'Sorry, I could not generate a response.')
        else:
            return f"Error: Unable to connect to AI model (Status: {response.status_code})"
            
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to Ollama. Please make sure Ollama is running with 'ollama serve' and the qwen2:0.5b model is installed."
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The AI model might be processing a complex request."
    except Exception as e:
        return f"Error: {str(e)}"

def get_fitness_context(user_data=None):
    """
    Generate context based on user's fitness data
    """
    if user_data:
        return f"User context: Weight: {user_data.get('weight', 'N/A')}kg, Height: {user_data.get('height', 'N/A')}cm, Goal: {user_data.get('goal', 'general fitness')}"
    return ""

# Medical Certificate Upload Route
@app.route('/upload_medical_certificate', methods=['POST'])
def upload_medical_certificate():
    """Handle medical certificate upload and processing."""
    try:
        if 'medical_certificate' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['medical_certificate']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, or TXT files only.'}), 400
        
        # Extract text from the file
        extracted_text = extract_text_from_file(file)
        
        if extracted_text is None:
            return jsonify({'error': 'Could not extract text from the file. Please check the file format.'}), 400
        
        # Detect health conditions
        health_conditions = detect_health_conditions(extracted_text)
        
        return jsonify({
            'success': True,
            'health_conditions': health_conditions,
            'conditions_text': ', '.join(health_conditions) if health_conditions else 'None'
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred while processing the file: {str(e)}'}), 500

# Exercise and Routine Functions
def load_exercises():
    try:
        return pd.read_csv('exercises.csv')
    except FileNotFoundError:
        print("Error: exercises.csv file not found")
        return pd.DataFrame()  # Return empty DataFrame
    except Exception as e:
        print(f"Error loading exercises: {str(e)}")
        return pd.DataFrame()

# Routine generator logic using the dataset
def output(intensity):
    df = load_exercises()  # Load dataset
    if df.empty:
        return ["Error: Could not load exercise data"]
    
    routine_list = []

    def add_exercises(category, max_intensity_ratio):
        max_intensity = intensity * max_intensity_ratio
        current_sum = 0

        category_exercises = df[df['category'] == category]  # Filter by category

        for _, exercise in category_exercises.iterrows():
            current_sum += 1  # Each exercise counts as one in the total
            if max_intensity > current_sum:
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

    return routine_list

# Function to calculate BMI and adjust intensity
def calculate_intensity(weight, height):
    # Input validation
    if height <= 0 or weight <= 0:
        raise ValueError("Height and weight must be positive values")
    
    if height > 300 or weight > 500:  # Reasonable upper limits
        raise ValueError("Height or weight values seem unrealistic")
    
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

# Load diet data from CSV
def load_diet_data():
    try:
        return pd.read_csv('diet_data.csv')
    except FileNotFoundError:
        print("Error: diet_data.csv file not found")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading diet data: {str(e)}")
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
        self.diet_data = load_diet_data()
        self.plan = self.create_diet_plan()

    def calculate_bmr(self):
        if self.gender == 'male':
            return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

    def adjust_calories(self):
        base_calories = self.bmr
        
        # Adjust for activity level
        if self.activity_level == "sedentary":
            base_calories *= 1.2
        elif self.activity_level == "moderate":
            base_calories *= 1.55
        elif self.activity_level == "active":
            base_calories *= 1.9
        
        # Adjust for goal
        if self.goal == 'weight gain':
            return base_calories + 500
        elif self.goal == 'weight loss':
            return base_calories - 500
        else:
            return base_calories

    def create_diet_plan(self):
        """Create personalized diet plan using ALL user inputs."""
        if self.diet_data.empty:
            return self.create_fallback_plan()
        
        # Filter by diet type (vegetarian/non-vegetarian)
        diet_filtered = self.diet_data
        if 'diet_preference' in self.diet_data.columns:
            diet_filtered = self.diet_data[self.diet_data['diet_preference'] == self.diet_type]
        
        # Filter by goal (weight gain/loss)
        goal_type = 'weight_gain' if self.goal == 'weight gain' else 'weight_loss'
        if 'goal_type' in diet_filtered.columns:
            goal_filtered = diet_filtered[diet_filtered['goal_type'] == goal_type]
        else:
            goal_filtered = diet_filtered
        
        plan = {}
        for i in range(7):
            day_name = f'Day {i+1}'
            plan[day_name] = self.get_personalized_meal_plan(goal_filtered, i+1)
        
        return plan

    def get_personalized_meal_plan(self, filtered_data, day):
        """Generate meal plan that considers user's health conditions and calorie needs."""
        
        # Calculate target calories per meal
        daily_calories = int(self.daily_calories)
        meal_distribution = {
            'Breakfast': 0.25,      # 25% of daily calories
            'Mid-Morning': 0.10,    # 10% of daily calories  
            'Lunch': 0.30,          # 30% of daily calories
            'Afternoon Snack': 0.10, # 10% of daily calories
            'Dinner': 0.20,         # 20% of daily calories
            'Before Bed': 0.05      # 5% of daily calories
        }
        
        meal_plan = {}
        meal_types = ['Breakfast', 'Mid-Morning', 'Lunch', 'Afternoon Snack', 'Dinner', 'Before Bed']
        
        for meal_type in meal_types:
            target_calories = int(daily_calories * meal_distribution.get(meal_type, 0.15))
            
            # Get suitable meals for this type
            if 'meal_type' in filtered_data.columns:
                type_meals = filtered_data[filtered_data['meal_type'] == meal_type]
            else:
                type_meals = filtered_data
            
            if not type_meals.empty:
                # Filter by health conditions if detected
                suitable_meals = self.filter_by_health_conditions(type_meals)
                
                if suitable_meals.empty:
                    suitable_meals = type_meals  # Fallback if no suitable meals
                
                # Select meal closest to target calories
                selected_meal = self.select_meal_by_calories(suitable_meals, target_calories)
                
                if selected_meal is not None:
                    meal_info = self.format_meal_info(selected_meal, target_calories)
                    meal_plan[meal_type] = meal_info
                else:
                    meal_plan[meal_type] = f"Custom meal - Target: {target_calories} calories"
            else:
                meal_plan[meal_type] = f"Custom meal - Target: {target_calories} calories"
        
        return meal_plan

    def filter_by_health_conditions(self, meals_df):
        """Filter meals based on detected health conditions."""
        if not self.health_conditions:
            return meals_df
        
        # Health condition dietary restrictions
        restrictions = {
            'Diabetes': ['high sugar', 'sweet', 'candy', 'cake', 'dessert'],
            'High Blood Pressure': ['high sodium', 'salty', 'pickled', 'processed'],
            'Heart Disease': ['high fat', 'fried', 'fatty', 'butter'],
            'High Cholesterol': ['high cholesterol', 'egg yolk', 'fatty meat']
        }
        
        suitable_meals = meals_df.copy()
        
        for condition in self.health_conditions:
            if condition in restrictions:
                # Remove meals with restricted keywords
                for restriction in restrictions[condition]:
                    if 'food_item' in suitable_meals.columns:
                        suitable_meals = suitable_meals[
                            ~suitable_meals['food_item'].str.lower().str.contains(restriction, na=False)
                        ]
        
        return suitable_meals

    def select_meal_by_calories(self, meals_df, target_calories):
        """Select meal closest to target calorie count."""
        if meals_df.empty:
            return None
        
        if 'calories' in meals_df.columns:
            # Convert calories to numeric, handle any non-numeric values
            meals_df = meals_df.copy()
            meals_df['calories_numeric'] = pd.to_numeric(meals_df['calories'], errors='coerce')
            meals_df = meals_df.dropna(subset=['calories_numeric'])
            
            if not meals_df.empty:
                # Find meal with calories closest to target
                meals_df['calorie_diff'] = abs(meals_df['calories_numeric'] - target_calories)
                best_meal = meals_df.loc[meals_df['calorie_diff'].idxmin()]
                return best_meal
        
        # Fallback to random selection
        return meals_df.sample(1).iloc[0] if not meals_df.empty else None

    def format_meal_info(self, meal_row, target_calories):
        """Format meal information for display."""
        try:
            food_item = meal_row.get('food_item', 'Custom meal')
            actual_calories = meal_row.get('calories', target_calories)
            
            # Add health-conscious note if conditions detected
            health_note = ""
            if self.health_conditions:
                health_note = f" (Suitable for: {', '.join(self.health_conditions)})"
            
            return f"{food_item} - {actual_calories} calories{health_note}"
        except:
            return f"Custom meal - {target_calories} calories"

    def create_fallback_plan(self):
        """Create a basic plan when CSV data is not available."""
        daily_calories = int(self.daily_calories)
        
        if self.diet_type == 'vegetarian':
            base_meals = {
                'Breakfast': f"Oatmeal with fruits - {int(daily_calories * 0.25)} calories",
                'Mid-Morning': f"Mixed nuts - {int(daily_calories * 0.10)} calories",
                'Lunch': f"Lentil curry with brown rice - {int(daily_calories * 0.30)} calories",
                'Afternoon Snack': f"Greek yogurt - {int(daily_calories * 0.10)} calories",
                'Dinner': f"Grilled vegetables with quinoa - {int(daily_calories * 0.20)} calories",
                'Before Bed': f"Herbal tea - {int(daily_calories * 0.05)} calories"
            }
        else:
            base_meals = {
                'Breakfast': f"Scrambled eggs with spinach - {int(daily_calories * 0.25)} calories",
                'Mid-Morning': f"Protein shake - {int(daily_calories * 0.10)} calories",
                'Lunch': f"Grilled chicken with sweet potato - {int(daily_calories * 0.30)} calories",
                'Afternoon Snack': f"Cottage cheese - {int(daily_calories * 0.10)} calories",
                'Dinner': f"Baked fish with vegetables - {int(daily_calories * 0.20)} calories",
                'Before Bed': f"Casein protein - {int(daily_calories * 0.05)} calories"
            }
        
        # Add health condition notes
        if self.health_conditions:
            health_note = f" (Plan adjusted for: {', '.join(self.health_conditions)})"
            for meal_type in base_meals:
                base_meals[meal_type] += health_note
        
        return {f'Day {i+1}': base_meals for i in range(7)}

# Route Definitions
@app.route('/gen')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        
        # Validate inputs
        if weight <= 0 or height <= 0:
            return render_template('index.html', error="Please enter positive values for weight and height")
        
        intensity = calculate_intensity(weight, height)
        routine = output(intensity)
        return render_template('index.html', routine=routine)
    except ValueError as e:
        return render_template('index.html', error=str(e))
    except Exception as e:
        return render_template('index.html', error="An error occurred while generating your routine")

@app.route("/")
def home_page():
    return render_template("Home.html")

@app.route("/diet", methods=["GET", "POST"])
def diet_plan():
    # Preserve form data for display
    form_data = {}
    diet_plan_result = None
    
    if request.method == "POST":
        try:
            # Capture form data
            form_data = {
                'age': request.form.get("age", ""),
                'height': request.form.get("height", ""),
                'weight': request.form.get("weight", ""),
                'goal': request.form.get("goal", ""),
                'duration': request.form.get("duration", ""),
                'diet_type': request.form.get("diet_type", ""),
                'gender': request.form.get("gender", ""),
                'activity_level': request.form.get("activity_level", "")
            }
            
            # Validate and convert
            age = int(form_data['age'])
            height = float(form_data['height'])
            weight = float(form_data['weight'])
            goal = form_data['goal']
            duration = form_data['duration']
            diet_type = form_data['diet_type']
            gender = form_data['gender']
            activity_level = form_data['activity_level']

            # Validate inputs
            if age <= 0 or height <= 0 or weight <= 0:
                return render_template("diet.html", error="Please enter positive values", form_data=form_data)

            # Get health conditions from session/hidden input if available
            health_conditions = request.form.getlist('health_conditions') if 'health_conditions' in request.form else []

            user = WeeklyDietPlan(age, height, weight, goal, duration, diet_type, gender, activity_level, health_conditions)
            diet_plan_result = user.plan

        except ValueError:
            return render_template("diet.html", error="Please enter valid numeric values", form_data=form_data)
        except Exception as e:
            return render_template("diet.html", error="An error occurred while generating your diet plan", form_data=form_data)

    return render_template("diet.html", diet_plan=diet_plan_result, form_data=form_data)

@app.route('/sport', methods=['GET', 'POST'])
def sport():
    routine = None
    
    if request.method == 'POST':
        fitness_level = request.form.get('fitness_level')
        
        # Improved routine data structure
        routines = {
            'beginner': {
                'strength': [
                    {'exercise': 'Push-ups', 'sets': 2, 'reps': '8-10'},
                    {'exercise': 'Bodyweight Squats', 'sets': 2, 'reps': '10-12'},
                    {'exercise': 'Wall Sits', 'duration': '30 seconds'}
                ],
                'cardio': [
                    {'exercise': 'Walking', 'duration': '20 minutes'},
                    {'exercise': 'Light Jogging', 'duration': '10 minutes'}
                ],
                'flexibility': [
                    {'exercise': 'Basic Stretching', 'duration': '10 minutes'},
                    {'exercise': 'Yoga Poses', 'duration': '15 minutes'}
                ]
            },
            'intermediate': {
                'strength': [
                    {'exercise': 'Push-ups', 'sets': 3, 'reps': '12-15'},
                    {'exercise': 'Squats', 'sets': 3, 'reps': '15-20'},
                    {'exercise': 'Lunges', 'sets': 3, 'reps': '10-12 per leg'},
                    {'exercise': 'Plank', 'duration': '45 seconds'}
                ],
                'cardio': [
                    {'exercise': 'Running', 'duration': '25 minutes'},
                    {'exercise': 'Cycling', 'duration': '20 minutes'}
                ],
                'flexibility': [
                    {'exercise': 'Dynamic Stretching', 'duration': '10 minutes'},
                    {'exercise': 'Yoga Flow', 'duration': '20 minutes'}
                ]
            },
            'advanced': {
                'strength': [
                    {'exercise': 'Push-ups', 'sets': 4, 'reps': '20-25'},
                    {'exercise': 'Jump Squats', 'sets': 4, 'reps': '15-20'},
                    {'exercise': 'Burpees', 'sets': 3, 'reps': '10-15'},
                    {'exercise': 'Mountain Climbers', 'sets': 3, 'reps': '20-30'},
                    {'exercise': 'Plank', 'duration': '90 seconds'}
                ],
                'cardio': [
                    {'exercise': 'HIIT Running', 'duration': '30 minutes'},
                    {'exercise': 'Sprint Intervals', 'duration': '20 minutes'}
                ],
                'flexibility': [
                    {'exercise': 'Advanced Stretching', 'duration': '15 minutes'},
                    {'exercise': 'Power Yoga', 'duration': '25 minutes'}
                ]
            }
        }
        
        if fitness_level in routines:
            routine = routines[fitness_level]
        else:
            return render_template('sports.html', error="Invalid fitness level selected")
    
    return render_template('sports.html', routine=routine)

@app.route("/workout")
def work():
    return render_template("Sections.html")

@app.route("/GP")
def gp():
    return render_template("page5.html")

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
        ai_response = chat_with_ollama(message, context)
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)