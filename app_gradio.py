import gradio as gr
import pandas as pd
import random
import os

# Import your existing fitness logic
from app import chat_with_fitness_ai, WorkoutPlanner, DietPlanner

def fitness_chat_interface(message, history):
    """Gradio interface for fitness AI chat"""
    response = chat_with_fitness_ai(message)
    return response

def generate_workout_plan(age, weight, height, goal, experience, equipment):
    """Generate workout plan using existing logic"""
    try:
        planner = WorkoutPlanner(
            age=int(age),
            weight=float(weight), 
            height=float(height),
            goal=goal.lower(),
            experience_level=experience.lower(),
            available_equipment=equipment.lower()
        )
        
        workout_plan = planner.generate_workout_plan()
        
        # Format the workout plan for display
        formatted_plan = ""
        for day, exercises in workout_plan.items():
            formatted_plan += f"**{day}:**\n"
            if isinstance(exercises, list):
                for exercise in exercises:
                    formatted_plan += f"• {exercise}\n"
            else:
                formatted_plan += f"• {exercises}\n"
            formatted_plan += "\n"
        
        return formatted_plan
    except Exception as e:
        return f"Error generating workout plan: {str(e)}"

def generate_diet_plan(age, weight, height, goal, diet_type):
    """Generate diet plan using existing logic"""
    try:
        planner = DietPlanner(
            age=int(age),
            weight=float(weight),
            height=float(height), 
            goal=goal.lower(),
            diet_type=diet_type.lower()
        )
        
        diet_plan = planner.generate_diet_plan()
        
        # Format the diet plan for display
        formatted_plan = ""
        for day, meals in diet_plan.items():
            formatted_plan += f"**{day}:**\n"
            if isinstance(meals, dict):
                for meal_type, meal_desc in meals.items():
                    formatted_plan += f"• **{meal_type}**: {meal_desc}\n"
            else:
                formatted_plan += f"• {meals}\n"
            formatted_plan += "\n"
        
        return formatted_plan
    except Exception as e:
        return f"Error generating diet plan: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="FitAI: Your AI Fitness Companion", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏋️ FitAI: Your AI Fitness Companion")
    gr.Markdown("Get personalized workout plans, diet recommendations, and fitness advice!")
    
    with gr.Tabs():
        # AI Chat Tab
        with gr.TabItem("💬 AI Fitness Coach"):
            gr.Markdown("Chat with your AI fitness coach for personalized advice!")
            
            chatbot = gr.Chatbot(height=400)
            msg = gr.Textbox(
                placeholder="Ask me about workouts, nutrition, motivation, or any fitness question...",
                label="Your Question"
            )
            
            def respond(message, chat_history):
                response = chat_with_fitness_ai(message)
                chat_history.append((message, response))
                return "", chat_history
            
            msg.submit(respond, [msg, chatbot], [msg, chatbot])
        
        # Workout Planner Tab
        with gr.TabItem("🏋️ Workout Planner"):
            gr.Markdown("Generate a personalized workout plan based on your profile!")
            
            with gr.Row():
                with gr.Column():
                    age_input = gr.Number(label="Age", value=25, minimum=16, maximum=100)
                    weight_input = gr.Number(label="Weight (kg)", value=70, minimum=30, maximum=200)
                    height_input = gr.Number(label="Height (cm)", value=170, minimum=120, maximum=250)
                
                with gr.Column():
                    goal_input = gr.Dropdown(
                        choices=["Weight Loss", "Muscle Gain", "Maintenance"],
                        label="Fitness Goal",
                        value="Maintenance"
                    )
                    experience_input = gr.Dropdown(
                        choices=["Beginner", "Intermediate", "Advanced"],
                        label="Experience Level",
                        value="Beginner"
                    )
                    equipment_input = gr.Dropdown(
                        choices=["Home", "Gym", "Minimal"],
                        label="Available Equipment",
                        value="Home"
                    )
            
            workout_btn = gr.Button("Generate Workout Plan", variant="primary")
            workout_output = gr.Markdown()
            
            workout_btn.click(
                generate_workout_plan,
                inputs=[age_input, weight_input, height_input, goal_input, experience_input, equipment_input],
                outputs=workout_output
            )
        
        # Diet Planner Tab
        with gr.TabItem("🥗 Diet Planner"):
            gr.Markdown("Get a personalized diet plan tailored to your goals!")
            
            with gr.Row():
                with gr.Column():
                    diet_age = gr.Number(label="Age", value=25, minimum=16, maximum=100)
                    diet_weight = gr.Number(label="Weight (kg)", value=70, minimum=30, maximum=200)
                    diet_height = gr.Number(label="Height (cm)", value=170, minimum=120, maximum=250)
                
                with gr.Column():
                    diet_goal = gr.Dropdown(
                        choices=["Weight Loss", "Weight Gain", "Maintenance"],
                        label="Diet Goal",
                        value="Maintenance"
                    )
                    diet_type = gr.Dropdown(
                        choices=["Vegetarian", "Non-Vegetarian", "Vegan"],
                        label="Diet Type",
                        value="Vegetarian"
                    )
            
            diet_btn = gr.Button("Generate Diet Plan", variant="primary")
            diet_output = gr.Markdown()
            
            diet_btn.click(
                generate_diet_plan,
                inputs=[diet_age, diet_weight, diet_height, diet_goal, diet_type],
                outputs=diet_output
            )

if __name__ == "__main__":
    demo.launch()