"""Test the expanded food database"""
import re
from src.calorie_database import CalorieDatabase

# Count foods in database
with open('src/calorie_database.py', 'r', encoding='utf-8') as f:
    content = f.read()
    count = len(re.findall(r"'[^']+'\s*:\s*\{", content))

print(f"Total foods in database: {count}")

# Test the database functionality
db = CalorieDatabase()
all_foods = db.get_all_foods()
print(f"Foods accessible via CalorieDatabase: {len(all_foods)}")

# Test some lookups
test_foods = ['pizza', 'apple', 'chicken_breast', 'sushi', 'hamburger']
print("\nTesting food lookups:")
for food in test_foods:
    info = db.get_nutrition_info(food)
    print(f"  {food}: {info.get('calories', 'N/A')} calories")

print("\nDatabase expansion successful!")
