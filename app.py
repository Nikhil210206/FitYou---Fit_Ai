from flask import Flask, render_template, request, jsonify
import random
import pandas as pd
import os
import requests
import json

app = Flask(__name__)

# Ollama API configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "YOUR_MODEL_NAME"  # Replace with your actual model name

# Ollama client functions
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
def load_exercises():
    return pd.read_csv('exercises.csv')

# Routine generator logic using the dataset
def output(intensity):
    df = load_exercises()  # Load dataset
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
                    reps = random.randint(reps_min, reps_max)
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
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    intensity = calculate_intensity(weight, height)
    routine = output(intensity)
    return render_template('index.html', routine=routine)

@app.route("/")
def diet():
    return render_template("Home.html")

# Load diet data from CSV
def load_diet_data():
    return pd.read_csv('diet_data.csv')

class WeeklyDietPlan:
    def __init__(self, age, height, weight, goal, duration, diet_type, gender, activity_level):
        self.age = age
        self.height = height
        self.weight = weight
        self.goal = goal
        self.duration = duration
        self.diet_type = diet_type
        self.gender = gender
        self.activity_level = activity_level
        self.bmr = self.calculate_bmr()
        self.daily_calories = self.adjust_calories()
        self.diet_data = load_diet_data()  # Load dataset here
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
        if self.diet_type == 'weight gain':
            return {f'Day {i+1}': self.get_meal_plan(i+1, 'weight_gain') for i in range(7)}
        elif self.diet_type == 'weight loss':
            return {f'Day {i+1}': self.get_meal_plan(i+1, 'weight_loss') for i in range(7)}
        else:
            return {}

    def get_meal_plan(self, day, diet_type):
        # Filter the dataset by diet_type
        meals = self.diet_data[self.diet_data['diet_type'] == diet_type]
        meal_plan = {}

        # Group meals by meal_type and generate the plan
        for meal_type in ['Breakfast', 'Mid-Morning', 'Lunch', 'Afternoon Snack', 'Dinner', 'Before Bed']:
            selected_meal = meals[meals['meal_type'] == meal_type].sample(1).iloc[0]  # Pick one random meal for each type
            meal_plan[meal_type] = f"{selected_meal['food_item']} - {selected_meal['calories']} calories"
        
        return meal_plan
@app.route("/diet", methods=["GET", "POST"])
def diet_plan():
    diet_plan = None
    if request.method == "POST":
        age = int(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        goal = request.form["goal"]
        duration = request.form["duration"]
        diet_type = request.form["diet_type"]
        gender = request.form["gender"]
        activity_level = request.form["activity_level"]

        user = WeeklyDietPlan(age, height, weight, goal, duration, diet_type, gender, activity_level)
        diet_plan = user.plan

    return render_template("diet.html", diet_plan=diet_plan)

@app.route('/sport', methods=['GET', 'POST'])
def home():
    routine = {'beginner': 'Beginner Routine', 'intermediate': 'Intermediate Routine', 'advanced': 'Advanced Routine'}  # Example routines
    
    if request.method == 'POST':
        fitness_level = request.form.get('fitness_level')
        if fitness_level in routine:  # Check if fitness level exists in routine dictionary
            return render_template('sports.html', routine=routine[fitness_level])  # Return the specific routine
        else:
            return render_template('sports.html', error="Invalid fitness level")  # Handle invalid fitness level case
    
    return render_template('sports.html', routine=None)




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


