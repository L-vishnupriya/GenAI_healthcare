import os
import uvicorn
from fastapi import FastAPI
from agno.os import AgentOS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import helper functions
from agents.healthcare_agents import DatabaseTool, get_all_agents

# --- 1. Setup Data and Tools ---
db_tool = DatabaseTool()
AGENTS = get_all_agents(db_tool)

# --- 2. Initialize AgentOS ---
# AgentOS automatically creates a FastAPI app with the /agno endpoint, 
# making it AG-UI compliant for CopilotKit.
agent_os = AgentOS(
    name="Personalized Healthcare Demo",
    description="A multi-agent system for personalized health tracking and adaptive meal planning.",
    agents=AGENTS,
)

# Get the FastAPI app from AgentOS
app = agent_os.get_app()

# Add a simple health endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Healthcare Backend"}

if __name__ == "__main__":
    # Ensure data is generated if not running via docker-compose (which handles volumes)
    try:
        if not os.path.exists(os.environ.get("DB_FILE")):
            import subprocess
            print("Database not found. Generating initial synthetic data...")
            subprocess.run(["python", "data_generator.py"], check=True)
    except Exception as e:
        print(f"Error generating data: {e}")

    # Start the FastAPI/AgentOS server
    uvicorn.run(
        app, 
        host=os.environ.get("AGNO_HOST", "0.0.0.0"), 
        port=int(os.environ.get("AGNO_PORT", 8000))
    )