"""
Database module for user authentication and meal tracking
Uses SQLite for persistent storage
"""
import sqlite3
import hashlib
import json
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class FoodTrackerDB:
    """Database handler for Food Tracker application"""
    
    def __init__(self, db_path="data/foodtracker.db"):
        """Initialize database connection"""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(str(self.db_path))
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Meals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                food_name TEXT NOT NULL,
                calories REAL NOT NULL,
                protein REAL DEFAULT 0,
                fat REAL DEFAULT 0,
                carbs REAL DEFAULT 0,
                fiber REAL DEFAULT 0,
                meal_type TEXT DEFAULT 'other',
                meal_date DATE NOT NULL,
                meal_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER PRIMARY KEY,
                daily_calorie_goal INTEGER DEFAULT 2000,
                daily_protein_goal INTEGER DEFAULT 50,
                daily_fat_goal INTEGER DEFAULT 65,
                daily_carbs_goal INTEGER DEFAULT 300,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        conn.commit()
        
        # Create default admin user if not exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        if cursor.fetchone()[0] == 0:
            self.create_user('admin', 'admin123', 'Administrator', 'admin@foodtracker.com')
            logger.info("Default admin user created")
        
        conn.close()
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password, name, email):
        """Create new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute('''
                INSERT INTO users (username, password_hash, name, email)
                VALUES (?, ?, ?, ?)
            ''', (username, password_hash, name, email))
            
            user_id = cursor.lastrowid
            
            # Create default preferences
            cursor.execute('''
                INSERT INTO user_preferences (user_id)
                VALUES (?)
            ''', (user_id,))
            
            conn.commit()
            conn.close()
            return True, "User created successfully"
        except sqlite3.IntegrityError:
            return False, "Username already exists"
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False, str(e)
    
    def authenticate_user(self, username, password):
        """Authenticate user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute('''
                SELECT id, username, name, email
                FROM users
                WHERE username = ? AND password_hash = ?
            ''', (username, password_hash))
            
            user = cursor.fetchone()
            
            if user:
                # Update last login
                cursor.execute('''
                    UPDATE users
                    SET last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (user[0],))
                conn.commit()
                
                user_data = {
                    'id': user[0],
                    'username': user[1],
                    'name': user[2],
                    'email': user[3]
                }
                conn.close()
                return True, user_data
            
            conn.close()
            return False, None
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            return False, None
    
    def add_meal(self, user_id, food_name, calories, nutrition, meal_type='other', meal_date=None):
        """Add meal to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if meal_date is None:
                meal_date = datetime.now().date()
            
            cursor.execute('''
                INSERT INTO meals (user_id, food_name, calories, protein, fat, carbs, fiber, meal_type, meal_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id, food_name, calories,
                nutrition.get('protein', 0),
                nutrition.get('fat', 0),
                nutrition.get('carbs', 0),
                nutrition.get('fiber', 0),
                meal_type, meal_date
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error adding meal: {e}")
            return False
    
    def get_daily_meals(self, user_id, date=None):
        """Get all meals for a specific date"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if date is None:
                date = datetime.now().date()
            
            cursor.execute('''
                SELECT id, food_name, calories, protein, fat, carbs, fiber, meal_type, meal_time
                FROM meals
                WHERE user_id = ? AND meal_date = ?
                ORDER BY meal_time DESC
            ''', (user_id, date))
            
            meals = []
            for row in cursor.fetchall():
                meals.append({
                    'id': row[0],
                    'food_name': row[1],
                    'calories': row[2],
                    'protein': row[3],
                    'fat': row[4],
                    'carbs': row[5],
                    'fiber': row[6],
                    'meal_type': row[7],
                    'meal_time': row[8]
                })
            
            conn.close()
            return meals
        except Exception as e:
            logger.error(f"Error getting daily meals: {e}")
            return []
    
    def get_daily_summary(self, user_id, date=None):
        """Get daily nutrition summary"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if date is None:
                date = datetime.now().date()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as meal_count,
                    SUM(calories) as total_calories,
                    SUM(protein) as total_protein,
                    SUM(fat) as total_fat,
                    SUM(carbs) as total_carbs,
                    SUM(fiber) as total_fiber
                FROM meals
                WHERE user_id = ? AND meal_date = ?
            ''', (user_id, date))
            
            row = cursor.fetchone()
            
            summary = {
                'total_meals': row[0] or 0,
                'total_calories': row[1] or 0,
                'nutrition': {
                    'protein': row[2] or 0,
                    'fat': row[3] or 0,
                    'carbs': row[4] or 0,
                    'fiber': row[5] or 0
                }
            }
            
            conn.close()
            return summary
        except Exception as e:
            logger.error(f"Error getting daily summary: {e}")
            return {
                'total_meals': 0,
                'total_calories': 0,
                'nutrition': {'protein': 0, 'fat': 0, 'carbs': 0, 'fiber': 0}
            }
    
    def get_meal_breakdown(self, user_id, date=None):
        """Get meal breakdown by type"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if date is None:
                date = datetime.now().date()
            
            cursor.execute('''
                SELECT 
                    meal_type,
                    COUNT(*) as count,
                    SUM(calories) as total_calories
                FROM meals
                WHERE user_id = ? AND meal_date = ?
                GROUP BY meal_type
            ''', (user_id, date))
            
            breakdown = {}
            for row in cursor.fetchall():
                breakdown[row[0]] = {
                    'count': row[1],
                    'calories': row[2]
                }
            
            conn.close()
            return breakdown
        except Exception as e:
            logger.error(f"Error getting meal breakdown: {e}")
            return {}
    
    def delete_meal(self, meal_id, user_id):
        """Delete a meal"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM meals
                WHERE id = ? AND user_id = ?
            ''', (meal_id, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error deleting meal: {e}")
            return False
    
    def reset_daily_meals(self, user_id, date=None):
        """Reset all meals for a specific date"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if date is None:
                date = datetime.now().date()
            
            cursor.execute('''
                DELETE FROM meals
                WHERE user_id = ? AND meal_date = ?
            ''', (user_id, date))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error resetting daily meals: {e}")
            return False
    
    def get_user_preferences(self, user_id):
        """Get user preferences"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT daily_calorie_goal, daily_protein_goal, daily_fat_goal, daily_carbs_goal
                FROM user_preferences
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            
            if row:
                prefs = {
                    'daily_calorie_goal': row[0],
                    'daily_protein_goal': row[1],
                    'daily_fat_goal': row[2],
                    'daily_carbs_goal': row[3]
                }
            else:
                prefs = {
                    'daily_calorie_goal': 2000,
                    'daily_protein_goal': 50,
                    'daily_fat_goal': 65,
                    'daily_carbs_goal': 300
                }
            
            conn.close()
            return prefs
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {
                'daily_calorie_goal': 2000,
                'daily_protein_goal': 50,
                'daily_fat_goal': 65,
                'daily_carbs_goal': 300
            }
    
    def get_meal_history(self, user_id, days=7):
        """Get meal history for the last N days"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT
                    id, food_name, calories, protein, fat, carbs, fiber,
                    meal_type, meal_date, meal_time
                FROM meals
                WHERE user_id = ?
                AND meal_date >= date('now', '-' || ? || ' days')
                ORDER BY meal_date DESC, meal_time DESC
            ''', (user_id, days))
            
            meals = []
            for row in cursor.fetchall():
                meals.append({
                    'id': row[0],
                    'food_name': row[1],
                    'calories': row[2],
                    'protein': row[3],
                    'fat': row[4],
                    'carbs': row[5],
                    'fiber': row[6],
                    'meal_type': row[7],
                    'meal_date': row[8],
                    'meal_time': row[9]
                })
            
            conn.close()
            return meals
        except Exception as e:
            logger.error(f"Error getting meal history: {e}")
            return []
    
    def get_date_range_summary(self, user_id, start_date, end_date):
        """Get summary for a date range"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT
                    meal_date,
                    COUNT(*) as meal_count,
                    SUM(calories) as total_calories,
                    SUM(protein) as total_protein,
                    SUM(fat) as total_fat,
                    SUM(carbs) as total_carbs
                FROM meals
                WHERE user_id = ? AND meal_date BETWEEN ? AND ?
                GROUP BY meal_date
                ORDER BY meal_date DESC
            ''', (user_id, start_date, end_date))
            
            daily_summaries = []
            for row in cursor.fetchall():
                daily_summaries.append({
                    'date': row[0],
                    'meal_count': row[1],
                    'total_calories': row[2] or 0,
                    'total_protein': row[3] or 0,
                    'total_fat': row[4] or 0,
                    'total_carbs': row[5] or 0
                })
            
            conn.close()
            return daily_summaries
        except Exception as e:
            logger.error(f"Error getting date range summary: {e}")
            return []

# Made with Bob
