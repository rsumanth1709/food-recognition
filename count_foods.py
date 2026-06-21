"""Count foods in database"""
import re

with open('src/calorie_database.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Count dictionary entries
matches = re.findall(r"'([^']+)'\s*:\s*\{", content)
print(f"Total foods in database: {len(matches)}")
print(f"\nFirst 10 foods: {matches[:10]}")
print(f"Last 10 foods: {matches[-10:]}")

