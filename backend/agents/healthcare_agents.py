import os
import sqlite3
import logging
from typing import List, Dict, Any

# Agno/Phidata imports
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import Function

# Set up logging
logger = logging.getLogger(__name__)

# --- Configuration ---
DB_FILE = os.environ.get("DB_FILE", "/app/data/user_data.db")
LLM_MODEL = OpenAIChat(id="gpt-4o-mini", temperature=0.7)

# --- Shared Database Tool ---
class DatabaseTool(Function):
    """Manages CRUD operations for user profiles and log tables."""
    name: str = "DatabaseTool"
    description: str = "Manages user profiles and logs (mood, CGM, food). Use ONLY for data lookups and storage."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self, action: str, user_id: int = None, **kwargs) -> str:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        try:
            # --- Validation & Fetch ---
            if action == "validate_user":
                cursor.execute("SELECT first_name, city, diet_preference, medical_conditions FROM users WHERE user_id = ?", (user_id,))
                user = cursor.fetchone()
                if user:
                    return f"Valid: Name={user[0]}, City={user[1]}, Diet={user[2]}, Conditions={user[3]}"
                return "Invalid user ID."

            elif action == "get_user_profile":
                cursor.execute("SELECT first_name, diet_preference, medical_conditions FROM users WHERE user_id = ?", (user_id,))
                user = cursor.fetchone()
                return f"Profile: Diet={user[1]}, Conditions={user[2]}" if user else "User not found."

            # --- Logging ---
            elif action == "log_mood":
                cursor.execute("INSERT INTO mood_logs (user_id, mood) VALUES (?, ?)", (user_id, kwargs.get('mood')))
                conn.commit()
                return f"Mood '{kwargs.get('mood')}' logged successfully."
            
            elif action == "log_cgm":
                reading = kwargs.get('reading')
                if reading < 80 or reading > 300:
                    return f"ALERT: CGM reading {reading} is outside the standard range (80-300 mg/dL). Logged and flagged."
                cursor.execute("INSERT INTO cgm_logs (user_id, glucose_reading) VALUES (?, ?)", (user_id, reading))
                conn.commit()
                return f"CGM reading {reading} mg/dL logged successfully."

            elif action == "log_food":
                cursor.execute("INSERT INTO food_logs (user_id, meal_description) VALUES (?, ?)", (user_id, kwargs.get('meal_description')))
                conn.commit()
                return f"Meal '{kwargs.get('meal_description')}' logged successfully for nutrient categorization."

            # --- Reporting / Chart Data ---
            elif action == "get_logs":
                log_type = kwargs.get('log_type')
                limit = kwargs.get('limit', 7)
                
                if log_type == 'cgm':
                    cursor.execute(f"SELECT timestamp, glucose_reading FROM cgm_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
                elif log_type == 'mood':
                    cursor.execute(f"SELECT timestamp, mood FROM mood_logs WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
                else:
                    return f"Unknown log type: {log_type}"
                    
                logs = cursor.fetchall()
                return str(logs) # Return simple string for LLM processing
            
            else:
                return f"Unknown database action: {action}"
        except Exception as e:
            logger.error(f"Database Error: {e}")
            return f"Database operation failed due to: {e}"
        finally:
            conn.close()

# --- Agent Definitions ---

# 1. Greeting Agent (Authentication & Validation)
def get_greeting_agent(db_tool: DatabaseTool):
    return Agent(
        name="Greeting Agent",
        model=LLM_MODEL,
        tools=[db_tool],
        instructions=[
            "You are the entry point. Start by asking the user for their integer User ID.",
            "Use the DatabaseTool (action='validate_user') to verify the ID.",
            "If invalid, prompt the user to re-enter a valid ID.",
            "If valid, retrieve their name and city from the tool output. Greet them personally: 'Hello, [Name] from [City]! How can I assist you today?'",
            "After greeting, suggest main actions: Mood tracking, CGM logging, or Meal planning."
        ]
    )

# 2. Mood Tracker Agent
def get_mood_tracker_agent(db_tool: DatabaseTool):
    return Agent(
        name="Mood Tracker Agent",
        model=LLM_MODEL,
        tools=[db_tool],
        instructions=[
            "You track the user's emotional state. Ask the user for their current mood.",
            "Once received, log it using the DatabaseTool (action='log_mood').",
            "After logging, retrieve the last 7 mood logs (action='get_logs', log_type='mood', limit=7).",
            "Compute the rolling average mood (e.g., 'Your mood has been slightly lower this week').",
            "Confirm the log and provide a brief analysis. Always route the user back to the main menu."
        ]
    )

# 3. CGM Agent (Continuous Glucose Monitor)
def get_cgm_agent(db_tool: DatabaseTool):
    return Agent(
        name="CGM Agent",
        model=LLM_MODEL,
        tools=[db_tool],
        instructions=[
            "You manage glucose readings. Ask the user for their current CGM reading (an integer, mg/dL).",
            "Use the DatabaseTool (action='log_cgm') to store the reading. The tool will flag alerts if the value is outside 80-300 mg/dL.",
            "Acknowledge the reading and inform the user of any alerts flagged by the tool. Always route the user back to the main menu."
        ]
    )

# 4. Food Intake Agent (Nutrient Categorization)
def get_food_intake_agent(db_tool: DatabaseTool):
    return Agent(
        name="Food Intake Agent",
        model=LLM_MODEL,
        tools=[db_tool],
        instructions=[
            "You record meals and categorize nutrients. Ask the user for a description of their meal or snack.",
            "Log the free-text description using the DatabaseTool (action='log_food').",
            "THEN, use your LLM capabilities to analyze the meal description and categorize the nutrients into Carbs, Protein, and Fat (e.g., '1 cup oatmeal with berries' is 'High Carb, Moderate Fiber, Low Fat').",
            "Confirm the log and provide the nutrient categorization. Always route the user back to the main menu."
        ]
    )

# 5. Meal Planner Agent (Adaptive Logic)
def get_meal_planner_agent(db_tool: DatabaseTool):
    return Agent(
        name="Meal Planner Agent",
        model=LLM_MODEL,
        tools=[db_tool],
        instructions=[
            "Your goal is to generate an adaptive, 3-meal plan (Breakfast, Lunch, Dinner).",
            "1. Use DatabaseTool (action='get_user_profile') to fetch the user's diet and conditions.",
            "2. Use DatabaseTool (action='get_logs', log_type='cgm', limit=1) to get the latest glucose reading.",
            "3. **Adaptive Logic:** If the latest CGM reading is **above 250 mg/dL**, the plan MUST be **Low-Glycemic Index, low-carb** to manage blood sugar.",
            "4. The plan MUST strictly adhere to the user's dietary preference (vegetarian/vegan/non-vegetarian) and medical conditions (e.g., low-sodium for Hypertension).",
            "5. The final output must be a well-formatted list of 3 meals, including the primary macro-focus for each (e.g., 'High Protein')."
        ]
    )

# 6. Interrupt Agent (General Q&A)
def get_interrupt_agent():
    return Agent(
        name="Interrupt Agent (Q&A)",
        model=LLM_MODEL,
        instructions=[
            "You are a general assistant, always ready to answer non-contextual, unrelated questions (e.g., 'What is the capital of France?').",
            "Answer the query concisely using your general knowledge.",
            "After answering, you MUST inform the user that you are returning them to their previous task or the main menu.",
            "NEVER handle queries related to the current healthcare flow (mood, CGM, food, or planning)."
        ]
    )

# --- AgentOS Setup ---
def get_all_agents(db_tool: DatabaseTool) -> List[Agent]:
    """Returns a list of all agents for AgentOS to expose."""
    return [
        get_greeting_agent(db_tool),
        get_mood_tracker_agent(db_tool),
        get_cgm_agent(db_tool),
        get_food_intake_agent(db_tool),
        get_meal_planner_agent(db_tool),
        get_interrupt_agent() 
    ]