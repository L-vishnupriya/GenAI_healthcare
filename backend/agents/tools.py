"""
Custom Tools for Healthcare Agents
"""

import sqlite3
import os
from typing import Optional
from datetime import datetime

DB_FILE = os.environ.get("DB_FILE", "/app/data/user_data.db")

class DatabaseTool:
    """Tool for database operations"""
    
    def __init__(self):
        self.db_file = DB_FILE
    
    def validate_user(self, user_id: int) -> dict:
        """Validate user ID and return user data"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT first_name, last_name, city, diet_preference, 
                   medical_conditions, physical_limitations 
            FROM users WHERE user_id = ?
        """, (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "valid": True,
                "first_name": result[0],
                "last_name": result[1],
                "city": result[2],
                "diet_preference": result[3],
                "medical_conditions": result[4],
                "physical_limitations": result[5]
            }
        return {"valid": False}
    
    def log_mood(self, user_id: int, mood: str) -> dict:
        """Log user mood"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO mood_logs (user_id, mood) VALUES (?, ?)
        """, (user_id, mood))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": f"Mood '{mood}' logged successfully"}
    
    def log_cgm(self, user_id: int, glucose_reading: int) -> dict:
        """Log CGM reading"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Validate range
        if glucose_reading < 80 or glucose_reading > 300:
            alert = "⚠️ ALERT: Glucose reading outside normal range (80-300 mg/dL)"
        else:
            alert = None
        
        cursor.execute("""
            INSERT INTO cgm_logs (user_id, glucose_reading) VALUES (?, ?)
        """, (user_id, glucose_reading))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True, 
            "message": f"CGM reading {glucose_reading} mg/dL logged",
            "alert": alert
        }
    
    def log_food(self, user_id: int, meal_description: str, nutrients: Optional[str] = None) -> dict:
        """Log food intake"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO food_logs (user_id, meal_description, nutrients) 
            VALUES (?, ?, ?)
        """, (user_id, meal_description, nutrients))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": "Food intake logged successfully"}
    
    def get_mood_logs(self, user_id: int, limit: int = 7) -> list:
        """Get recent mood logs"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, mood FROM mood_logs 
            WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT ?
        """, (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{"timestamp": r[0], "mood": r[1]} for r in results]
    
    def get_cgm_logs(self, user_id: int, limit: int = 7) -> list:
        """Get recent CGM logs"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, glucose_reading FROM cgm_logs 
            WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT ?
        """, (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{"timestamp": r[0], "glucose": r[1]} for r in results]
    
    def get_food_logs(self, user_id: int, limit: int = 7) -> list:
        """Get recent food logs"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, meal_description, nutrients FROM food_logs 
            WHERE user_id = ? 
            ORDER BY timestamp DESC LIMIT ?
        """, (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{"timestamp": r[0], "meal": r[1], "nutrients": r[2]} for r in results]