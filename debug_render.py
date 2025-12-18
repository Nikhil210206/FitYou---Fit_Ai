from flask import Flask, render_template

app = Flask(__name__)

# Mock all endpoints used in url_for
@app.route('/')
def home(): return render_template('Home.html')

@app.route('/home')
def home_alt(): return ""

@app.route('/sport')
def sports(): return ""

@app.route('/workout')
def work(): return ""

@app.route('/diet-plan')
def diet_plan(): return ""

@app.route('/yoga')
def yoga(): return ""

@app.route('/meditation')
def meditation(): return "" # Mocking even if replaced, just in case

@app.route('/coaches')
def coaches(): return ""

@app.route('/ai-coach')
def ai_coach(): return ""

@app.route('/workout-plan')
def workout_plan(): return ""

@app.route('/gen')
def generate(): return ""

if __name__ == "__main__":
    with app.app_context():
        try:
            print("Attempting to render Home.html...")
            rendered = render_template('Home.html')
            print("Successfully rendered Home.html")
            print("Length:", len(rendered))
        except Exception as e:
            print("FAILED to render Home.html")
            print(e)
