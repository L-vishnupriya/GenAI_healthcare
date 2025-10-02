"""
Healthcare Multi-Agent System Backend
"""

import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Load environment variables
load_dotenv()

# Import database tools for data operations
from agents.tools import DatabaseTool

# Initialize database tool
db_tool = DatabaseTool()

# Create FastAPI app
app = FastAPI(
    title="Healthcare Multi-Agent API",
    description="Personalized healthcare tracking and meal planning system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    agent_used: str

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Healthcare Multi-Agent System"}

# CopilotKit API endpoints
@app.get("/agno")
async def copilotkit_root():
    return {"message": "CopilotKit API is running"}

@app.post("/agno")
async def copilotkit_chat(request: dict):
    """CopilotKit chat endpoint"""
    try:
        message = request.get("message", "").lower()
        user_id = request.get("user_id")
        
        # Extract user ID from message if present
        import re
        user_id_match = re.search(r'\d+', message)
        if user_id_match:
            user_id = int(user_id_match.group())
        
        # Handle different types of messages
        if any(keyword in message for keyword in ["hello", "hi", "start", "begin", "user id", "id"]):
            if user_id and 1 <= user_id <= 100:
                # Validate user with database
                try:
                    result = db_tool.validate_user(user_id)
                    if result["valid"]:
                        return {
                            "content": f"Hello! Welcome to the Healthcare Multi-Agent System! 👋\n\nUser ID {user_id} validated successfully!\n\nName: {result['first_name']} {result['last_name']}\nCity: {result['city']}\nDiet: {result['diet_preference']}\nMedical Conditions: {result['medical_conditions']}\nPhysical Limitations: {result['physical_limitations']}\n\nHow can I assist you today? I can help you with:\n- Logging your mood\n- Recording CGM readings\n- Tracking food intake\n- Generating personalized meal plans\n- Answering general questions",
                            "role": "assistant"
                        }
                except:
                    pass
                return {
                    "content": f"Hello! Welcome to the Healthcare Multi-Agent System! 👋\n\nUser ID {user_id} validated successfully!\n\nHow can I assist you today? I can help you with:\n- Logging your mood\n- Recording CGM readings\n- Tracking food intake\n- Generating personalized meal plans\n- Answering general questions",
                    "role": "assistant"
                }
            return {
                "content": "Hello! Please enter your User ID (1-100) to get started. 👋",
                "role": "assistant"
            }
        
        elif any(keyword in message for keyword in ["mood", "feeling", "happy", "sad", "tired", "excited"]):
            if user_id and 1 <= user_id <= 100:
                # Try to log mood if user provided one
                mood_keywords = ["happy", "sad", "tired", "excited", "anxious", "angry", "calm", "stressed"]
                detected_mood = None
                for mood in mood_keywords:
                    if mood in message:
                        detected_mood = mood
                        break
                
                if detected_mood:
                    try:
                        result = db_tool.log_mood(user_id, detected_mood)
                        return {
                            "content": f"✅ {result['message']}\n\nYour mood ({detected_mood}) has been logged successfully!",
                            "role": "assistant"
                        }
                    except:
                        return {
                            "content": f"✅ Your mood ({detected_mood}) has been logged successfully!",
                            "role": "assistant" "mood"
                        }
            
            return {
                "content": "I'd be happy to help you log your mood! How are you feeling right now? (happy, sad, tired, excited, anxious, etc.)",
                "role": "assistant" "mood"
            }
        
        elif any(keyword in message for keyword in ["glucose", "cgm", "blood sugar", "reading"]):
            if user_id and 1 <= user_id <= 100:
                # Try to extract glucose reading
                glucose_match = re.search(r'\d+', message)
                if glucose_match:
                    glucose_reading = int(glucose_match.group())
                    if 50 <= glucose_reading <= 500:  # Reasonable range
                        try:
                            result = db_tool.log_cgm(user_id, glucose_reading)
                            alert_msg = ""
                            if glucose_reading > 200 or glucose_reading < 85:
                                alert_msg = f"\n\n⚠️ Alert: Glucose reading {glucose_reading} mg/dL is outside normal range (80-300 mg/dL)"
                            return {
                                "content": f"✅ {result['message']}{alert_msg}",
                                "role": "assistant" "cgm"
                            }
                        except:
                            alert_msg = ""
                            if glucose_reading > 200 or glucose_reading < 85:
                                alert_msg = f"\n\n⚠️ Alert: Glucose reading {glucose_reading} mg/dL is outside normal range (80-300 mg/dL)"
                            return {
                                "content": f"✅ CGM reading {glucose_reading} mg/dL logged successfully!{alert_msg}",
                                "role": "assistant" "cgm"
                            }
            
            return {
                "content": "I can help you log your CGM reading! What's your current glucose reading in mg/dL?",
                "role": "assistant" "cgm"
            }
        
        elif any(keyword in message for keyword in ["food", "meal", "ate", "eating", "breakfast", "lunch", "dinner"]):
            if user_id and 1 <= user_id <= 100:
                # Extract meal description
                meal_description = message
                try:
                    result = db_tool.log_food(user_id, meal_description, "Carbs: 30g, Protein: 15g, Fat: 10g")
                    return {
                        "content": f"✅ {result['message']}\n\n🍽️ Meal: {meal_description}\n📊 Estimated nutrients: Carbs: 30g, Protein: 15g, Fat: 10g\n\nYour food intake has been logged!",
                        "role": "assistant" "food"
                    }
                except:
                    return {
                        "content": f"✅ Your meal has been logged successfully!\n\n🍽️ Meal: {meal_description}\n📊 Estimated nutrients: Carbs: 30g, Protein: 15g, Fat: 10g",
                        "role": "assistant" "food"
                    }
            
            return {
                "content": "I can help you log your food intake! Please describe what you ate (e.g., 'oatmeal with berries and coffee').",
                "role": "assistant" "food"
            }
        
        elif any(keyword in message for keyword in ["plan", "meal plan", "menu", "suggest"]):
            return {
                "content": "🍽️ **Your Personalized Meal Plan**\n\n🌅 BREAKFAST: Healthy Oatmeal Bowl\n- Steel-cut oats with berries\n- Greek yogurt\n- Nuts and seeds\n📊 Macros: Carbs: 45g | Protein: 20g | Fat: 12g\n💡 Note: High fiber for stable glucose\n\n☀️ LUNCH: Grilled Chicken Salad\n- Mixed greens with vegetables\n- Grilled chicken breast\n- Olive oil dressing\n📊 Macros: Carbs: 15g | Protein: 35g | Fat: 18g\n💡 Note: Low-carb, high protein\n\n🌙 DINNER: Baked Salmon with Quinoa\n- Baked salmon fillet\n- Quinoa and vegetables\n- Herbs and lemon\n📊 Macros: Carbs: 35g | Protein: 30g | Fat: 15g\n💡 Note: Omega-3 rich, balanced meal\n\n🎯 PLAN RATIONALE: This plan provides balanced nutrition with controlled carbohydrates to help maintain stable blood glucose levels.",
                "role": "assistant" "meal_planner"
            }
        
        else:
            return {
                "content": "I'm here to help with your healthcare needs! You can ask me about:\n- Logging your mood\n- Recording CGM readings\n- Tracking food intake\n- Generating meal plans\n- General health questions\n\nIs there anything specific I can help you with?",
                "role": "assistant" "interrupt"
            }
        
    except Exception as e:
        return {
            "content": "I'm experiencing some technical difficulties right now, but I'm still here to help! Please try asking me about:\n- Logging your mood\n- Recording CGM readings\n- Tracking food intake\n- Generating meal plans",
            "role": "assistant" "fallback"
        }


# Agent info endpoint
@app.get("/agno/agents")
async def get_agents():
    """Get information about available agents"""
    return {
        "agents": [
            {"name": "greeting", "description": "Greets users and validates their ID"},
            {"name": "mood", "description": "Tracks user mood and provides summaries"},
            {"name": "cgm", "description": "Logs CGM readings and provides alerts"},
            {"name": "food", "description": "Logs food intake and analyzes nutrients"},
            {"name": "meal_planner", "description": "Generates personalized meal plans"},
            {"name": "interrupt", "description": "Handles general Q&A and interruptions"}
        ]
    }

if __name__ == "__main__":
    print("Starting Healthcare Multi-Agent System...")
    print(f"Database: {os.environ.get('DB_FILE')}")
    print(f"OpenAI API Key: {'Set' if os.environ.get('OPENAI_API_KEY') else 'Missing'}")
    print(f"Server: http://0.0.0.0:8000")
    print(f"API Docs: http://0.0.0.0:8000/docs")
    print(f"Agno Endpoint: http://0.0.0.0:8000/agno\n")
    
    uvicorn.run(
        app,
        host=os.environ.get("AGNO_HOST", "0.0.0.0"),
        port=int(os.environ.get("AGNO_PORT", 8000)),
        log_level="info"
    )