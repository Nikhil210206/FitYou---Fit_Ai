[![OSCI-Project-Banner.png](https://i.postimg.cc/76mJvBmF/OSCI-Project-Banner.png)](https://postimg.cc/8JfzMb84)

<p align="center">
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React.js">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Google%20Generative%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Generative AI">
</p>

# FitAi: Your AI Fitness Companion 🌟

FitAi redefines fitness with **AI-driven personalized plans** for workouts and diets. Empowering your fitness journey with cutting-edge technology and expert guidance, FitAi adapts to your unique goals and lifestyle.

**🌐 Live Deployment:** [Check it out here 👀](https://fityou-fit-ai.onrender.com/)

**Points for issues on leaderboard:** (Currently not started yet)
1 star - 5 points |
2 star - 10 points |
3 star - 15 points

## 📑 Table of Contents

- [🌟 Key Features](#-key-features)
- [💻 Technologies at Work](#-technologies-at-work)
- [🎯 Highlights](#-highlights)
- [📂 Project Structure](#-project-structure)
- [⚙️ How to Install](#️-how-to-install)
- [🛠️ Usage](#️-usage)
- [🚀 Future Enhancements](#-future-enhancements)
- [🤝 Contributions Welcome](#-contributions-welcome)
- [📞 Contact](#-contact)
- [🙏 Acknowledgments](#-acknowledgments)
- [📜 License](#-license)


## 🌟 Key Features

- 🏋️ **Personalized Workout Plans**
  Tailored routines based on your preferences, fitness goals, and available equipment, ensuring an effective and safe workout experience.

- 🥗 **Customized Diet Plans**
  Balanced meal recommendations with a special focus on Indian cuisine, offering 60% vegetarian and 40% non-vegetarian options.

- 🤖 **AI-Powered Insights**
  Smart algorithms deliver highly personalized fitness and diet suggestions, continuously learning and adapting to your progress.

- 🎨 **Dark-Themed, User-Friendly Interface**
  An intuitive and aesthetically pleasing dark-themed design provides a smooth and engaging user experience.

- 🛠️ **Professional Guidance**
  Access to experienced coaches and mentors for expert support and advice throughout your fitness journey.



## 💻 Technologies at Work

- **Frontend:** **React.js** for building a dynamic, responsive, and modern user interface.
- **Backend:** **Flask** for robust API management and seamless integration of AI models.
- **Machine Learning:** **Scikit-learn** powers the predictive modeling for personalized recommendations.
- **Database:** **MongoDB** for flexible and scalable storage of user profiles, fitness data, and personalized plans.
- **AI API:** **Google Generative AI** for advanced language understanding and enhanced interactive features.


## 🎯 Highlights

- **Stylish Dark Theme:** An elegant UI featuring subtle orange accents and modern typography for a premium feel.
- **Indian Cuisine Focus:** Thoughtfully curated meal plans that align with diverse cultural and dietary preferences specific to India.
- **AI-Driven Accuracy:** Leveraging data-powered intelligence to provide precise and effective personalized fitness recommendations.
- **Scalability:** Architected for growth, the platform is designed to efficiently accommodate an expanding user base and new features.


## 📂 Project Structure

The FitAi project follows a consolidated structure where both frontend (React) and backend (Flask) components reside primarily in the root directory, with dedicated folders for static assets, templates, and configurations.


```
FitAi/
├── .github/                      # GitHub configurations for issue templates and workflows
│   ├── ISSUE_TEMPLATE/           # Templates for bug reports, feature requests
│   └── workflows/                # CI/CD workflows (e.g., deploy.yml, automated messages)
├── .idea/                        # IDE (e.g., IntelliJ/PyCharm) configuration files
├── node_modules/                 # Frontend dependencies installed by npm
├── static/                       # Static assets served by the application
│   ├── css/                      # Custom CSS files
│   ├── images/                   # Application images (logos, icons, plan images)
│   └── js/                       # Frontend JavaScript files and React components
│       ├── README_WorkoutPlanCard.md # Documentation for WorkoutPlanCard
│       ├── WorkoutPlanCard.jsx   # React JSX component for workout plans
│       ├── WorkoutPlanCard.tsx   # React TypeScript component for workout plans
│       ├── WorkoutPlanCardDemo.html # HTML demo for workout plan card
│       ├── WorkoutPlanCardExample.jsx # Example usage of WorkoutPlanCard
│       └── theme.js              # Theme-related JavaScript
├── templates/                    # HTML templates served by Flask
│   ├── css/                      # CSS specific to Flask templates
│   ├── images/                   # Images specific to Flask templates
│   ├── chatbot.html              # Chatbot interface
│   ├── day1.html                 # Day 1 workout/diet plan
│   ├── day2.html                 # Day 2 workout/diet plan
│   ├── day3.html                 # Day 3 workout/diet plan
│   ├── day4.html                 # Day 4 workout/diet plan
│   ├── day5.html                 # Day 5 workout/diet plan
│   ├── day6.html                 # Day 6 workout/diet plan
│   ├── diet.html                 # Diet plan display
│   ├── diet_data.csv             # Diet data file (likely moved from root into templates, if not already)
│   ├── Home.html                 # Main landing page
│   ├── index.html                # Main application entry point (could be Flask's or a fallback)
│   ├── login.html                # User login page
│   ├── page5.html                # Generic page 5
│   ├── registration.html         # User registration page
│   ├── Sections.html             # Sections page
│   ├── sports.html               # Sports related content page
│   ├── Untitled-2.css            # Untitled CSS file
│   ├── workout_plan.html         # Workout plan display
│   └── Yoga.html                 # Yoga content page
├── pycache/                  # Python compiled bytecode cache
├── .DS_Store                     # macOS folder metadata
├── .gitignore                    # Specifies untracked files to ignore
├── .hintrc                       # Configuration for a linter/formatter
├── .vercelignore                  # Files to ignore during Vercel deployment
├── app.py                        # Main Flask application and API routes
├── app_gradio.py                 # Gradio interface for demonstration/specific features
├── DEPLOYMENT.md                 # Deployment instructions
├── diet_data.csv                 # Dataset for diet plans
├── env_template.txt              # Template for environment variables
├── exercises.csv                 # Dataset for exercises
├── fitai.jpg                     # Project-related image
├── LICENSE                       # Project licensing information
├── package-lock.json             # Records exact versions of frontend dependencies
├── package.json                  # Frontend project metadata and scripts (for React app)
├── postcss.config.js             # PostCSS configuration (e.g., for Tailwind CSS)
├── README.md                     # Main project documentation (this file)
├── README_HUGGINGFACE.md         # README specific to Hugging Face deployment
├── render.yaml                   # Render deployment configuration
├── requirements.txt              # Python dependencies for the main Flask backend
├── requirements_gradio.txt       # Python dependencies specific to the Gradio app
├── runtime.txt                   # Specifies Python runtime version for deployment
├── SECURITY.md                   # Security policy documentation
├── tailwind.config.js            # Tailwind CSS configuration
└── vercel.json                   # Vercel deployment configuration
```


## ⚙️ How to Install

Follow these steps to set up and run FitAi locally for development:

1.  **Fork the repository.**
    * Click the "Fork" button on the top right of the GitHub repository page to create a copy in your account.
2.  **Clone your forked repository:**
    ```
    git clone https://github.com/Nikhil210206/FitYou---Fit_Ai.git
    ```
3.  **Navigate to the project directory:**
    ```
    cd FitYou---Fit_Ai
    ```
4.  **Install Python dependencies for the backend:**
    ```
    pip install -r requirements.txt
    ```
5.  **Install frontend dependencies:**
    ```
    npm install
    ```
6.  **Start the backend server:**
    ```
    flask run
    # Alternatively, if 'flask' command is not globally available:
    # python app.py
    ```
7.  **Start the frontend development server:**
    ```
    npm start
    ```
    * **Note:** Given the consolidated project structure, the `npm start` command runs the React development server. It serves the frontend assets (like your React components) which are then likely integrated or proxied by the Flask backend.
    * **Important:** Ensure both the Flask backend (Step 6) and the React development server (Step 7) are running concurrently for the full application functionality.
8.  **Open in browser:**
    * Access the application by navigating to: `http://localhost:5000`
    * **Explanation:** The Flask backend, which serves as the primary web server, typically runs on port `5000` by default. Your React frontend assets are likely served through this same port once the Flask application is running and configured to handle them.


## 🛠️ Usage

-   **Sign up or Log in:** Create an account or log in to access your personalized fitness dashboard.
-   **Enter your details:** Provide information about your fitness goals, current activity level, and available equipment.
-   **Receive Plans:** Get instant access to tailored workout routines and customized diet plans.
-   **Track Progress:** Monitor your achievements and adjust your preferences to evolve your plan as needed.
-   **Connect with Experts:** Engage with experienced coaches and mentors for additional guidance and motivation.



## 🚀 Future Enhancements

-   **Wearable Device Integration:** Seamless connectivity with popular wearable devices for real-time activity tracking and data synchronization.
-   **Multi-Language Support:** Expand accessibility by offering the application in multiple languages.
-   **Gamification Features:** Introduce engaging game-like elements and challenges to enhance user motivation and engagement.
-   **Advanced Analytics Dashboard:** A comprehensive dashboard providing deeper insights into user progress, performance metrics, and health trends.


## 🤝 Contributions Welcome

We welcome contributions from the community! To contribute to FitAi, please follow these steps:

1.  **Fork the repository.**
2.  **Create a new branch for your feature or bug fix:**
    ```
    git checkout -b feature-name
    ```
3.  **Commit your changes with a clear and concise message:**
    ```
    git commit -m 'Add a feature'
    ```
4.  **Push to your branch:**
    ```
    git push origin feature-name
    ```
5.  **Open a Pull Request for review.** Please ensure your code adheres to our style guidelines and includes relevant tests.



## 📞 Contact

For any questions, suggestions, or collaborations, feel free to reach out to:

-   **Name:** Nikhil Balamurugan
-   **GitHub:** [Nikhil210206](https://github.com/Nikhil210206)
-   **Email:** nikhilbalamurugan@gmail.com


## 🙏 Acknowledgments

We extend our sincere gratitude to:

-   My incredible team and all dedicated contributors for their hard work and commitment.
-   The open-source community for providing invaluable tools and libraries that made this project possible.
-   The fitness community for their continuous inspiration and feedback.


## 📜 License

-   This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for more details.
-   This Project is under Open Source Connect India 2025
