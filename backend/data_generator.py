"""
Synthetic Healthcare Data Generator
Generates 100 user profiles with medical conditions and dietary preferences
"""

import sqlite3
import os
import random
from faker import Faker

# Configuration
DB_FILE = os.environ.get("DB_FILE", "./data/user_data.db")
NUM_USERS = 100

# Data distributions
CITIES = ["New York", "London", "Tokyo", "Bangalore", "Sydney", "Toronto", "Berlin", "Singapore"]
DIETS = ["vegetarian", "non-vegetarian", "vegan"]
MEDICAL_CONDITIONS = [
    "Type 2 Diabetes", 
    "Hypertension", 
    "Celiac Disease", 
    "Heart Disease",
    "High Cholesterol",
    "None"
]
PHYSICAL_LIMITATIONS = [
    "None",
    "Mobility issues",
    "Swallowing difficulties",
    "Visual impairment",
    "Hearing impairment"
]

def generate_synthetic_data():
    """Generate synthetic healthcare data for 100 users"""
    
    print(f"📊 Generating synthetic data...")
    print(f"Database location: {DB_FILE}")
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    fake = Faker()

    # Create USERS table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city TEXT NOT NULL,
            diet_preference TEXT NOT NULL,
            medical_conditions TEXT,
            physical_limitations TEXT
        )
    """)

    # Create LOG tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mood_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            mood TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cgm_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            glucose_reading INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            meal_description TEXT NOT NULL,
            nutrients TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)

    # Generate user data
    user_data = []
    for i in range(1, NUM_USERS + 1):
        # Ensure even distribution of diets
        diet = DIETS[(i - 1) % len(DIETS)]
        
        # Randomly assign 1-2 medical conditions
        num_conditions = random.randint(1, 2)
        conditions = random.sample(MEDICAL_CONDITIONS, k=num_conditions)
        
        # Ensure Type 2 Diabetes is present in ~20% of users
        if i % 5 == 0 and "Type 2 Diabetes" not in conditions:
            conditions[0] = "Type 2 Diabetes"
        
        # Remove duplicates and handle "None"
        if "None" in conditions and len(conditions) > 1:
            conditions.remove("None")
        
        # Physical limitations
        limitations = random.choice(PHYSICAL_LIMITATIONS)
        
        user_data.append((
            i,
            fake.first_name(),
            fake.last_name(),
            random.choice(CITIES),
            diet,
            ", ".join(conditions),
            limitations
        ))

    # Insert data
    cursor.executemany("""
        INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)
    """, user_data)

    # Commit and close
    conn.commit()
    
    # Verify data
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    
    print(f"✅ Successfully generated {count} user records")
    print(f"📍 Cities: {', '.join(CITIES[:5])}...")
    print(f"🍽️  Diets: {', '.join(DIETS)}")
    print(f"💊 Medical conditions: {len(MEDICAL_CONDITIONS)} types")
    print(f"♿ Physical limitations: {len(PHYSICAL_LIMITATIONS)} types")
    
    conn.close()

if __name__ == "__main__":
    # Clean slate
    if os.path.exists(DB_FILE):
        print(f"🗑️  Removing existing database...")
        os.remove(DB_FILE)
    
    generate_synthetic_data()
    print(f"✅ Data generation complete!\n")