import sqlite3
import os
import random
from faker import Faker

# --- CONFIG ---
DB_FILE = os.environ.get("DB_FILE", "./data/user_data.db")
NUM_USERS = 100
CITIES = ["New York", "London", "Tokyo", "Bangalore", "Sydney", "Berlin", "Toronto"]
DIETS = ["vegetarian", "non-vegetarian", "vegan"]
MEDICAL_CONDITIONS = ["Type 2 Diabetes", "Hypertension", "Celiac Disease", "None", "Mobility Issues"]
CGM_RANGES = {
    "Type 2 Diabetes": (100, 250),
    "Hypertension": (80, 150),
    "None": (80, 120),
}
MOODS = ["happy", "sad", "excited", "tired", "calm", "stressed"]

def generate_synthetic_data():
    """Generates 100 synthetic user records and their initial log tables."""
    print(f"Connecting to database: {DB_FILE}")
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    fake = Faker()

    # --- 1. Create Tables ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            city TEXT,
            diet_preference TEXT,
            medical_conditions TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood_logs (
            log_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            mood TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cgm_logs (
            log_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            glucose_reading INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_logs (
            log_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            meal_description TEXT,
            nutrients TEXT
        )
    """)

    # --- 2. Insert User Data ---
    user_data = []
    for i in range(1, NUM_USERS + 1):
        diet = DIETS[i % len(DIETS)] 
        
        # Ensure realistic condition distribution
        conditions = random.sample(MEDICAL_CONDITIONS, k=random.randint(1, 2))
        if i % 10 == 0 and "Type 2 Diabetes" not in conditions: conditions.append("Type 2 Diabetes")
        
        conditions = [c for c in set(conditions) if c != "None" or len(conditions) == 1]
        
        user_data.append((
            i,
            fake.first_name(),
            fake.last_name(),
            random.choice(CITIES),
            diet,
            ", ".join(conditions)
        ))

    cursor.executemany("""
        INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)
    """, user_data)
    
    # --- 3. Insert Mock Initial Logs (for Chart Demo) ---
    for i in range(1, NUM_USERS + 1):
        # Create 7 mock CGM logs for the first 10 users
        if i <= 10:
            for day in range(7, 0, -1):
                # Simulate a range based on assumed medical conditions (simplification)
                user_conditions = user_data[i-1][5]
                base_range = CGM_RANGES.get("None")
                if "Type 2 Diabetes" in user_conditions:
                    base_range = CGM_RANGES["Type 2 Diabetes"]
                
                reading = random.randint(base_range[0], base_range[1] + random.randint(0, 50))
                
                cursor.execute("INSERT INTO cgm_logs (user_id, timestamp, glucose_reading) VALUES (?, datetime('now', ?), ?)", 
                               (i, f'-{day} days', reading))
                cursor.execute("INSERT INTO mood_logs (user_id, timestamp, mood) VALUES (?, datetime('now', ?), ?)", 
                               (i, f'-{day} days', random.choice(MOODS)))
                
    conn.commit()
    conn.close()
    print(f"Successfully generated {NUM_USERS} user records and initial logs in {DB_FILE}")

if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE) 
    generate_synthetic_data()