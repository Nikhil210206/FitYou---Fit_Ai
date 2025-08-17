from flask import Flask, render_template, request, jsonify
import random
import pandas as pd
import os
import requests
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Ollama API configuration - REMOVED FOR VERCEL COMPATIBILITY
# OLLAMA_BASE_URL = "http://localhost:11434"
# OLLAMA_MODEL = "YOUR_MODEL_NAME"  # Replace with your actual model name

# Rule-based fitness chatbot for Vercel compatibility
def chat_with_fitness_ai(message, context=""):
    """
    Rule-based fitness AI response system that works in Vercel
    """
    message_lower = message.lower()
    
    # Fitness advice patterns
    if any(word in message_lower for word in ['workout', 'exercise', 'training']):
        if 'beginner' in message_lower:
            return "For beginners, start with 20-30 minutes of cardio 3 times a week. Focus on form over intensity. Try walking, cycling, or swimming to build endurance safely."
        elif 'strength' in message_lower:
            return "Start with bodyweight exercises: push-ups, squats, lunges, and planks. Do 2-3 sets of 10-15 reps. Rest 1-2 minutes between sets."
        else:
            return "A good workout routine includes: 1) 5-10 min warm-up, 2) 20-40 min main exercise, 3) 5-10 min cool-down. Aim for 150 minutes of moderate activity weekly."
    
    elif any(word in message_lower for word in ['diet', 'nutrition', 'food', 'eat']):
        if 'weight loss' in message_lower:
            return "For weight loss: Create a 500-calorie daily deficit, eat protein-rich foods, include vegetables, and stay hydrated. Track your meals and be consistent."
        elif 'muscle' in message_lower:
            return "For muscle building: Eat 1.6-2.2g protein per kg body weight daily. Include complex carbs, healthy fats, and eat in a slight calorie surplus."
        else:
            return "A balanced diet includes: lean proteins, whole grains, fruits, vegetables, and healthy fats. Stay hydrated with 8-10 glasses of water daily."
    
    elif any(word in message_lower for word in ['motivation', 'motivated', 'tired']):
        return "Remember why you started! Set small, achievable goals. Celebrate progress, not perfection. Find a workout buddy or join a fitness community for support."
    
    elif any(word in message_lower for word in ['injury', 'pain', 'hurt']):
        return "If you're experiencing pain, stop exercising immediately. Rest, ice, compress, and elevate (RICE). Consult a healthcare professional for persistent pain."
    
    elif any(word in message_lower for word in ['goal', 'target', 'aim']):
        return "Set SMART goals: Specific, Measurable, Achievable, Relevant, and Time-bound. Break big goals into smaller milestones. Track your progress regularly."
    
    elif any(word in message_lower for word in ['form', 'technique', 'proper']):
        return "Proper form is crucial! Start with lighter weights, focus on controlled movements, and consider working with a certified trainer. Quality over quantity always."
    
    elif any(word in message_lower for word in ['rest', 'recovery', 'sleep']):
        return "Rest days are essential! Aim for 7-9 hours of sleep, take 1-2 rest days per week, and listen to your body. Recovery is when your body gets stronger."
    
    elif any(word in message_lower for word in ['cardio', 'aerobic', 'endurance']):
        return "Cardio improves heart health and burns calories. Start with 20-30 minutes of moderate activity like brisk walking, cycling, or swimming. Gradually increase duration and intensity."
    
    elif any(word in message_lower for word in ['hiit', 'interval', 'intense']):
        return "HIIT workouts are great for burning fat and improving fitness. Try 30 seconds of high-intensity exercise followed by 30 seconds of rest. Repeat for 10-20 minutes."
    
    else:
        return "I'm FitAI, your fitness coach! I can help with workout routines, nutrition advice, motivation, injury prevention, and fitness goals. What specific fitness topic would you like to discuss?"

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
        meal_plan = {}

        # Group meals by meal_type and generate the plan
        for meal_type in ['Breakfast', 'Mid-Morning', 'Lunch', 'Afternoon Snack', 'Dinner', 'Before Bed']:
            selected_meal = meals[meals['meal_type'] == meal_type].sample(1).iloc[0]  # Pick one random meal for each type
            meal_plan[meal_type] = f"{selected_meal['food_item']} - {selected_meal['calories']} calories"
        
        # Add health condition specific notes
        if adjusted_diet_type != diet_type:
            meal_plan['Health Notes'] = self.get_health_specific_notes(adjusted_diet_type)
        
        return meal_plan
    
    def get_health_specific_notes(self, adjusted_diet_type):
        """Get specific dietary notes based on health conditions"""
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
        age = int(request.form["age"])
        height = float(request.form["height"])
        weight = float(request.form["weight"])
        goal = request.form["goal"]
        duration = int(request.form["duration"])
        diet_type = request.form["diet_type"]
        gender = request.form["gender"]
        activity_level = request.form["activity_level"]
        
        # Get health conditions if provided
        health_conditions = []
        if "health_conditions" in request.form:
            try:
                health_conditions = json.loads(request.form["health_conditions"])
            except (json.JSONDecodeError, KeyError):
                health_conditions = []

        user = WeeklyDietPlan(age, height, weight, goal, duration, diet_type, gender, activity_level, health_conditions)
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

