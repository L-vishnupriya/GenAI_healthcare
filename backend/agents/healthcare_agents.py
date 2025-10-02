"""
Healthcare Agent Definitions
"""

import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from .tools import DatabaseTool

# Configuration - Use Groq for faster responses
LLM_MODEL = "llama-3.1-70b-versatile"  # Groq model
db_tool = DatabaseTool()

def get_greeting_agent() -> Agent:
    """Agent that greets users and validates their ID"""
    
    def validate_and_greet(user_id: int) -> str:
        """Validate user ID and return greeting"""
        result = db_tool.validate_user(user_id)
        
        if result["valid"]:
            return f"""User validated successfully!
            
Name: {result['first_name']} {result['last_name']}
City: {result['city']}
Diet: {result['diet_preference']}
Medical Conditions: {result['medical_conditions']}
Physical Limitations: {result['physical_limitations']}

Hello, {result['first_name']} from {result['city']}! 👋

How can I assist you today? I can help you with:
- Logging your mood
- Recording CGM readings
- Tracking food intake
- Generating personalized meal plans
- Answering general questions"""
        else:
            return "❌ Invalid User ID. Please enter a valid ID between 1 and 100."
    
    return Agent(
        name="Greeting Agent",
        model=OpenAIChat(
            id=LLM_MODEL,
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        ),
        tools=[validate_and_greet],
        instructions=[
            "You are a friendly healthcare assistant.",
            "Your first task is to ask the user for their User ID (1-100).",
            "Once you receive a user ID, call the validate_and_greet function.",
            "If the ID is invalid, politely ask them to try again.",
            "If valid, show the greeting message and ask how you can help.",
        ],
        markdown=True
    )

def get_mood_tracker_agent() -> Agent:
    """Agent that tracks user mood"""
    
    def log_mood_function(user_id: int, mood: str) -> str:
        """Log mood and calculate summary"""
        result = db_tool.log_mood(user_id, mood)
        logs = db_tool.get_mood_logs(user_id, limit=7)
        
        # Calculate mood frequency
        mood_counts = {}
        for log in logs:
            m = log["mood"]
            mood_counts[m] = mood_counts.get(m, 0) + 1
        
        summary = "\n".join([f"• {m}: {c} time(s)" for m, c in mood_counts.items()])
        
        return f"""✅ {result['message']}

📊 Your 7-day mood summary:
{summary}

Your mood has been logged successfully!"""
    
    return Agent(
        name="Mood Tracker Agent",
        model=OpenAIChat(
            id=LLM_MODEL,
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        ),
        tools=[log_mood_function],
        instructions=[
            "You help users log their mood.",
            "Ask the user: 'How are you feeling right now?' (happy, sad, tired, excited, anxious, etc.)",
            "Once they provide their mood, call log_mood_function with their user_id and mood.",
            "After logging, show them the 7-day summary.",
            "Be empathetic and supportive in your responses.",
        ],
        markdown=True
    )

def get_cgm_agent() -> Agent:
    """Agent that logs CGM readings"""
    
    def log_cgm_function(user_id: int, glucose_reading: int) -> str:
        """Log CGM reading"""
        result = db_tool.log_cgm(user_id, glucose_reading)
        
        message = f"""✅ {result['message']}"""
        
        if result.get("alert"):
            message += f"\n\n{result['alert']}"
        
        # Get recent readings
        logs = db_tool.get_cgm_logs(user_id, limit=7)
        if logs:
            avg = sum(log["glucose"] for log in logs) / len(logs)
            message += f"\n\n📊 7-day average: {avg:.1f} mg/dL"
        
        return message
    
    return Agent(
        name="CGM Agent",
        model=OpenAIChat(
            id=LLM_MODEL,
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        ),
        tools=[log_cgm_function],
        instructions=[
            "You help users log their Continuous Glucose Monitor (CGM) readings.",
            "Ask for their current glucose reading in mg/dL.",
            "Normal range is 80-300 mg/dL.",
            "Call log_cgm_function with user_id and glucose_reading.",
            "If the reading is outside the normal range, acknowledge the alert.",
            "Provide the 7-day average if available.",
        ],
        markdown=True
    )

