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

We welcome contributions from the community! To contribute to FitAi, please follow these steps to ensure a smooth and conflict-free process:

1.  **Fork the repository.**
    * Click the "Fork" button on the top right of the [FitAi GitHub repository](https://github.com/Nikhil210206/FitAi.git) 

2.  **Clone your forked repository locally:**
    ```
    git clone https://github.com/your-username/FitAi.git
    cd FitAi
    ```
    *Replace `your-username` with your actual GitHub username.*

3.  **Add the upstream remote:**
    * This step links your local repository to the original FitAi repository, allowing you to fetch updates.
    ```
    git remote add upstream https://github.com/Nikhil210206/FitAi.git
    ```

4.  **Fetch the latest changes from the upstream `main` branch:**
    * Before starting any work, always synchronize your local `main` branch with the upstream `main` to get the most recent updates and avoid merge conflicts.
    ```
    git fetch upstream
    ```

5.  **Merge upstream changes into your local `main` branch:**
    ```
    git checkout main
    git merge upstream/main
    ```
    * This ensures your local `main` is up-to-date.

6.  **Create a new branch for your feature or bug fix:**
    * Always work on a new branch, giving it a descriptive name (e.g., `feature/add-dark-mode`, `bugfix/fix-login-issue`).
    ```
    git checkout -b feature-name
    ```

7.  **Make your changes according to the issue assigned to you.**
    * Implement your feature or bug fix. Ensure your code follows the project's coding standards and includes necessary tests.

8.  **Commit your changes with a clear and concise message:**
    * Use a descriptive commit message that explains what changes were made.
    ```
    git commit -m 'feat: Add new feature'
    # Example for a bug fix:
    # git commit -m 'fix: Resolve login authentication issue'
    ```

9.  **Push your branch to your forked repository on GitHub (and set upstream):**
    * This command pushes your local `feature-name` branch to your `origin` remote (your forked repository) and sets it up to track that remote branch. This means that from now on, you can simply use `git push` and `git pull` without specifying the remote and branch name for this particular branch.
    ```
    git push -u origin feature-name
    ```
    * After this first push, subsequent pushes from this branch can simply be `git push`.

10. **Open a Pull Request (PR) for review:**
    * Go to your forked repository on GitHub.
    * You will see a "Compare & pull request" button next to your newly pushed branch. Click it.
    * Provide a clear title and detailed description of your changes, referencing the issue number it addresses (e.g., "Fixes #123").
    * Ensure your code adheres to our style guidelines and includes relevant tests.
   

## 💥 Resolving Merge Conflicts 

Merge conflicts happen when Git can't automatically reconcile changes between two branches. Here's how to resolve them concisely:

1.  **Sync with Latest `main`:**
    * Ensure your local `main` branch is up-to-date, then merge it into your feature branch.
    ```bash
    git checkout main
    git pull upstream main # Or git pull origin main
    git checkout feature-name
    git merge main
    ```
    *This step will likely trigger the conflict.*

2.  **Edit Conflicting Files:**
    * Open files flagged by Git. Manually edit sections marked by `<<<<<<<`, `=======`, and `>>>>>>>` to combine the desired changes.
    * **Remove all conflict markers** after resolution.

3.  **Stage Changes:**
    * After resolving each file, stage it:
    ```
    git add .
    ```

4.  **Commit Merge:**
    * Git will provide a default merge commit message. Review and save it.
    ```
    git commit
    ```

5.  **Push Resolved Branch:**
    * Push your updated, conflict-free feature branch:
    ```
    git push origin feature-name
    ```



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