# ----- Load & prep data -----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # directory of app.py
file_path = os.path.join(BASE_DIR, "workout data", "Workout.csv")

df = pd.read_csv(file_path)
df['features'] = df['Body Part'] + " " + df['Type of Muscle'] + " " + df['Workout']

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['features'])

# ----- Recommender -----
def recommend_workouts(user_input, threshold=0.4):
    user_vec = vectorizer.transform([user_input])
    sim_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()

    mask = sim_scores > threshold
    if not mask.any():
        return []

    # Build results with sets/reps (NO similarity in output)
    hits = df.loc[mask, ['Workout', 'Sets', 'Reps per Set']].copy()
    hits = hits.sort_index()  # keep original CSV order

    return [
        {
            "workout": row['Workout'],
            "sets": row['Sets'],
            "reps": row['Reps per Set']
        }
        for _, row in hits.iterrows()
    ]

# ----- Flask route -----
@app.route('/fitness', methods=['GET', 'POST'], endpoint='fitness')
def fitness_index():
    user_query = None
    threshold = 0.4
    results = None

    if request.method == 'POST':
        # take raw input, split on commas (multi-input support)
        user_query_raw = request.form.get('user_query', '').strip()
        user_query_list = [q.strip() for q in user_query_raw.split(",") if q.strip()]
        user_query = " ".join(user_query_list)  # join all as one query string

        # threshold
        threshold_str = request.form.get('threshold', '0.4').strip()
        try:
            threshold = float(threshold_str)
        except ValueError:
            threshold = 0.4

        if user_query:
            results = recommend_workouts(user_query, threshold)

    return render_template(
        'fitness.html',
        user_query=user_query,
        threshold=threshold,
        results=results
    )

if __name__ == '__main__':
    app.run(debug=True)

# # backend/adjuster.py
# import os
# from flask import Blueprint, request, jsonify
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# import numpy as np
# from sklearn.neighbors import NearestNeighbors
# import json
# import datetime

# bp = Blueprint('adjuster', __name__, url_prefix='/api/adjuster')

# # ---------- CONFIG ----------
# MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/fitai")
# client = MongoClient(MONGO_URI)
# db = client.get_default_database() or client['fitai']

# # If you integrate Google Generative AI, supply API key and model via env vars:
# # GOOGLE_API_KEY, GOOGLE_GEN_AI_MODEL
# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")  # placeholder
# GOOGLE_GEN_AI_MODEL = os.environ.get("GOOGLE_GEN_AI_MODEL", "models/text-bison-001")