def get_food_intake_agent() -> Agent:
    """Agent that logs food intake and categorizes nutrients"""
    
    def log_food_function(user_id: int, meal_description: str) -> str:
        """Log food and categorize nutrients using LLM"""
        
        # Use LLM to categorize nutrients
        from openai import OpenAI
        client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a nutrition expert. Analyze the meal and estimate macronutrients. Respond ONLY with format: 'Carbs: Xg, Protein: Yg, Fat: Zg'"},
                {"role": "user", "content": f"Analyze this meal: {meal_description}"}
            ],
            max_tokens=50
        )
        
        nutrients = response.choices[0].message.content.strip()
        
        # Log to database
        result = db_tool.log_food(user_id, meal_description, nutrients)
        
        return f"""✅ {result['message']}

🍽️ Meal: {meal_description}
📊 Estimated nutrients: {nutrients}

Your food intake has been logged!"""
    
    return Agent(
        name="Food Intake Agent",
        model=OpenAIChat(
            id=LLM_MODEL,
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        ),
        tools=[log_food_function],
        instructions=[
            "You help users log their food intake.",
            "Ask them to describe what they ate (e.g., 'oatmeal with berries and coffee').",
            "Call log_food_function to log the meal and get nutrient analysis.",
            "Show the meal description and estimated macronutrients.",
            "Be encouraging and supportive about their food choices.",
        ],
        markdown=True
    )

def get_meal_planner_agent() -> Agent:
    """Agent that generates adaptive meal plans"""
    
    def generate_meal_plan(user_id: int) -> str:
        """Generate adaptive 3-meal plan"""
        
        # Get user profile
        user = db_tool.validate_user(user_id)
        
        # Get latest CGM reading
        cgm_logs = db_tool.get_cgm_logs(user_id, limit=1)
        latest_cgm = cgm_logs[0]["glucose"] if cgm_logs else None
        
        # Get recent moods
        mood_logs = db_tool.get_mood_logs(user_id, limit=3)
        recent_moods = [log["mood"] for log in mood_logs] if mood_logs else []
        
        # Create adaptive prompt
        from openai import OpenAI
        client = OpenAI(
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        
        prompt = f"""Generate a personalized 3-meal plan for today.

User Profile:
- Diet: {user['diet_preference']}
- Medical Conditions: {user['medical_conditions']}
- Physical Limitations: {user['physical_limitations']}
- Latest CGM: {latest_cgm} mg/dL (Normal: 80-300)
- Recent Moods: {', '.join(recent_moods) if recent_moods else 'No data'}

IMPORTANT ADAPTIVE RULES:
1. If CGM > 200 or < 85: Prioritize LOW-CARB, HIGH-FIBER meals to stabilize glucose
2. If "Type 2 Diabetes" in conditions: All meals must be diabetes-friendly (low GI, high fiber)
3. If "Celiac Disease": Must be gluten-free
4. If physical limitations include swallowing difficulties: Recommend soft, easy-to-swallow foods
5. Respect diet preference (vegetarian/vegan/non-vegetarian)

Format your response EXACTLY as:

🌅 BREAKFAST: [Meal Name]
- [Item 1]
- [Item 2]
- [Item 3]
📊 Macros: Carbs: Xg | Protein: Yg | Fat: Zg
💡 Note: [Why this meal is appropriate]

☀️ LUNCH: [Meal Name]
- [Item 1]
- [Item 2]
- [Item 3]
📊 Macros: Carbs: Xg | Protein: Yg | Fat: Zg
💡 Note: [Why this meal is appropriate]

🌙 DINNER: [Meal Name]
- [Item 1]
- [Item 2]
- [Item 3]
📊 Macros: Carbs: Xg | Protein: Yg | Fat: Zg
💡 Note: [Why this meal is appropriate]

🎯 PLAN RATIONALE:
[1-2 sentences explaining why this plan is adaptive to their current health status]"""

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert nutritionist and meal planner."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        
        meal_plan = response.choices[0].message.content
        
        return f"""🍽️ **Your Personalized Meal Plan**

{meal_plan}

---
✅ This plan has been generated based on your current health data and will help you achieve your wellness goals!"""
    
    return Agent(
        name="Meal Planner Agent",
        model=OpenAIChat(
            id=LLM_MODEL,
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        ),
        tools=[generate_meal_plan],
        instructions=[
            "You are a personalized meal planning assistant.",
            "When a user asks for a meal plan, call generate_meal_plan with their user_id.",
            "The function will create an adaptive plan based on their:",
            "  - Dietary preferences",
            "  - Medical conditions",
            "  - Latest CGM reading",
            "  - Recent mood trends",
            "  - Physical limitations",
            "Present the meal plan in a clear, organized format.",
            "Explain why the plan is appropriate for their specific needs.",
        ],
        markdown=True
    )

def get_interrupt_agent() -> Agent:
    """Agent that handles general Q&A and interruptions"""
    
    return Agent(
        name="Interrupt Agent",
        model=OpenAIChat(
            id=LLM_MODEL,
            api_key=os.environ.get("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        ),
        instructions=[
            "You are a general knowledge assistant.",
            "You can answer ANY question the user asks, even if unrelated to healthcare.",
            "After answering, ALWAYS say: 'Is there anything else related to your health tracking I can help you with?'",
            "Be concise but informative.",
            "If the question IS related to health tracking (mood, CGM, food, meals), redirect to the appropriate agent.",
        ],
        markdown=True
    )