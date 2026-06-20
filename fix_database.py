"""Fix the calorie database structure"""
import re

print("Reading current database file...")
with open('src/calorie_database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract all food entries
food_pattern = r"'([^']+)'\s*:\s*(\{[^}]+\})"
foods = re.findall(food_pattern, content)

print(f"Found {len(foods)} food entries")

# Get the header and class definition
header = '''"""
Calorie database and nutritional information lookup
"""
import csv
import json
import pandas as pd
from pathlib import Path
from config import CALORIE_DB_CONFIG
import logging

logger = logging.getLogger(__name__)

# Comprehensive calorie database for common foods
CALORIE_DATABASE = {
'''

# Add all foods
food_entries = []
for name, data in foods:
    food_entries.append(f"    '{name}': {data},")

# Get the class definition (everything after the first closing brace)
class_start = content.find('\n\nclass CalorieDatabase:')
if class_start == -1:
    class_start = content.find('\nclass CalorieDatabase:')

if class_start > 0:
    class_def = content[class_start:]
    # Clean up any stray food entries in the class definition
    class_def = re.sub(r"\n\s+'[^']+'\s*:\s*\{[^}]+\},?\s*\n", "\n", class_def)
else:
    # Use default class definition
    class_def = '''

class CalorieDatabase:
    """Manager for food calorie and nutritional information"""
    
    def __init__(self, db_path=None):
        """Initialize the calorie database."""
        self.db_path = db_path or CALORIE_DB_CONFIG['db_path']
        self.database = self._load_database()
    
    def _load_database(self):
        """Load database from CSV file or use default"""
        if self.db_path.exists():
            try:
                df = pd.read_csv(self.db_path)
                return df.set_index('food_name').to_dict('index')
            except Exception as e:
                logger.warning(f"Failed to load database from {self.db_path}: {e}")
                return CALORIE_DATABASE
        else:
            logger.info("Database file not found, using default database")
            return CALORIE_DATABASE
    
    def get_nutrition_info(self, food_name, serving_size=100):
        """Get nutritional information for a food item."""
        food_name = food_name.lower().strip()
        
        if food_name in self.database:
            info = self.database[food_name].copy()
        else:
            matches = [key for key in self.database.keys() if food_name in key or key in food_name]
            if matches:
                info = self.database[matches[0]].copy()
            else:
                logger.warning(f"Food item '{food_name}' not found in database")
                return self._default_nutrition()
        
        if 'unit' in info:
            unit = info.pop('unit')
            if 'g' in unit.lower():
                multiplier = serving_size / 100.0
                for key in ['calories', 'protein', 'fat', 'carbs', 'fiber']:
                    if key in info:
                        info[key] = round(info[key] * multiplier, 1)
        
        info['serving_size'] = f"{serving_size}g"
        return info
    
    def _default_nutrition(self):
        """Return default nutritional values"""
        return {
            'calories': 250,
            'protein': 12,
            'fat': 10,
            'carbs': 30,
            'fiber': 2,
            'serving_size': '100g',
            'note': 'Estimated values'
        }
    
    def add_food_item(self, food_name, nutrition_info):
        """Add a new food item to the database."""
        self.database[food_name.lower()] = nutrition_info
        logger.info(f"Added food item: {food_name}")
    
    def search_food(self, query):
        """Search for foods matching a query."""
        query = query.lower()
        matches = [food for food in self.database.keys() if query in food]
        return sorted(matches)
    
    def get_all_foods(self):
        """Get list of all foods in database"""
        return sorted(list(self.database.keys()))
    
    def save_database(self, output_path=None):
        """Save database to CSV file."""
        if output_path is None:
            output_path = self.db_path
        
        df = pd.DataFrame.from_dict(self.database, orient='index')
        df.index.name = 'food_name'
        df.to_csv(output_path)
        logger.info(f"Database saved to {output_path}")
    
    def export_to_json(self, output_path):
        """Export database to JSON format."""
        with open(output_path, 'w') as f:
            json.dump(self.database, f, indent=2)
        logger.info(f"Database exported to {output_path}")


def estimate_calories(food_name, quantity=100, unit='grams'):
    """Quick function to estimate calories for a food."""
    db = CalorieDatabase()
    info = db.get_nutrition_info(food_name, serving_size=quantity)
    return info.get('calories', 0)


def get_macronutrients(food_name, serving_size=100):
    """Get macronutrient breakdown for a food."""
    db = CalorieDatabase()
    info = db.get_nutrition_info(food_name, serving_size)
    return {
        'protein': info.get('protein', 0),
        'fat': info.get('fat', 0),
        'carbs': info.get('carbs', 0),
        'fiber': info.get('fiber', 0)
    }
'''

# Build the complete file
new_content = header + '\n'.join(food_entries) + '\n}' + class_def

# Write the fixed file
print("Writing fixed database file...")
with open('src/calorie_database.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✓ Database file fixed successfully!")
print(f"✓ Total foods in database: {len(foods)}")

# Made with Bob
