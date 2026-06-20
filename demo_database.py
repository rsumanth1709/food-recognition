"""Demonstrate the expanded food database"""
from src.calorie_database import CalorieDatabase

print("=" * 60)
print("FOOD DATABASE DEMONSTRATION")
print("=" * 60)

# Initialize database
db = CalorieDatabase()

# Get all foods
all_foods = db.get_all_foods()
print(f"\nTotal foods in database: {len(all_foods)}")

# Show sample foods from different categories
print("\n" + "=" * 60)
print("SAMPLE FOODS BY CATEGORY")
print("=" * 60)

categories = {
    "Fruits": ["apple", "banana", "orange", "strawberry", "mango"],
    "Vegetables": ["broccoli", "carrot", "spinach", "tomato", "cucumber"],
    "Proteins": ["chicken_breast", "salmon", "tofu", "boiled_egg", "shrimp"],
    "Grains": ["white_rice", "brown_rice", "pasta", "oats", "quinoa"],
    "Dairy": ["milk_whole", "yogurt", "cheddar_cheese", "butter"],
    "Dishes": ["pizza", "sushi", "hamburger", "tacos", "lasagna"]
}

for category, foods in categories.items():
    print(f"\n{category}:")
    for food in foods:
        info = db.get_nutrition_info(food, 100)
        if 'note' not in info:  # Food was found
            print(f"  - {food}: {info['calories']} cal, "
                  f"{info['protein']}g protein, "
                  f"{info['fat']}g fat, "
                  f"{info['carbs']}g carbs")

# Search functionality
print("\n" + "=" * 60)
print("SEARCH FUNCTIONALITY")
print("=" * 60)

search_terms = ["chicken", "rice", "cheese", "cake"]
for term in search_terms:
    results = db.search_food(term)
    print(f"\nSearch '{term}': Found {len(results)} items")
    if results:
        print(f"  Examples: {', '.join(results[:5])}")

# Show first and last 10 foods
print("\n" + "=" * 60)
print("DATABASE RANGE")
print("=" * 60)
print(f"\nFirst 10 foods: {', '.join(all_foods[:10])}")
print(f"\nLast 10 foods: {', '.join(all_foods[-10:])}")

print("\n" + "=" * 60)
print("DATABASE EXPANSION COMPLETE!")
print("=" * 60)
print(f"\nOriginal: 35 foods")
print(f"Current: {len(all_foods)} foods")
print(f"Increase: {len(all_foods) - 35} foods added ({((len(all_foods) - 35) / 35 * 100):.1f}% growth)")
print("\nThe database is ready for use in the food tracking application!")

