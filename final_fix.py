"""Final fix for database - remove all stray entries after functions"""
import re

print("Reading database file...")
with open('src/calorie_database.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find where get_macronutrients function ends
in_function = False
function_end_line = 0

for i, line in enumerate(lines):
    if 'def get_macronutrients' in line:
        in_function = True
    if in_function and line.strip() == '}':
        function_end_line = i + 1
        break

if function_end_line > 0:
    # Keep everything up to and including the function end
    clean_lines = lines[:function_end_line]
    
    print(f"Removing stray entries after line {function_end_line}")
    print(f"Kept {len(clean_lines)} lines")
    
    # Write cleaned file
    with open('src/calorie_database.py', 'w', encoding='utf-8') as f:
        f.writelines(clean_lines)
    
    print("Database file cleaned successfully!")
    print("Now counting foods...")
    
    # Count foods
    content = ''.join(clean_lines)
    foods = re.findall(r"'([^']+)'\s*:\s*\{", content)
    print(f"Total foods in database: {len(foods)}")
else:
    print("Could not find function end")

# Made with Bob