# # ---------- Utility: local fallback suggestions using NearestNeighbors ----------
# def build_meal_index():
#     # build index from meals collection. Use calories+protein+carbs+fat normalized.
#     meals = list(db.meals.find({}))
#     if not meals:
#         return None, [], None
#     X = []
#     ids = []
#     for m in meals:
#         macros = m.get('macros', {})
#         # default zero if missing
#         row = [
#             float(macros.get('calories', 0)),
#             float(macros.get('protein', 0)),
#             float(macros.get('carbs', 0)),
#             float(macros.get('fat', 0))
#         ]
#         X.append(row)
#         ids.append(str(m['_id']))
#     X = np.array(X)
#     # normalize by column
#     X_mean = X.mean(axis=0)
#     X_std = X.std(axis=0)
#     X_std[X_std == 0] = 1.0
#     X_norm = (X - X_mean) / X_std
#     knn = NearestNeighbors(n_neighbors=10, metric='euclidean')
#     knn.fit(X_norm)
#     return knn, ids, (X_mean, X_std)

# # Build once on import (can be improved to rebuild on meal changes)
# _knn_index, _knn_ids, _knn_norm_params = build_meal_index()

# def find_similar_meals_by_macros(target_macros, top_k=5, tolerance=0.15, cuisine=None, meal_type=None, exclude_ids=None):
#     """
#     target_macros: dict with calories, protein, carbs, fat
#     tolerance: fraction allowed difference (e.g., 0.15 => ±15%)
#     """
#     if _knn_index is None:
#         return []

#     X_mean, X_std = _knn_norm_params
#     target_row = np.array([
#         float(target_macros.get('calories', 0)),
#         float(target_macros.get('protein', 0)),
#         float(target_macros.get('carbs', 0)),
#         float(target_macros.get('fat', 0))
#     ])
#     target_norm = (target_row - X_mean) / X_std
#     dists, neigh = _knn_index.kneighbors([target_norm], n_neighbors=min(10, len(_knn_ids)))
#     candidate_ids = [ObjectId(_knn_ids[i]) for i in neigh[0]]
#     # filter by tolerance, cuisine, meal_type, exclude
#     suggestions = []
#     for mid in candidate_ids:
#         if exclude_ids and str(mid) in exclude_ids:
#             continue
#         m = db.meals.find_one({"_id": mid})
#         if not m:
#             continue
#         macros = m.get('macros', {})
#         ok = True
#         for k in ['calories','protein','carbs','fat']:
#             target_v = float(target_macros.get(k,0))
#             cand_v = float(macros.get(k,0))
#             if target_v == 0:
#                 continue
#             if abs(cand_v - target_v) / target_v > tolerance:
#                 ok = False
#                 break
#         if not ok:
#             continue
#         if cuisine and m.get('cuisine') != cuisine:
#             continue
#         if meal_type and m.get('type') != meal_type:
#             continue
#         suggestions.append(m)
#         if len(suggestions) >= top_k:
#             break
#     return suggestions

# # ---------- Optional: Wrapper to call Google Generative AI ----------
# def call_google_gen_ai_generate_swap(original_meal, constraints, n=3):
#     """
#     Placeholder function — implement with your Google Generative AI client code.
#     It should return a list of suggested meals (dicts with title, ingredients, macros, recipe_steps)
#     """
#     if not GOOGLE_API_KEY:
#         return []

#     # Example prompt to send:
#     prompt = {
#         "prompt": f"""You are a helpful assistant that suggests Indian meal alternatives.
# Original meal: {json.dumps(original_meal, indent=0)}
# Constraints: {json.dumps(constraints)}
# Return {n} alternatives as JSON list; each item must contain: title, type (vegetarian/non-vegetarian/vegan), cuisine, ingredients(list of {{"name","qty"}}), macros (calories, protein, carbs, fat), and recipe_steps (list of strings)."""
#     }

#     # NOTE: Implementation depends on google client library. Here we return [] as placeholder.
#     # You must implement this with your project's Google Gen AI integration.
#     return []

