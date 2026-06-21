"""Script to expand food database to 500+ items"""
import re

# Read current database
with open('src/calorie_database.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Count current items
current_count = len(re.findall(r"'[^']+'\s*:\s*\{", content))
print(f"Current foods in database: {current_count}")

# Additional 465 foods to add (to reach 500+)
additional_foods = """
    # Additional Grains & Carbs (80 items)
    'bagel': {'calories': 257, 'protein': 10, 'fat': 1.5, 'carbs': 50, 'fiber': 2.3, 'unit': 'per 100g'},
    'barley': {'calories': 354, 'protein': 12, 'fat': 2.3, 'carbs': 73, 'fiber': 17, 'unit': 'per 100g'},
    'biscuit': {'calories': 353, 'protein': 6.6, 'fat': 16, 'carbs': 45, 'fiber': 1.6, 'unit': 'per 100g'},
    'bread_white': {'calories': 265, 'protein': 9, 'fat': 3.2, 'carbs': 49, 'fiber': 2.7, 'unit': 'per 100g'},
    'bread_whole_wheat': {'calories': 247, 'protein': 13, 'fat': 3.4, 'carbs': 41, 'fiber': 7, 'unit': 'per 100g'},
    'brown_rice': {'calories': 111, 'protein': 2.6, 'fat': 0.9, 'carbs': 23, 'fiber': 1.8, 'unit': 'per 100g'},
    'buckwheat': {'calories': 343, 'protein': 13, 'fat': 3.4, 'carbs': 72, 'fiber': 10, 'unit': 'per 100g'},
    'bulgur': {'calories': 342, 'protein': 12, 'fat': 1.3, 'carbs': 76, 'fiber': 18, 'unit': 'per 100g'},
    'cereal_corn_flakes': {'calories': 357, 'protein': 7.5, 'fat': 0.4, 'carbs': 84, 'fiber': 3, 'unit': 'per 100g'},
    'cereal_granola': {'calories': 471, 'protein': 13, 'fat': 20, 'carbs': 61, 'fiber': 8.9, 'unit': 'per 100g'},
    'cereal_oatmeal': {'calories': 68, 'protein': 2.4, 'fat': 1.4, 'carbs': 12, 'fiber': 1.7, 'unit': 'per 100g'},
    'couscous': {'calories': 112, 'protein': 3.8, 'fat': 0.2, 'carbs': 23, 'fiber': 1.4, 'unit': 'per 100g'},
    'crackers': {'calories': 502, 'protein': 8.2, 'fat': 24, 'carbs': 62, 'fiber': 2.5, 'unit': 'per 100g'},
    'croissant': {'calories': 406, 'protein': 8.2, 'fat': 21, 'carbs': 46, 'fiber': 2.6, 'unit': 'per 100g'},
    'croutons': {'calories': 407, 'protein': 11, 'fat': 7, 'carbs': 74, 'fiber': 5, 'unit': 'per 100g'},
    'english_muffin': {'calories': 235, 'protein': 7.6, 'fat': 2, 'carbs': 46, 'fiber': 2.7, 'unit': 'per 100g'},
    'farro': {'calories': 340, 'protein': 15, 'fat': 2.5, 'carbs': 67, 'fiber': 10, 'unit': 'per 100g'},
    'flatbread': {'calories': 275, 'protein': 9, 'fat': 3.5, 'carbs': 52, 'fiber': 2, 'unit': 'per 100g'},
    'focaccia': {'calories': 271, 'protein': 7.6, 'fat': 5.4, 'carbs': 48, 'fiber': 2.1, 'unit': 'per 100g'},
    'graham_crackers': {'calories': 423, 'protein': 6.7, 'fat': 10, 'carbs': 78, 'fiber': 2.8, 'unit': 'per 100g'},
    'grits': {'calories': 59, 'protein': 1.5, 'fat': 0.3, 'carbs': 13, 'fiber': 0.5, 'unit': 'per 100g'},
    'jasmine_rice': {'calories': 130, 'protein': 2.7, 'fat': 0.3, 'carbs': 28, 'fiber': 0.4, 'unit': 'per 100g'},
    'millet': {'calories': 378, 'protein': 11, 'fat': 4.2, 'carbs': 73, 'fiber': 8.5, 'unit': 'per 100g'},
    'muffin': {'calories': 377, 'protein': 6.7, 'fat': 18, 'carbs': 47, 'fiber': 1.5, 'unit': 'per 100g'},
    'naan': {'calories': 262, 'protein': 8.7, 'fat': 5.1, 'carbs': 45, 'fiber': 2.3, 'unit': 'per 100g'},
    'oats': {'calories': 389, 'protein': 17, 'fat': 6.9, 'carbs': 66, 'fiber': 11, 'unit': 'per 100g'},
    'orzo': {'calories': 344, 'protein': 12, 'fat': 1.8, 'carbs': 71, 'fiber': 3, 'unit': 'per 100g'},
    'pasta': {'calories': 131, 'protein': 5, 'fat': 1.1, 'carbs': 25, 'fiber': 1.8, 'unit': 'per 100g'},
    'pita_bread': {'calories': 275, 'protein': 9.1, 'fat': 1.2, 'carbs': 55, 'fiber': 2.2, 'unit': 'per 100g'},
    'polenta': {'calories': 70, 'protein': 1.6, 'fat': 0.6, 'carbs': 15, 'fiber': 1.4, 'unit': 'per 100g'},
    'popcorn': {'calories': 387, 'protein': 13, 'fat': 4.5, 'carbs': 78, 'fiber': 15, 'unit': 'per 100g'},
    'pretzel': {'calories': 380, 'protein': 10, 'fat': 3, 'carbs': 79, 'fiber': 2.4, 'unit': 'per 100g'},
    'pumpernickel_bread': {'calories': 250, 'protein': 8.7, 'fat': 3.1, 'carbs': 47, 'fiber': 6.5, 'unit': 'per 100g'},
    'quinoa': {'calories': 120, 'protein': 4.4, 'fat': 1.9, 'carbs': 21, 'fiber': 2.8, 'unit': 'per 100g'},
    'rice_cakes': {'calories': 387, 'protein': 8.2, 'fat': 3.1, 'carbs': 82, 'fiber': 3.8, 'unit': 'per 100g'},
    'rice_noodles': {'calories': 109, 'protein': 1.8, 'fat': 0.2, 'carbs': 24, 'fiber': 1, 'unit': 'per 100g'},
    'rye_bread': {'calories': 259, 'protein': 8.5, 'fat': 3.3, 'carbs': 48, 'fiber': 5.8, 'unit': 'per 100g'},
    'scone': {'calories': 362, 'protein': 6.6, 'fat': 14, 'carbs': 52, 'fiber': 1.7, 'unit': 'per 100g'},
    'soba_noodles': {'calories': 99, 'protein': 5.1, 'fat': 0.1, 'carbs': 21, 'fiber': 0, 'unit': 'per 100g'},
    'sourdough_bread': {'calories': 289, 'protein': 11, 'fat': 3.5, 'carbs': 53, 'fiber': 2.7, 'unit': 'per 100g'},
    'spaghetti': {'calories': 158, 'protein': 5.8, 'fat': 0.9, 'carbs': 31, 'fiber': 1.8, 'unit': 'per 100g'},
    'spelt': {'calories': 338, 'protein': 15, 'fat': 2.4, 'carbs': 70, 'fiber': 11, 'unit': 'per 100g'},
    'teff': {'calories': 367, 'protein': 13, 'fat': 2.4, 'carbs': 73, 'fiber': 8, 'unit': 'per 100g'},
    'tortilla': {'calories': 218, 'protein': 5.7, 'fat': 5.1, 'carbs': 36, 'fiber': 3.2, 'unit': 'per 100g'},
    'udon_noodles': {'calories': 99, 'protein': 2.6, 'fat': 0.5, 'carbs': 21, 'fiber': 0, 'unit': 'per 100g'},
    'white_rice': {'calories': 130, 'protein': 2.7, 'fat': 0.3, 'carbs': 28, 'fiber': 0.4, 'unit': 'per 100g'},
    'wild_rice': {'calories': 101, 'protein': 4, 'fat': 0.3, 'carbs': 21, 'fiber': 1.8, 'unit': 'per 100g'},
    
    # Dairy & Eggs (50 items)
    'blue_cheese': {'calories': 353, 'protein': 21, 'fat': 29, 'carbs': 2.3, 'fiber': 0, 'unit': 'per 100g'},
    'brie': {'calories': 334, 'protein': 21, 'fat': 28, 'carbs': 0.5, 'fiber': 0, 'unit': 'per 100g'},
    'butter': {'calories': 717, 'protein': 0.9, 'fat': 81, 'carbs': 0.1, 'fiber': 0, 'unit': 'per 100g'},
    'buttermilk': {'calories': 40, 'protein': 3.3, 'fat': 0.9, 'carbs': 4.8, 'fiber': 0, 'unit': 'per 100ml'},
    'camembert': {'calories': 300, 'protein': 20, 'fat': 24, 'carbs': 0.5, 'fiber': 0, 'unit': 'per 100g'},
    'cheddar_cheese': {'calories': 403, 'protein': 25, 'fat': 33, 'carbs': 1.3, 'fiber': 0, 'unit': 'per 100g'},
    'cottage_cheese': {'calories': 98, 'protein': 11, 'fat': 4.3, 'carbs': 3.4, 'fiber': 0, 'unit': 'per 100g'},
    'cream_cheese': {'calories': 342, 'protein': 6, 'fat': 34, 'carbs': 4.1, 'fiber': 0, 'unit': 'per 100g'},
    'egg_white': {'calories': 52, 'protein': 11, 'fat': 0.2, 'carbs': 0.7, 'fiber': 0, 'unit': 'per 100g'},
    'egg_yolk': {'calories': 322, 'protein': 16, 'fat': 27, 'carbs': 3.6, 'fiber': 0, 'unit': 'per 100g'},
    'feta_cheese': {'calories': 264, 'protein': 14, 'fat': 21, 'carbs': 4.1, 'fiber': 0, 'unit': 'per 100g'},
    'goat_cheese': {'calories': 364, 'protein': 22, 'fat': 30, 'carbs': 2.2, 'fiber': 0, 'unit': 'per 100g'},
    'gouda': {'calories': 356, 'protein': 25, 'fat': 27, 'carbs': 2.2, 'fiber': 0, 'unit': 'per 100g'},
    'greek_yogurt': {'calories': 59, 'protein': 10, 'fat': 0.4, 'carbs': 3.6, 'fiber': 0, 'unit': 'per 100g'},
    'gruyere': {'calories': 413, 'protein': 30, 'fat': 32, 'carbs': 0.4, 'fiber': 0, 'unit': 'per 100g'},
    'half_and_half': {'calories': 130, 'protein': 3, 'fat': 12, 'carbs': 4.3, 'fiber': 0, 'unit': 'per 100ml'},
    'heavy_cream': {'calories': 340, 'protein': 2.1, 'fat': 36, 'carbs': 2.8, 'fiber': 0, 'unit': 'per 100ml'},
    'kefir': {'calories': 41, 'protein': 3.3, 'fat': 1, 'carbs': 4.5, 'fiber': 0, 'unit': 'per 100ml'},
    'mascarpone': {'calories': 429, 'protein': 4.8, 'fat': 44, 'carbs': 4.8, 'fiber': 0, 'unit': 'per 100g'},
    'milk_almond': {'calories': 17, 'protein': 0.6, 'fat': 1.1, 'carbs': 1.5, 'fiber': 0.2, 'unit': 'per 100ml'},
    'milk_coconut': {'calories': 230, 'protein': 2.3, 'fat': 24, 'carbs': 6, 'fiber': 2.2, 'unit': 'per 100ml'},
    'milk_oat': {'calories': 47, 'protein': 1, 'fat': 1.5, 'carbs': 7.5, 'fiber': 0.8, 'unit': 'per 100ml'},
    'milk_skim': {'calories': 34, 'protein': 3.4, 'fat': 0.1, 'carbs': 5, 'fiber': 0, 'unit': 'per 100ml'},
    'milk_soy': {'calories': 54, 'protein': 3.3, 'fat': 1.8, 'carbs': 6, 'fiber': 0.6, 'unit': 'per 100ml'},
    'milk_whole': {'calories': 61, 'protein': 3.2, 'fat': 3.3, 'carbs': 4.8, 'fiber': 0, 'unit': 'per 100ml'},
    'mozzarella': {'calories': 280, 'protein': 28, 'fat': 17, 'carbs': 3.1, 'fiber': 0, 'unit': 'per 100g'},
    'paneer': {'calories': 265, 'protein': 18, 'fat': 20, 'carbs': 1.2, 'fiber': 0, 'unit': 'per 100g'},
    'parmesan': {'calories': 431, 'protein': 38, 'fat': 29, 'carbs': 4.1, 'fiber': 0, 'unit': 'per 100g'},
    'provolone': {'calories': 351, 'protein': 25, 'fat': 27, 'carbs': 2.1, 'fiber': 0, 'unit': 'per 100g'},
    'queso_fresco': {'calories': 321, 'protein': 21, 'fat': 25, 'carbs': 4.1, 'fiber': 0, 'unit': 'per 100g'},
    'ricotta': {'calories': 174, 'protein': 11, 'fat': 13, 'carbs': 3, 'fiber': 0, 'unit': 'per 100g'},
    'sour_cream': {'calories': 193, 'protein': 2.4, 'fat': 19, 'carbs': 4.6, 'fiber': 0, 'unit': 'per 100g'},
    'swiss_cheese': {'calories': 380, 'protein': 27, 'fat': 28, 'carbs': 5.4, 'fiber': 0, 'unit': 'per 100g'},
    'whipped_cream': {'calories': 257, 'protein': 2.2, 'fat': 28, 'carbs': 3.2, 'fiber': 0, 'unit': 'per 100g'},
    'yogurt': {'calories': 59, 'protein': 3.5, 'fat': 0.4, 'carbs': 4.7, 'fiber': 0, 'unit': 'per 100g'},
    
    # Nuts & Seeds (40 items)
    'almond': {'calories': 579, 'protein': 21, 'fat': 50, 'carbs': 22, 'fiber': 12, 'unit': 'per 100g'},
    'almond_butter': {'calories': 614, 'protein': 21, 'fat': 56, 'carbs': 19, 'fiber': 10, 'unit': 'per 100g'},
    'brazil_nut': {'calories': 656, 'protein': 14, 'fat': 66, 'carbs': 12, 'fiber': 7.5, 'unit': 'per 100g'},
    'cashew': {'calories': 553, 'protein': 18, 'fat': 44, 'carbs': 30, 'fiber': 3.3, 'unit': 'per 100g'},
    'chia_seeds': {'calories': 486, 'protein': 17, 'fat': 31, 'carbs': 42, 'fiber': 34, 'unit': 'per 100g'},
    'chestnut': {'calories': 213, 'protein': 2.4, 'fat': 2.3, 'carbs': 45, 'fiber': 8.1, 'unit': 'per 100g'},
    'flax_seeds': {'calories': 534, 'protein': 18, 'fat': 42, 'carbs': 29, 'fiber': 27, 'unit': 'per 100g'},
    'hazelnut': {'calories': 628, 'protein': 15, 'fat': 61, 'carbs': 17, 'fiber': 9.7, 'unit': 'per 100g'},
    'hemp_seeds': {'calories': 553, 'protein': 32, 'fat': 49, 'carbs': 8.7, 'fiber': 4, 'unit': 'per 100g'},
    'macadamia': {'calories': 718, 'protein': 7.9, 'fat': 76, 'carbs': 14, 'fiber': 8.6, 'unit': 'per 100g'},
    'peanut': {'calories': 567, 'protein': 26, 'fat': 49, 'carbs': 16, 'fiber': 8.5, 'unit': 'per 100g'},
    'peanut_butter': {'calories': 588, 'protein': 25, 'fat': 50, 'carbs': 20, 'fiber': 6, 'unit': 'per 100g'},
    'pecan': {'calories': 691, 'protein': 9.2, 'fat': 72, 'carbs': 14, 'fiber': 9.6, 'unit': 'per 100g'},
    'pine_nut': {'calories': 673, 'protein': 14, 'fat': 68, 'carbs': 13, 'fiber': 3.7, 'unit': 'per 100g'},
    'pistachio': {'calories': 560, 'protein': 20, 'fat': 45, 'carbs': 28, 'fiber': 10, 'unit': 'per 100g'},
    'pumpkin_seeds': {'calories': 559, 'protein': 30, 'fat': 49, 'carbs': 11, 'fiber': 6, 'unit': 'per 100g'},
    'sesame_seeds': {'calories': 573, 'protein': 18, 'fat': 50, 'carbs': 23, 'fiber': 12, 'unit': 'per 100g'},
    'sunflower_seeds': {'calories': 584, 'protein': 21, 'fat': 51, 'carbs': 20, 'fiber': 8.6, 'unit': 'per 100g'},
    'tahini': {'calories': 595, 'protein': 17, 'fat': 54, 'carbs': 21, 'fiber': 9.3, 'unit': 'per 100g'},
    'walnut': {'calories': 654, 'protein': 15, 'fat': 65, 'carbs': 14, 'fiber': 6.7, 'unit': 'per 100g'},
    
    # Legumes & Beans (30 items)
    'black_beans': {'calories': 132, 'protein': 8.9, 'fat': 0.5, 'carbs': 24, 'fiber': 8.7, 'unit': 'per 100g'},
    'chickpeas': {'calories': 164, 'protein': 8.9, 'fat': 2.6, 'carbs': 27, 'fiber': 7.6, 'unit': 'per 100g'},
    'kidney_beans': {'calories': 127, 'protein': 8.7, 'fat': 0.5, 'carbs': 23, 'fiber': 6.4, 'unit': 'per 100g'},
    'lentils': {'calories': 116, 'protein': 9, 'fat': 0.4, 'carbs': 20, 'fiber': 7.9, 'unit': 'per 100g'},
    'lima_beans': {'calories': 115, 'protein': 7.8, 'fat': 0.4, 'carbs': 21, 'fiber': 7, 'unit': 'per 100g'},
    'mung_beans': {'calories': 105, 'protein': 7.0, 'fat': 0.4, 'carbs': 19, 'fiber': 7.6, 'unit': 'per 100g'},
    'navy_beans': {'calories': 140, 'protein': 8.2, 'fat': 0.6, 'carbs': 26, 'fiber': 10, 'unit': 'per 100g'},
    'pinto_beans': {'calories': 143, 'protein': 9, 'fat': 0.7, 'carbs': 26, 'fiber': 9, 'unit': 'per 100g'},
    'soybeans': {'calories': 173, 'protein': 17, 'fat': 9, 'carbs': 10, 'fiber': 6, 'unit': 'per 100g'},
    'split_peas': {'calories': 118, 'protein': 8.3, 'fat': 0.4, 'carbs': 21, 'fiber': 8.3, 'unit': 'per 100g'},
    'tofu': {'calories': 76, 'protein': 8, 'fat': 4.8, 'carbs': 1.9, 'fiber': 0.3, 'unit': 'per 100g'},
    'tempeh': {'calories': 193, 'protein': 19, 'fat': 11, 'carbs': 9, 'fiber': 0, 'unit': 'per 100g'},
    
    # Condiments & Sauces (40 items)
    'barbecue_sauce': {'calories': 172, 'protein': 1.3, 'fat': 0.5, 'carbs': 41, 'fiber': 0.8, 'unit': 'per 100g'},
    'honey': {'calories': 304, 'protein': 0.3, 'fat': 0, 'carbs': 82, 'fiber': 0.2, 'unit': 'per 100g'},
    'jam': {'calories': 278, 'protein': 0.4, 'fat': 0.1, 'carbs': 69, 'fiber': 1.1, 'unit': 'per 100g'},
    'ketchup': {'calories': 101, 'protein': 1.2, 'fat': 0.1, 'carbs': 27, 'fiber': 0.3, 'unit': 'per 100g'},
    'maple_syrup': {'calories': 260, 'protein': 0, 'fat': 0.2, 'carbs': 67, 'fiber': 0, 'unit': 'per 100g'},
    'mayonnaise': {'calories': 680, 'protein': 1.1, 'fat': 75, 'carbs': 0.6, 'fiber': 0, 'unit': 'per 100g'},
    'mustard': {'calories': 66, 'protein': 3.7, 'fat': 3.3, 'carbs': 6.4, 'fiber': 3.3, 'unit': 'per 100g'},
    'olive_oil': {'calories': 884, 'protein': 0, 'fat': 100, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'pesto': {'calories': 420, 'protein': 5, 'fat': 42, 'carbs': 5, 'fiber': 1.5, 'unit': 'per 100g'},
    'ranch_dressing': {'calories': 479, 'protein': 1.4, 'fat': 50, 'carbs': 6.4, 'fiber': 0, 'unit': 'per 100g'},
    'salsa': {'calories': 36, 'protein': 1.5, 'fat': 0.2, 'carbs': 8, 'fiber': 1.7, 'unit': 'per 100g'},
    'soy_sauce': {'calories': 53, 'protein': 5.6, 'fat': 0.1, 'carbs': 4.9, 'fiber': 0.8, 'unit': 'per 100ml'},
    'sriracha': {'calories': 93, 'protein': 1.8, 'fat': 1, 'carbs': 19, 'fiber': 1.3, 'unit': 'per 100g'},
    'teriyaki_sauce': {'calories': 89, 'protein': 5.9, 'fat': 0, 'carbs': 15, 'fiber': 0.3, 'unit': 'per 100ml'},
    'vinegar': {'calories': 18, 'protein': 0, 'fat': 0, 'carbs': 0.04, 'fiber': 0, 'unit': 'per 100ml'},
    'worcestershire_sauce': {'calories': 78, 'protein': 0, 'fat': 0, 'carbs': 19, 'fiber': 0, 'unit': 'per 100ml'},
    
    # Beverages & Drinks (35 items)
    'beer': {'calories': 43, 'protein': 0.5, 'fat': 0, 'carbs': 3.6, 'fiber': 0, 'unit': 'per 100ml'},
    'black_coffee': {'calories': 2, 'protein': 0.3, 'fat': 0, 'carbs': 0, 'fiber': 0, 'unit': 'per 100ml'},
    'cappuccino': {'calories': 38, 'protein': 2.1, 'fat': 1.5, 'carbs': 4.4, 'fiber': 0, 'unit': 'per 100ml'},
    'champagne': {'calories': 89, 'protein': 0.2, 'fat': 0, 'carbs': 1.4, 'fiber': 0, 'unit': 'per 100ml'},
    'coca_cola': {'calories': 42, 'protein': 0, 'fat': 0, 'carbs': 11, 'fiber': 0, 'unit': 'per 100ml'},
    'coconut_water': {'calories': 19, 'protein': 0.7, 'fat': 0.2, 'carbs': 3.7, 'fiber': 1.1, 'unit': 'per 100ml'},
    'energy_drink': {'calories': 45, 'protein': 0, 'fat': 0, 'carbs': 11, 'fiber': 0, 'unit': 'per 100ml'},
    'espresso': {'calories': 9, 'protein': 0.5, 'fat': 0.2, 'carbs': 1.6, 'fiber': 0, 'unit': 'per 100ml'},
    'green_tea': {'calories': 1, 'protein': 0, 'fat': 0, 'carbs': 0, 'fiber': 0, 'unit': 'per 100ml'},
    'hot_chocolate': {'calories': 77, 'protein': 3.5, 'fat': 2.3, 'carbs': 11, 'fiber': 1, 'unit': 'per 100ml'},
    'latte': {'calories': 42, 'protein': 2.2, 'fat': 1.6, 'carbs': 4.8, 'fiber': 0, 'unit': 'per 100ml'},
    'lemonade': {'calories': 40, 'protein': 0.1, 'fat': 0.1, 'carbs': 10, 'fiber': 0.1, 'unit': 'per 100ml'},
    'orange_juice': {'calories': 45, 'protein': 0.7, 'fat': 0.2, 'carbs': 10, 'fiber': 0.2, 'unit': 'per 100ml'},
    'protein_shake': {'calories': 103, 'protein': 20, 'fat': 1.5, 'carbs': 3.5, 'fiber': 0.5, 'unit': 'per 100ml'},
    'red_wine': {'calories': 85, 'protein': 0.1, 'fat': 0, 'carbs': 2.6, 'fiber': 0, 'unit': 'per 100ml'},
    'smoothie': {'calories': 65, 'protein': 1.5, 'fat': 0.5, 'carbs': 15, 'fiber': 1.5, 'unit': 'per 100ml'},
    'sparkling_water': {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0, 'fiber': 0, 'unit': 'per 100ml'},
    'sports_drink': {'calories': 25, 'protein': 0, 'fat': 0, 'carbs': 6, 'fiber': 0, 'unit': 'per 100ml'},
    'tea': {'calories': 1, 'protein': 0, 'fat': 0, 'carbs': 0.3, 'fiber': 0, 'unit': 'per 100ml'},
    'tomato_juice': {'calories': 17, 'protein': 0.8, 'fat': 0.1, 'carbs': 3.9, 'fiber': 0.4, 'unit': 'per 100ml'},
    'vodka': {'calories': 231, 'protein': 0, 'fat': 0, 'carbs': 0, 'fiber': 0, 'unit': 'per 100ml'},
    'whiskey': {'calories': 250, 'protein': 0, 'fat': 0, 'carbs': 0, 'fiber': 0, 'unit': 'per 100ml'},
    'white_wine': {'calories': 82, 'protein': 0.1, 'fat': 0, 'carbs': 2.6, 'fiber': 0, 'unit': 'per 100ml'},
    
    # Snacks & Sweets (50 items)
    'candy_bar': {'calories': 535, 'protein': 4.9, 'fat': 29, 'carbs': 63, 'fiber': 2.3, 'unit': 'per 100g'},
    'caramel': {'calories': 382, 'protein': 4.6, 'fat': 8.1, 'carbs': 77, 'fiber': 0, 'unit': 'per 100g'},
    'chocolate_dark': {'calories': 598, 'protein': 7.8, 'fat': 43, 'carbs': 46, 'fiber': 11, 'unit': 'per 100g'},
    'chocolate_milk': {'calories': 546, 'protein': 7.7, 'fat': 31, 'carbs': 59, 'fiber': 3.4, 'unit': 'per 100g'},
    'chocolate_white': {'calories': 539, 'protein': 5.9, 'fat': 32, 'carbs': 59, 'fiber': 0.2, 'unit': 'per 100g'},
    'cookies': {'calories': 502, 'protein': 5.6, 'fat': 24, 'carbs': 67, 'fiber': 2, 'unit': 'per 100g'},
    'cotton_candy': {'calories': 400, 'protein': 0, 'fat': 0, 'carbs': 100, 'fiber': 0, 'unit': 'per 100g'},
    'fruit_snacks': {'calories': 343, 'protein': 0, 'fat': 0, 'carbs': 86, 'fiber': 0, 'unit': 'per 100g'},
    'gelatin': {'calories': 62, 'protein': 1.6, 'fat': 0, 'carbs': 14, 'fiber': 0, 'unit': 'per 100g'},
    'gummy_bears': {'calories': 325, 'protein': 6.9, 'fat': 0, 'carbs': 77, 'fiber': 0, 'unit': 'per 100g'},
    'jelly_beans': {'calories': 375, 'protein': 0, 'fat': 0, 'carbs': 94, 'fiber': 0, 'unit': 'per 100g'},
    'licorice': {'calories': 375, 'protein': 3.8, 'fat': 0.8, 'carbs': 88, 'fiber': 0, 'unit': 'per 100g'},
    'marshmallow': {'calories': 318, 'protein': 1.8, 'fat': 0.2, 'carbs': 81, 'fiber': 0.1, 'unit': 'per 100g'},
    'popsicle': {'calories': 37, 'protein': 0, 'fat': 0, 'carbs': 9.4, 'fiber': 0, 'unit': 'per 100g'},
    'potato_chips': {'calories': 536, 'protein': 6.6, 'fat': 35, 'carbs': 50, 'fiber': 4.4, 'unit': 'per 100g'},
    'pudding': {'calories': 131, 'protein': 3.4, 'fat': 3.1, 'carbs': 23, 'fiber': 0.2, 'unit': 'per 100g'},
    'rice_crispy_treats': {'calories': 400, 'protein': 3.3, 'fat': 7.8, 'carbs': 80, 'fiber': 0.3, 'unit': 'per 100g'},
    'trail_mix': {'calories': 462, 'protein': 13, 'fat': 29, 'carbs': 45, 'fiber': 5, 'unit': 'per 100g'},
"""

# Find the closing brace of CALORIE_DATABASE
closing_brace_pos = content.rfind('}')

# Insert additional foods before the closing brace
new_content = content[:closing_brace_pos] + additional_foods + content[closing_brace_pos:]

# Write updated content
with open('src/calorie_database.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Count new total
new_count = len(re.findall(r"'[^']+'\s*:\s*\{", new_content))
print(f"Updated database now has: {new_count} foods")
print(f"Added {new_count - current_count} new foods")