# # ---------- API: Adjust meal ----------
# @bp.route('/adjust', methods=['POST'])
# def adjust_meal():
#     """
#     Request JSON:
#     {
#       "user_id": "<user_id>",
#       "meal_id": "<meal_id>",  # original meal
#       "constraints": {
#          "type": "vegetarian" | "non-vegetarian" | "vegan" | null,
#          "calorie_tolerance": 0.10,   # 10%
#          "exclude_ingredients": ["peanut"],
#          "prefer_cuisine": "South Indian"
#       },
#       "use_ai": true  # whether to call Google Gen AI (if available)
#     }
#     """
#     data = request.get_json()
#     user_id = data.get('user_id')
#     meal_id = data.get('meal_id')
#     constraints = data.get('constraints', {})
#     use_ai = data.get('use_ai', True)

#     if not meal_id:
#         return jsonify({"error": "meal_id required"}), 400

#     orig = db.meals.find_one({"_id": ObjectId(meal_id)})
#     if not orig:
#         return jsonify({"error": "meal not found"}), 404

#     # 1) Try AI suggestions first (if allowed)
#     suggestions = []
#     if use_ai and GOOGLE_API_KEY:
#         suggestions = call_google_gen_ai_generate_swap(orig, constraints, n=3)

#     # 2) Always provide fallback suggestions from local DB (nearest macros)
#     exclude_ids = [meal_id]
#     local_suggestions = find_similar_meals_by_macros(orig.get('macros', {}), top_k=3, tolerance=constraints.get('calorie_tolerance', 0.15), cuisine=constraints.get('prefer_cuisine'), meal_type=constraints.get('type'), exclude_ids=exclude_ids)
#     # format llocal suggestions minimal fields
#     local_suggestions_clean = []
#     for s in local_suggestions:
#         # filter out suggestions that contain excluded ingredients
#         excluded = False
#         ex_ing = set([i.lower() for i in constraints.get('exclude_ingredients', [])])
#         for ing in s.get('ingredients', []):
#             if ing.get('name','').lower() in ex_ing:
#                 excluded = True
#                 break
#         if excluded:
#             continue
#         local_suggestions_clean.append({
#             "id": str(s['_id']),
#             "title": s.get('title'),
#             "type": s.get('type'),
#             "cuisine": s.get('cuisine'),
#             "ingredients": s.get('ingredients'),
#             "macros": s.get('macros'),
#             "recipe_steps": s.get('recipe_steps')
#         })
#     # merge AI suggestions (if any) + local suggestions, dedupe by title
#     seen = set()
#     merged = []
#     for s in (suggestions or []):
#         title = s.get('title')
#         if title and title not in seen:
#             merged.append(s)
#             seen.add(title)
#     for s in local_suggestions_clean:
#         if s.get('title') not in seen:
#             merged.append(s)
#             seen.add(s.get('title'))

#     # return up to 3 suggestions
#     merged = merged[:3]

#     # record the adjustment search (not commit to plan yet)
#     db.meal_adjustments.insert_one({
#         "user_id": ObjectId(user_id) if user_id else None,
#         "original_meal_id": ObjectId(meal_id),
#         "query_constraints": constraints,
#         "results_count": len(merged),
#         "created_at": datetime.datetime.utcnow()
#     })

#     return jsonify({"original": {"id": str(orig['_id']), "title": orig.get('title'), "macros": orig.get('macros')}, "suggestions": merged})
# # backend/tests/test_adjuster.py
# import json
# from backend.adjuster import bp as adjuster_bp
# from flask import Flask
# import os

# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(adjuster_bp)
#     return app

# def test_adjust_missing_meal():
#     app = create_app()
#     client = app.test_client()
#     res = client.post('/api/adjuster/adjust', json={"user_id": None, "meal_id": "000000000000000000000000"})
#     assert res.status_code in (400,404)

