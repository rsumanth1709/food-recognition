"""
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
    'apple_pie': {'calories': 237, 'protein': 1.9, 'fat': 10.8, 'carbs': 34.5, 'fiber': 1.5, 'unit': 'per 100g'},
    'baby_back_ribs': {'calories': 291, 'protein': 24.5, 'fat': 23.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'baklava': {'calories': 380, 'protein': 7.5, 'fat': 21, 'carbs': 40, 'fiber': 2, 'unit': 'per 100g'},
    'beef_carpaccio': {'calories': 143, 'protein': 27, 'fat': 4.3, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'beef_tartare': {'calories': 155, 'protein': 28, 'fat': 5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'beet_salad': {'calories': 85, 'protein': 3.2, 'fat': 3.5, 'carbs': 12.5, 'fiber': 2.8, 'unit': 'per 100g'},
    'beignets': {'calories': 320, 'protein': 5, 'fat': 18, 'carbs': 35, 'fiber': 1, 'unit': 'per 100g'},
    'bibimbap': {'calories': 160, 'protein': 8, 'fat': 6, 'carbs': 20, 'fiber': 3, 'unit': 'per 100g'},
    'black_bean_soup': {'calories': 75, 'protein': 5, 'fat': 1.5, 'carbs': 12, 'fiber': 3.5, 'unit': 'per 100ml'},
    'black_eyed_peas': {'calories': 116, 'protein': 8.5, 'fat': 0.5, 'carbs': 20, 'fiber': 4.5, 'unit': 'per 100g'},
    'boiled_egg': {'calories': 155, 'protein': 13, 'fat': 11, 'carbs': 1.1, 'fiber': 0, 'unit': 'per 100g'},
    'borscht': {'calories': 55, 'protein': 2.5, 'fat': 1.8, 'carbs': 8.5, 'fiber': 1.5, 'unit': 'per 100ml'},
    'breakfast_burrito': {'calories': 250, 'protein': 14, 'fat': 12, 'carbs': 24, 'fiber': 3, 'unit': 'per 100g'},
    'broccoli': {'calories': 34, 'protein': 2.8, 'fat': 0.4, 'carbs': 7, 'fiber': 2.4, 'unit': 'per 100g'},
    'brownies': {'calories': 406, 'protein': 5.2, 'fat': 23, 'carbs': 43, 'fiber': 1.5, 'unit': 'per 100g'},
    'buffalo_wings': {'calories': 290, 'protein': 28, 'fat': 20, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'caesar_salad': {'calories': 160, 'protein': 7, 'fat': 10, 'carbs': 12, 'fiber': 1.5, 'unit': 'per 100g'},
    'cake': {'calories': 365, 'protein': 4.2, 'fat': 16, 'carbs': 48, 'fiber': 1, 'unit': 'per 100g'},
    'calzone': {'calories': 290, 'protein': 12, 'fat': 12, 'carbs': 34, 'fiber': 2, 'unit': 'per 100g'},
    'carrot_cake': {'calories': 370, 'protein': 4.5, 'fat': 15.5, 'carbs': 50, 'fiber': 1.5, 'unit': 'per 100g'},
    'caviar': {'calories': 264, 'protein': 24.9, 'fat': 17.9, 'carbs': 4, 'fiber': 0, 'unit': 'per 100g'},
    'ceviche': {'calories': 90, 'protein': 16, 'fat': 1.5, 'carbs': 2, 'fiber': 0.5, 'unit': 'per 100g'},
    'cheese_plate': {'calories': 400, 'protein': 25, 'fat': 33, 'carbs': 2, 'fiber': 0, 'unit': 'per 100g'},
    'cheesecake': {'calories': 321, 'protein': 6, 'fat': 20, 'carbs': 30, 'fiber': 0.5, 'unit': 'per 100g'},
    'chef_salad': {'calories': 120, 'protein': 12, 'fat': 6, 'carbs': 8, 'fiber': 2, 'unit': 'per 100g'},
    'cherry_pie': {'calories': 220, 'protein': 2.3, 'fat': 8.5, 'carbs': 35, 'fiber': 1.2, 'unit': 'per 100g'},
    'chicken_curry': {'calories': 165, 'protein': 18, 'fat': 8, 'carbs': 6, 'fiber': 1, 'unit': 'per 100g'},
    'chicken_fingers': {'calories': 285, 'protein': 22, 'fat': 15, 'carbs': 18, 'fiber': 0.5, 'unit': 'per 100g'},
    'chicken_teriyaki': {'calories': 195, 'protein': 28, 'fat': 5, 'carbs': 12, 'fiber': 0.5, 'unit': 'per 100g'},
    'chickpea_curry': {'calories': 145, 'protein': 8.5, 'fat': 6, 'carbs': 16, 'fiber': 4, 'unit': 'per 100g'},
    'chocolate_cake': {'calories': 385, 'protein': 4.8, 'fat': 18, 'carbs': 48, 'fiber': 1.5, 'unit': 'per 100g'},
    'chocolate_mousse': {'calories': 250, 'protein': 4, 'fat': 17, 'carbs': 22, 'fiber': 1, 'unit': 'per 100g'},
    'churro': {'calories': 366, 'protein': 2.5, 'fat': 22, 'carbs': 38, 'fiber': 0.5, 'unit': 'per 100g'},
    'chow_mein': {'calories': 180, 'protein': 8, 'fat': 7, 'carbs': 24, 'fiber': 1, 'unit': 'per 100g'},
    'chow_fun': {'calories': 165, 'protein': 7, 'fat': 6, 'carbs': 22, 'fiber': 1, 'unit': 'per 100g'},
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
    'acai_berry': {'calories': 70, 'protein': 2, 'fat': 5, 'carbs': 4, 'fiber': 2, 'unit': 'per 100g'},
    'boysenberry': {'calories': 50, 'protein': 1.1, 'fat': 0.5, 'carbs': 12, 'fiber': 5.3, 'unit': 'per 100g'},
    'cloudberry': {'calories': 51, 'protein': 2.4, 'fat': 0.8, 'carbs': 9, 'fiber': 6.3, 'unit': 'per 100g'},
    'currant': {'calories': 63, 'protein': 1.4, 'fat': 0.2, 'carbs': 15, 'fiber': 4.3, 'unit': 'per 100g'},
    'elderberry': {'calories': 73, 'protein': 0.7, 'fat': 0.5, 'carbs': 19, 'fiber': 7, 'unit': 'per 100g'},
    'gooseberry': {'calories': 44, 'protein': 0.9, 'fat': 0.6, 'carbs': 10, 'fiber': 4.3, 'unit': 'per 100g'},
    'kumquat': {'calories': 71, 'protein': 1.9, 'fat': 0.9, 'carbs': 16, 'fiber': 6.5, 'unit': 'per 100g'},
    'mulberry': {'calories': 43, 'protein': 1.4, 'fat': 0.4, 'carbs': 10, 'fiber': 1.7, 'unit': 'per 100g'},
    'rambutan': {'calories': 82, 'protein': 0.7, 'fat': 0.2, 'carbs': 21, 'fiber': 0.9, 'unit': 'per 100g'},
    'bamboo_shoots': {'calories': 27, 'protein': 2.6, 'fat': 0.3, 'carbs': 5, 'fiber': 2.2, 'unit': 'per 100g'},
    'bean_sprouts': {'calories': 30, 'protein': 3, 'fat': 0.2, 'carbs': 6, 'fiber': 1.8, 'unit': 'per 100g'},
    'bitter_melon': {'calories': 17, 'protein': 1, 'fat': 0.2, 'carbs': 3.7, 'fiber': 2.8, 'unit': 'per 100g'},
    'butternut_squash': {'calories': 45, 'protein': 1, 'fat': 0.1, 'carbs': 12, 'fiber': 2, 'unit': 'per 100g'},
    'celeriac': {'calories': 42, 'protein': 1.5, 'fat': 0.3, 'carbs': 9, 'fiber': 1.8, 'unit': 'per 100g'},
    'chayote': {'calories': 19, 'protein': 0.8, 'fat': 0.1, 'carbs': 4.5, 'fiber': 1.7, 'unit': 'per 100g'},
    'daikon': {'calories': 18, 'protein': 0.6, 'fat': 0.1, 'carbs': 4.1, 'fiber': 1.6, 'unit': 'per 100g'},
    'jicama': {'calories': 38, 'protein': 0.7, 'fat': 0.1, 'carbs': 9, 'fiber': 4.9, 'unit': 'per 100g'},
    'kohlrabi': {'calories': 27, 'protein': 1.7, 'fat': 0.1, 'carbs': 6, 'fiber': 3.6, 'unit': 'per 100g'},
    'lotus_root': {'calories': 74, 'protein': 2.6, 'fat': 0.1, 'carbs': 17, 'fiber': 4.9, 'unit': 'per 100g'},
    'napa_cabbage': {'calories': 16, 'protein': 1.2, 'fat': 0.2, 'carbs': 3.2, 'fiber': 1.2, 'unit': 'per 100g'},
    'radicchio': {'calories': 23, 'protein': 1.4, 'fat': 0.3, 'carbs': 4.5, 'fiber': 0.9, 'unit': 'per 100g'},
    'rutabaga': {'calories': 37, 'protein': 1.1, 'fat': 0.2, 'carbs': 8.6, 'fiber': 2.3, 'unit': 'per 100g'},
    'salsify': {'calories': 82, 'protein': 3.3, 'fat': 0.2, 'carbs': 18, 'fiber': 3.3, 'unit': 'per 100g'},
    'taro': {'calories': 112, 'protein': 1.5, 'fat': 0.2, 'carbs': 27, 'fiber': 4.1, 'unit': 'per 100g'},
    'water_chestnut': {'calories': 97, 'protein': 1.4, 'fat': 0.1, 'carbs': 24, 'fiber': 3, 'unit': 'per 100g'},
    'bison': {'calories': 143, 'protein': 28, 'fat': 2.4, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'boar': {'calories': 122, 'protein': 21, 'fat': 3.3, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'cornish_hen': {'calories': 220, 'protein': 23, 'fat': 14, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'elk': {'calories': 111, 'protein': 23, 'fat': 1.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'frog_legs': {'calories': 73, 'protein': 16, 'fat': 0.3, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'goat': {'calories': 143, 'protein': 27, 'fat': 3, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'guinea_fowl': {'calories': 110, 'protein': 23, 'fat': 2.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'kangaroo': {'calories': 98, 'protein': 22, 'fat': 1.2, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'ostrich': {'calories': 142, 'protein': 27, 'fat': 2.8, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'partridge': {'calories': 105, 'protein': 25, 'fat': 1, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'pheasant': {'calories': 133, 'protein': 24, 'fat': 3.6, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'pigeon': {'calories': 142, 'protein': 18, 'fat': 7.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'rabbit': {'calories': 173, 'protein': 33, 'fat': 3.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'snail': {'calories': 90, 'protein': 16, 'fat': 1.4, 'carbs': 2, 'fiber': 0, 'unit': 'per 100g'},
    'turkey_bacon': {'calories': 226, 'protein': 30, 'fat': 11, 'carbs': 1.5, 'fiber': 0, 'unit': 'per 100g'},
    'abalone': {'calories': 105, 'protein': 17, 'fat': 0.8, 'carbs': 6, 'fiber': 0, 'unit': 'per 100g'},
    'barramundi': {'calories': 113, 'protein': 20, 'fat': 3.6, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'bluefish': {'calories': 124, 'protein': 20, 'fat': 4.2, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'carp': {'calories': 127, 'protein': 18, 'fat': 5.6, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'conch': {'calories': 130, 'protein': 26, 'fat': 1.2, 'carbs': 3, 'fiber': 0, 'unit': 'per 100g'},
    'crawfish': {'calories': 77, 'protein': 16, 'fat': 1, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'grouper': {'calories': 92, 'protein': 19, 'fat': 1, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'kingfish': {'calories': 105, 'protein': 20, 'fat': 2.2, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'monkfish': {'calories': 76, 'protein': 14, 'fat': 1.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'perch': {'calories': 91, 'protein': 19, 'fat': 0.9, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'pike': {'calories': 88, 'protein': 19, 'fat': 0.7, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'pollock': {'calories': 92, 'protein': 19, 'fat': 1, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'pompano': {'calories': 164, 'protein': 18, 'fat': 9.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'rockfish': {'calories': 94, 'protein': 19, 'fat': 1.6, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'sea_urchin': {'calories': 172, 'protein': 13, 'fat': 4.2, 'carbs': 2.5, 'fiber': 0, 'unit': 'per 100g'},
    'sole': {'calories': 70, 'protein': 12, 'fat': 1.9, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'sturgeon': {'calories': 105, 'protein': 16, 'fat': 4, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'trout_rainbow': {'calories': 119, 'protein': 20, 'fat': 3.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'turbot': {'calories': 95, 'protein': 16, 'fat': 3, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'yellowtail': {'calories': 146, 'protein': 23, 'fat': 5.2, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'adobo': {'calories': 180, 'protein': 15, 'fat': 10, 'carbs': 8, 'fiber': 1, 'unit': 'per 100g'},
    'arancini': {'calories': 250, 'protein': 8, 'fat': 12, 'carbs': 28, 'fiber': 1.5, 'unit': 'per 100g'},
    'baba_ganoush': {'calories': 120, 'protein': 2, 'fat': 10, 'carbs': 8, 'fiber': 3, 'unit': 'per 100g'},
    'biryani': {'calories': 170, 'protein': 7, 'fat': 6, 'carbs': 24, 'fiber': 1.5, 'unit': 'per 100g'},
    'boeuf_bourguignon': {'calories': 180, 'protein': 16, 'fat': 10, 'carbs': 6, 'fiber': 1, 'unit': 'per 100g'},
    'bulgogi': {'calories': 195, 'protein': 18, 'fat': 11, 'carbs': 6, 'fiber': 0.5, 'unit': 'per 100g'},
    'burrito': {'calories': 206, 'protein': 10, 'fat': 8, 'carbs': 25, 'fiber': 3, 'unit': 'per 100g'},
    'cassoulet': {'calories': 165, 'protein': 12, 'fat': 8, 'carbs': 12, 'fiber': 3, 'unit': 'per 100g'},
    'chicken_adobo': {'calories': 185, 'protein': 16, 'fat': 11, 'carbs': 5, 'fiber': 0.5, 'unit': 'per 100g'},
    'chicken_tikka_masala': {'calories': 150, 'protein': 14, 'fat': 8, 'carbs': 7, 'fiber': 1, 'unit': 'per 100g'},
    'chili_con_carne': {'calories': 140, 'protein': 12, 'fat': 6, 'carbs': 10, 'fiber': 3, 'unit': 'per 100g'},
    'chimichanga': {'calories': 245, 'protein': 12, 'fat': 13, 'carbs': 22, 'fiber': 2.5, 'unit': 'per 100g'},
    'coq_au_vin': {'calories': 175, 'protein': 18, 'fat': 9, 'carbs': 4, 'fiber': 0.5, 'unit': 'per 100g'},
    'croquettes': {'calories': 220, 'protein': 8, 'fat': 12, 'carbs': 20, 'fiber': 1.5, 'unit': 'per 100g'},
    'dal': {'calories': 105, 'protein': 7, 'fat': 2, 'carbs': 17, 'fiber': 4, 'unit': 'per 100g'},
    'dim_sum': {'calories': 180, 'protein': 7, 'fat': 8, 'carbs': 20, 'fiber': 1, 'unit': 'per 100g'},
    'dolma': {'calories': 140, 'protein': 5, 'fat': 7, 'carbs': 16, 'fiber': 2, 'unit': 'per 100g'},
    'empanada': {'calories': 280, 'protein': 8, 'fat': 15, 'carbs': 28, 'fiber': 1.5, 'unit': 'per 100g'},
    'enchilada': {'calories': 190, 'protein': 10, 'fat': 9, 'carbs': 18, 'fiber': 2.5, 'unit': 'per 100g'},
    'fajitas': {'calories': 160, 'protein': 14, 'fat': 7, 'carbs': 12, 'fiber': 2, 'unit': 'per 100g'},
    'feijoada': {'calories': 155, 'protein': 12, 'fat': 8, 'carbs': 10, 'fiber': 3, 'unit': 'per 100g'},
    'fondue': {'calories': 240, 'protein': 15, 'fat': 18, 'carbs': 3, 'fiber': 0, 'unit': 'per 100g'},
    'goulash': {'calories': 130, 'protein': 12, 'fat': 6, 'carbs': 8, 'fiber': 1.5, 'unit': 'per 100g'},
    'jambalaya': {'calories': 145, 'protein': 9, 'fat': 5, 'carbs': 17, 'fiber': 1.5, 'unit': 'per 100g'},
    'katsu': {'calories': 250, 'protein': 20, 'fat': 14, 'carbs': 12, 'fiber': 0.5, 'unit': 'per 100g'},
    'kebab': {'calories': 210, 'protein': 18, 'fat': 13, 'carbs': 5, 'fiber': 1, 'unit': 'per 100g'},
    'kimchi': {'calories': 15, 'protein': 1.1, 'fat': 0.5, 'carbs': 2.4, 'fiber': 1.6, 'unit': 'per 100g'},
    'korma': {'calories': 175, 'protein': 12, 'fat': 11, 'carbs': 8, 'fiber': 1.5, 'unit': 'per 100g'},
    'laksa': {'calories': 140, 'protein': 8, 'fat': 7, 'carbs': 13, 'fiber': 1.5, 'unit': 'per 100ml'},
    'moussaka': {'calories': 160, 'protein': 9, 'fat': 10, 'carbs': 10, 'fiber': 2, 'unit': 'per 100g'},
    'nasi_goreng': {'calories': 175, 'protein': 6, 'fat': 7, 'carbs': 23, 'fiber': 1.5, 'unit': 'per 100g'},
    'osso_buco': {'calories': 195, 'protein': 20, 'fat': 11, 'carbs': 3, 'fiber': 0.5, 'unit': 'per 100g'},
    'paella_seafood': {'calories': 145, 'protein': 11, 'fat': 4, 'carbs': 18, 'fiber': 1, 'unit': 'per 100g'},
    'panang_curry': {'calories': 155, 'protein': 10, 'fat': 9, 'carbs': 10, 'fiber': 2, 'unit': 'per 100g'},
    'pho_beef': {'calories': 95, 'protein': 7, 'fat': 2.5, 'carbs': 12, 'fiber': 1, 'unit': 'per 100ml'},
    'pierogi': {'calories': 200, 'protein': 6, 'fat': 7, 'carbs': 28, 'fiber': 2, 'unit': 'per 100g'},
    'poke_bowl': {'calories': 140, 'protein': 15, 'fat': 4, 'carbs': 14, 'fiber': 2, 'unit': 'per 100g'},
    'quesadilla': {'calories': 210, 'protein': 11, 'fat': 11, 'carbs': 18, 'fiber': 1.5, 'unit': 'per 100g'},
    'ratatouille': {'calories': 55, 'protein': 1.5, 'fat': 3, 'carbs': 7, 'fiber': 2.5, 'unit': 'per 100g'},
    'rendang': {'calories': 195, 'protein': 16, 'fat': 12, 'carbs': 6, 'fiber': 1, 'unit': 'per 100g'},
    'satay': {'calories': 220, 'protein': 18, 'fat': 14, 'carbs': 6, 'fiber': 1, 'unit': 'per 100g'},
    'schnitzel': {'calories': 245, 'protein': 22, 'fat': 14, 'carbs': 10, 'fiber': 0.5, 'unit': 'per 100g'},
    'shawarma': {'calories': 195, 'protein': 16, 'fat': 11, 'carbs': 9, 'fiber': 1.5, 'unit': 'per 100g'},
    'shepherd_pie': {'calories': 120, 'protein': 8, 'fat': 5, 'carbs': 12, 'fiber': 2, 'unit': 'per 100g'},
    'souvlaki': {'calories': 200, 'protein': 18, 'fat': 12, 'carbs': 5, 'fiber': 1, 'unit': 'per 100g'},
    'spanakopita': {'calories': 240, 'protein': 8, 'fat': 16, 'carbs': 18, 'fiber': 2, 'unit': 'per 100g'},
    'tandoori_chicken': {'calories': 170, 'protein': 24, 'fat': 7, 'carbs': 2, 'fiber': 0.5, 'unit': 'per 100g'},
    'tempura': {'calories': 200, 'protein': 8, 'fat': 10, 'carbs': 20, 'fiber': 1, 'unit': 'per 100g'},
    'tikka': {'calories': 165, 'protein': 18, 'fat': 8, 'carbs': 4, 'fiber': 1, 'unit': 'per 100g'},
    'tom_yum': {'calories': 45, 'protein': 3, 'fat': 1.5, 'carbs': 6, 'fiber': 1, 'unit': 'per 100ml'},
    'tonkatsu': {'calories': 260, 'protein': 21, 'fat': 15, 'carbs': 12, 'fiber': 0.5, 'unit': 'per 100g'},
    'vindaloo': {'calories': 160, 'protein': 14, 'fat': 9, 'carbs': 7, 'fiber': 1.5, 'unit': 'per 100g'},
    'yakitori': {'calories': 185, 'protein': 22, 'fat': 9, 'carbs': 3, 'fiber': 0.5, 'unit': 'per 100g'},
    'affogato': {'calories': 120, 'protein': 2.5, 'fat': 6, 'carbs': 14, 'fiber': 0, 'unit': 'per 100ml'},
    'banoffee_pie': {'calories': 320, 'protein': 3, 'fat': 18, 'carbs': 38, 'fiber': 1, 'unit': 'per 100g'},
    'blondie': {'calories': 420, 'protein': 5, 'fat': 20, 'carbs': 55, 'fiber': 1, 'unit': 'per 100g'},
    'boston_cream_pie': {'calories': 280, 'protein': 4, 'fat': 14, 'carbs': 35, 'fiber': 0.5, 'unit': 'per 100g'},
    'bread_pudding': {'calories': 212, 'protein': 5.5, 'fat': 8, 'carbs': 30, 'fiber': 1, 'unit': 'per 100g'},
    'butter_tart': {'calories': 380, 'protein': 3.5, 'fat': 18, 'carbs': 50, 'fiber': 0.8, 'unit': 'per 100g'},
    'cannoli': {'calories': 298, 'protein': 6, 'fat': 15, 'carbs': 35, 'fiber': 1, 'unit': 'per 100g'},
    'cobbler': {'calories': 195, 'protein': 2, 'fat': 7, 'carbs': 32, 'fiber': 1.5, 'unit': 'per 100g'},
    'creme_caramel': {'calories': 140, 'protein': 4, 'fat': 4, 'carbs': 22, 'fiber': 0, 'unit': 'per 100g'},
    'eclair': {'calories': 262, 'protein': 6, 'fat': 16, 'carbs': 24, 'fiber': 0.5, 'unit': 'per 100g'},
    'flan': {'calories': 140, 'protein': 4, 'fat': 4, 'carbs': 22, 'fiber': 0, 'unit': 'per 100g'},
    'gelato': {'calories': 190, 'protein': 3.5, 'fat': 8, 'carbs': 26, 'fiber': 0, 'unit': 'per 100g'},
    'key_lime_pie': {'calories': 320, 'protein': 4, 'fat': 16, 'carbs': 40, 'fiber': 0.5, 'unit': 'per 100g'},
    'lemon_bar': {'calories': 360, 'protein': 4, 'fat': 16, 'carbs': 52, 'fiber': 0.5, 'unit': 'per 100g'},
    'meringue': {'calories': 381, 'protein': 5.2, 'fat': 0.2, 'carbs': 95, 'fiber': 0, 'unit': 'per 100g'},
    'mochi': {'calories': 250, 'protein': 4, 'fat': 0.5, 'carbs': 58, 'fiber': 1, 'unit': 'per 100g'},
    'mousse': {'calories': 250, 'protein': 4, 'fat': 17, 'carbs': 22, 'fiber': 1, 'unit': 'per 100g'},
    'pavlova': {'calories': 280, 'protein': 3, 'fat': 8, 'carbs': 50, 'fiber': 0.5, 'unit': 'per 100g'},
    'pecan_pie': {'calories': 503, 'protein': 6, 'fat': 27, 'carbs': 64, 'fiber': 2, 'unit': 'per 100g'},
    'profiterole': {'calories': 280, 'protein': 5, 'fat': 16, 'carbs': 28, 'fiber': 0.5, 'unit': 'per 100g'},
    'pumpkin_pie': {'calories': 243, 'protein': 4.5, 'fat': 11, 'carbs': 32, 'fiber': 2, 'unit': 'per 100g'},
    'sorbet': {'calories': 130, 'protein': 0.5, 'fat': 0, 'carbs': 34, 'fiber': 1, 'unit': 'per 100g'},
    'souffle': {'calories': 180, 'protein': 7, 'fat': 11, 'carbs': 13, 'fiber': 0, 'unit': 'per 100g'},
    'trifle': {'calories': 200, 'protein': 3, 'fat': 8, 'carbs': 30, 'fiber': 0.5, 'unit': 'per 100g'},
    'acai_bowl': {'calories': 210, 'protein': 3, 'fat': 6, 'carbs': 38, 'fiber': 7, 'unit': 'per 100g'},
    'avocado_toast': {'calories': 195, 'protein': 6, 'fat': 11, 'carbs': 19, 'fiber': 5, 'unit': 'per 100g'},
    'bagel_with_cream_cheese': {'calories': 290, 'protein': 10, 'fat': 11, 'carbs': 38, 'fiber': 2, 'unit': 'per 100g'},
    'breakfast_sandwich': {'calories': 260, 'protein': 14, 'fat': 14, 'carbs': 20, 'fiber': 1.5, 'unit': 'per 100g'},
    'chilaquiles': {'calories': 180, 'protein': 8, 'fat': 10, 'carbs': 16, 'fiber': 2.5, 'unit': 'per 100g'},
    'congee': {'calories': 65, 'protein': 1.5, 'fat': 0.2, 'carbs': 14, 'fiber': 0.2, 'unit': 'per 100g'},
    'crepe': {'calories': 227, 'protein': 6, 'fat': 9, 'carbs': 28, 'fiber': 1, 'unit': 'per 100g'},
    'frittata': {'calories': 150, 'protein': 10, 'fat': 11, 'carbs': 3, 'fiber': 0.5, 'unit': 'per 100g'},
    'granola': {'calories': 471, 'protein': 13, 'fat': 20, 'carbs': 61, 'fiber': 8.9, 'unit': 'per 100g'},
    'hash_browns': {'calories': 265, 'protein': 3, 'fat': 17, 'carbs': 27, 'fiber': 2.5, 'unit': 'per 100g'},
    'muesli': {'calories': 352, 'protein': 10, 'fat': 5.5, 'carbs': 66, 'fiber': 7.7, 'unit': 'per 100g'},
    'overnight_oats': {'calories': 150, 'protein': 5, 'fat': 3, 'carbs': 27, 'fiber': 4, 'unit': 'per 100g'},
    'quiche': {'calories': 240, 'protein': 11, 'fat': 17, 'carbs': 11, 'fiber': 0.5, 'unit': 'per 100g'},
    'shakshuka': {'calories': 120, 'protein': 7, 'fat': 8, 'carbs': 6, 'fiber': 2, 'unit': 'per 100g'},
    'smoothie_bowl': {'calories': 150, 'protein': 4, 'fat': 3, 'carbs': 28, 'fiber': 5, 'unit': 'per 100g'},
    'biscuit': {'calories': 353, 'protein': 6.6, 'fat': 16, 'carbs': 45, 'fiber': 1.6, 'unit': 'per 100g'},
    'bread_whole_wheat': {'calories': 247, 'protein': 13, 'fat': 3.4, 'carbs': 41, 'fiber': 7, 'unit': 'per 100g'},
    'buckwheat': {'calories': 343, 'protein': 13, 'fat': 3.4, 'carbs': 72, 'fiber': 10, 'unit': 'per 100g'},
    'cereal_corn_flakes': {'calories': 357, 'protein': 7.5, 'fat': 0.4, 'carbs': 84, 'fiber': 3, 'unit': 'per 100g'},
    'cereal_oatmeal': {'calories': 68, 'protein': 2.4, 'fat': 1.4, 'carbs': 12, 'fiber': 1.7, 'unit': 'per 100g'},
    'crackers': {'calories': 502, 'protein': 8.2, 'fat': 24, 'carbs': 62, 'fiber': 2.5, 'unit': 'per 100g'},
    'croutons': {'calories': 407, 'protein': 11, 'fat': 7, 'carbs': 74, 'fiber': 5, 'unit': 'per 100g'},
    'farro': {'calories': 340, 'protein': 15, 'fat': 2.5, 'carbs': 67, 'fiber': 10, 'unit': 'per 100g'},
    'focaccia': {'calories': 271, 'protein': 7.6, 'fat': 5.4, 'carbs': 48, 'fiber': 2.1, 'unit': 'per 100g'},
    'grits': {'calories': 59, 'protein': 1.5, 'fat': 0.3, 'carbs': 13, 'fiber': 0.5, 'unit': 'per 100g'},
    'millet': {'calories': 378, 'protein': 11, 'fat': 4.2, 'carbs': 73, 'fiber': 8.5, 'unit': 'per 100g'},
    'naan': {'calories': 262, 'protein': 8.7, 'fat': 5.1, 'carbs': 45, 'fiber': 2.3, 'unit': 'per 100g'},
    'orzo': {'calories': 344, 'protein': 12, 'fat': 1.8, 'carbs': 71, 'fiber': 3, 'unit': 'per 100g'},
    'pita_bread': {'calories': 275, 'protein': 9.1, 'fat': 1.2, 'carbs': 55, 'fiber': 2.2, 'unit': 'per 100g'},
    'popcorn': {'calories': 387, 'protein': 13, 'fat': 4.5, 'carbs': 78, 'fiber': 15, 'unit': 'per 100g'},
    'pumpernickel_bread': {'calories': 250, 'protein': 8.7, 'fat': 3.1, 'carbs': 47, 'fiber': 6.5, 'unit': 'per 100g'},
    'rice_cakes': {'calories': 387, 'protein': 8.2, 'fat': 3.1, 'carbs': 82, 'fiber': 3.8, 'unit': 'per 100g'},
    'rye_bread': {'calories': 259, 'protein': 8.5, 'fat': 3.3, 'carbs': 48, 'fiber': 5.8, 'unit': 'per 100g'},
    'soba_noodles': {'calories': 99, 'protein': 5.1, 'fat': 0.1, 'carbs': 21, 'fiber': 0, 'unit': 'per 100g'},
    'spaghetti': {'calories': 158, 'protein': 5.8, 'fat': 0.9, 'carbs': 31, 'fiber': 1.8, 'unit': 'per 100g'},
    'teff': {'calories': 367, 'protein': 13, 'fat': 2.4, 'carbs': 73, 'fiber': 8, 'unit': 'per 100g'},
    'udon_noodles': {'calories': 99, 'protein': 2.6, 'fat': 0.5, 'carbs': 21, 'fiber': 0, 'unit': 'per 100g'},
    'wild_rice': {'calories': 101, 'protein': 4, 'fat': 0.3, 'carbs': 21, 'fiber': 1.8, 'unit': 'per 100g'},
    'brie': {'calories': 334, 'protein': 21, 'fat': 28, 'carbs': 0.5, 'fiber': 0, 'unit': 'per 100g'},
    'buttermilk': {'calories': 40, 'protein': 3.3, 'fat': 0.9, 'carbs': 4.8, 'fiber': 0, 'unit': 'per 100ml'},
    'cheddar_cheese': {'calories': 403, 'protein': 25, 'fat': 33, 'carbs': 1.3, 'fiber': 0, 'unit': 'per 100g'},
    'cream_cheese': {'calories': 342, 'protein': 6, 'fat': 34, 'carbs': 4.1, 'fiber': 0, 'unit': 'per 100g'},
    'egg_yolk': {'calories': 322, 'protein': 16, 'fat': 27, 'carbs': 3.6, 'fiber': 0, 'unit': 'per 100g'},
    'goat_cheese': {'calories': 364, 'protein': 22, 'fat': 30, 'carbs': 2.2, 'fiber': 0, 'unit': 'per 100g'},
    'greek_yogurt': {'calories': 59, 'protein': 10, 'fat': 0.4, 'carbs': 3.6, 'fiber': 0, 'unit': 'per 100g'},
    'half_and_half': {'calories': 130, 'protein': 3, 'fat': 12, 'carbs': 4.3, 'fiber': 0, 'unit': 'per 100ml'},
    'kefir': {'calories': 41, 'protein': 3.3, 'fat': 1, 'carbs': 4.5, 'fiber': 0, 'unit': 'per 100ml'},
    'milk_almond': {'calories': 17, 'protein': 0.6, 'fat': 1.1, 'carbs': 1.5, 'fiber': 0.2, 'unit': 'per 100ml'},
    'milk_oat': {'calories': 47, 'protein': 1, 'fat': 1.5, 'carbs': 7.5, 'fiber': 0.8, 'unit': 'per 100ml'},
    'milk_soy': {'calories': 54, 'protein': 3.3, 'fat': 1.8, 'carbs': 6, 'fiber': 0.6, 'unit': 'per 100ml'},
    'mozzarella': {'calories': 280, 'protein': 28, 'fat': 17, 'carbs': 3.1, 'fiber': 0, 'unit': 'per 100g'},
    'parmesan': {'calories': 431, 'protein': 38, 'fat': 29, 'carbs': 4.1, 'fiber': 0, 'unit': 'per 100g'},
    'queso_fresco': {'calories': 321, 'protein': 21, 'fat': 25, 'carbs': 4.1, 'fiber': 0, 'unit': 'per 100g'},
    'sour_cream': {'calories': 193, 'protein': 2.4, 'fat': 19, 'carbs': 4.6, 'fiber': 0, 'unit': 'per 100g'},
    'whipped_cream': {'calories': 257, 'protein': 2.2, 'fat': 28, 'carbs': 3.2, 'fiber': 0, 'unit': 'per 100g'},
    'almond_butter': {'calories': 614, 'protein': 21, 'fat': 56, 'carbs': 19, 'fiber': 10, 'unit': 'per 100g'},
    'cashew': {'calories': 553, 'protein': 18, 'fat': 44, 'carbs': 30, 'fiber': 3.3, 'unit': 'per 100g'},
    'chestnut': {'calories': 213, 'protein': 2.4, 'fat': 2.3, 'carbs': 45, 'fiber': 8.1, 'unit': 'per 100g'},
    'hazelnut': {'calories': 628, 'protein': 15, 'fat': 61, 'carbs': 17, 'fiber': 9.7, 'unit': 'per 100g'},
    'macadamia': {'calories': 718, 'protein': 7.9, 'fat': 76, 'carbs': 14, 'fiber': 8.6, 'unit': 'per 100g'},
    'peanut_butter': {'calories': 588, 'protein': 25, 'fat': 50, 'carbs': 20, 'fiber': 6, 'unit': 'per 100g'},
    'pine_nut': {'calories': 673, 'protein': 14, 'fat': 68, 'carbs': 13, 'fiber': 3.7, 'unit': 'per 100g'},
    'pumpkin_seeds': {'calories': 559, 'protein': 30, 'fat': 49, 'carbs': 11, 'fiber': 6, 'unit': 'per 100g'},
    'sunflower_seeds': {'calories': 584, 'protein': 21, 'fat': 51, 'carbs': 20, 'fiber': 8.6, 'unit': 'per 100g'},
    'walnut': {'calories': 654, 'protein': 15, 'fat': 65, 'carbs': 14, 'fiber': 6.7, 'unit': 'per 100g'},
    'chickpeas': {'calories': 164, 'protein': 8.9, 'fat': 2.6, 'carbs': 27, 'fiber': 7.6, 'unit': 'per 100g'},
    'lentils': {'calories': 116, 'protein': 9, 'fat': 0.4, 'carbs': 20, 'fiber': 7.9, 'unit': 'per 100g'},
    'mung_beans': {'calories': 105, 'protein': 7.0, 'fat': 0.4, 'carbs': 19, 'fiber': 7.6, 'unit': 'per 100g'},
    'pinto_beans': {'calories': 143, 'protein': 9, 'fat': 0.7, 'carbs': 26, 'fiber': 9, 'unit': 'per 100g'},
    'split_peas': {'calories': 118, 'protein': 8.3, 'fat': 0.4, 'carbs': 21, 'fiber': 8.3, 'unit': 'per 100g'},
    'tempeh': {'calories': 193, 'protein': 19, 'fat': 11, 'carbs': 9, 'fiber': 0, 'unit': 'per 100g'},
    'honey': {'calories': 304, 'protein': 0.3, 'fat': 0, 'carbs': 82, 'fiber': 0.2, 'unit': 'per 100g'},
    'ketchup': {'calories': 101, 'protein': 1.2, 'fat': 0.1, 'carbs': 27, 'fiber': 0.3, 'unit': 'per 100g'},
    'mayonnaise': {'calories': 680, 'protein': 1.1, 'fat': 75, 'carbs': 0.6, 'fiber': 0, 'unit': 'per 100g'},
    'olive_oil': {'calories': 884, 'protein': 0, 'fat': 100, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'ranch_dressing': {'calories': 479, 'protein': 1.4, 'fat': 50, 'carbs': 6.4, 'fiber': 0, 'unit': 'per 100g'},
    'soy_sauce': {'calories': 53, 'protein': 5.6, 'fat': 0.1, 'carbs': 4.9, 'fiber': 0.8, 'unit': 'per 100ml'},
    'teriyaki_sauce': {'calories': 89, 'protein': 5.9, 'fat': 0, 'carbs': 15, 'fiber': 0.3, 'unit': 'per 100ml'},
    'worcestershire_sauce': {'calories': 78, 'protein': 0, 'fat': 0, 'carbs': 19, 'fiber': 0, 'unit': 'per 100ml'},
    'black_coffee': {'calories': 2, 'protein': 0.3, 'fat': 0, 'carbs': 0, 'fiber': 0, 'unit': 'per 100ml'},
    'champagne': {'calories': 89, 'protein': 0.2, 'fat': 0, 'carbs': 1.4, 'fiber': 0, 'unit': 'per 100ml'},
    'coconut_water': {'calories': 19, 'protein': 0.7, 'fat': 0.2, 'carbs': 3.7, 'fiber': 1.1, 'unit': 'per 100ml'},
    'espresso': {'calories': 9, 'protein': 0.5, 'fat': 0.2, 'carbs': 1.6, 'fiber': 0, 'unit': 'per 100ml'},
    'hot_chocolate': {'calories': 77, 'protein': 3.5, 'fat': 2.3, 'carbs': 11, 'fiber': 1, 'unit': 'per 100ml'},
    'lemonade': {'calories': 40, 'protein': 0.1, 'fat': 0.1, 'carbs': 10, 'fiber': 0.1, 'unit': 'per 100ml'},
    'protein_shake': {'calories': 103, 'protein': 20, 'fat': 1.5, 'carbs': 3.5, 'fiber': 0.5, 'unit': 'per 100ml'},
    'smoothie': {'calories': 65, 'protein': 1.5, 'fat': 0.5, 'carbs': 15, 'fiber': 1.5, 'unit': 'per 100ml'},
    'sports_drink': {'calories': 25, 'protein': 0, 'fat': 0, 'carbs': 6, 'fiber': 0, 'unit': 'per 100ml'},
    'tomato_juice': {'calories': 17, 'protein': 0.8, 'fat': 0.1, 'carbs': 3.9, 'fiber': 0.4, 'unit': 'per 100ml'},
    'whiskey': {'calories': 250, 'protein': 0, 'fat': 0, 'carbs': 0, 'fiber': 0, 'unit': 'per 100ml'},
    'caramel': {'calories': 382, 'protein': 4.6, 'fat': 8.1, 'carbs': 77, 'fiber': 0, 'unit': 'per 100g'},
    'chocolate_milk': {'calories': 546, 'protein': 7.7, 'fat': 31, 'carbs': 59, 'fiber': 3.4, 'unit': 'per 100g'},
    'cookies': {'calories': 502, 'protein': 5.6, 'fat': 24, 'carbs': 67, 'fiber': 2, 'unit': 'per 100g'},
    'fruit_snacks': {'calories': 343, 'protein': 0, 'fat': 0, 'carbs': 86, 'fiber': 0, 'unit': 'per 100g'},
    'gummy_bears': {'calories': 325, 'protein': 6.9, 'fat': 0, 'carbs': 77, 'fiber': 0, 'unit': 'per 100g'},
    'licorice': {'calories': 375, 'protein': 3.8, 'fat': 0.8, 'carbs': 88, 'fiber': 0, 'unit': 'per 100g'},
    'popsicle': {'calories': 37, 'protein': 0, 'fat': 0, 'carbs': 9.4, 'fiber': 0, 'unit': 'per 100g'},
    'pudding': {'calories': 131, 'protein': 3.4, 'fat': 3.1, 'carbs': 23, 'fiber': 0.2, 'unit': 'per 100g'},
    'trail_mix': {'calories': 462, 'protein': 13, 'fat': 29, 'carbs': 45, 'fiber': 5, 'unit': 'per 100g'},
    'boysenberry': {'calories': 50, 'protein': 1.1, 'fat': 0.5, 'carbs': 12, 'fiber': 5.3, 'unit': 'per 100g'},
    'currant': {'calories': 63, 'protein': 1.4, 'fat': 0.2, 'carbs': 15, 'fiber': 4.3, 'unit': 'per 100g'},
    'gooseberry': {'calories': 44, 'protein': 0.9, 'fat': 0.6, 'carbs': 10, 'fiber': 4.3, 'unit': 'per 100g'},
    'mulberry': {'calories': 43, 'protein': 1.4, 'fat': 0.4, 'carbs': 10, 'fiber': 1.7, 'unit': 'per 100g'},
    'bean_sprouts': {'calories': 30, 'protein': 3, 'fat': 0.2, 'carbs': 6, 'fiber': 1.8, 'unit': 'per 100g'},
    'butternut_squash': {'calories': 45, 'protein': 1, 'fat': 0.1, 'carbs': 12, 'fiber': 2, 'unit': 'per 100g'},
    'chayote': {'calories': 19, 'protein': 0.8, 'fat': 0.1, 'carbs': 4.5, 'fiber': 1.7, 'unit': 'per 100g'},
    'jicama': {'calories': 38, 'protein': 0.7, 'fat': 0.1, 'carbs': 9, 'fiber': 4.9, 'unit': 'per 100g'},
    'lotus_root': {'calories': 74, 'protein': 2.6, 'fat': 0.1, 'carbs': 17, 'fiber': 4.9, 'unit': 'per 100g'},
    'radicchio': {'calories': 23, 'protein': 1.4, 'fat': 0.3, 'carbs': 4.5, 'fiber': 0.9, 'unit': 'per 100g'},
    'salsify': {'calories': 82, 'protein': 3.3, 'fat': 0.2, 'carbs': 18, 'fiber': 3.3, 'unit': 'per 100g'},
    'water_chestnut': {'calories': 97, 'protein': 1.4, 'fat': 0.1, 'carbs': 24, 'fiber': 3, 'unit': 'per 100g'},
    'boar': {'calories': 122, 'protein': 21, 'fat': 3.3, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'elk': {'calories': 111, 'protein': 23, 'fat': 1.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'goat': {'calories': 143, 'protein': 27, 'fat': 3, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'kangaroo': {'calories': 98, 'protein': 22, 'fat': 1.2, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'partridge': {'calories': 105, 'protein': 25, 'fat': 1, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'pigeon': {'calories': 142, 'protein': 18, 'fat': 7.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'snail': {'calories': 90, 'protein': 16, 'fat': 1.4, 'carbs': 2, 'fiber': 0, 'unit': 'per 100g'},
    'barramundi': {'calories': 113, 'protein': 20, 'fat': 3.6, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'carp': {'calories': 127, 'protein': 18, 'fat': 5.6, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'crawfish': {'calories': 77, 'protein': 16, 'fat': 1, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'kingfish': {'calories': 105, 'protein': 20, 'fat': 2.2, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'perch': {'calories': 91, 'protein': 19, 'fat': 0.9, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'pollock': {'calories': 92, 'protein': 19, 'fat': 1, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'rockfish': {'calories': 94, 'protein': 19, 'fat': 1.6, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'sole': {'calories': 70, 'protein': 12, 'fat': 1.9, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'trout_rainbow': {'calories': 119, 'protein': 20, 'fat': 3.5, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'yellowtail': {'calories': 146, 'protein': 23, 'fat': 5.2, 'carbs': 0, 'fiber': 0, 'unit': 'per 100g'},
    'arancini': {'calories': 250, 'protein': 8, 'fat': 12, 'carbs': 28, 'fiber': 1.5, 'unit': 'per 100g'},
    'biryani': {'calories': 170, 'protein': 7, 'fat': 6, 'carbs': 24, 'fiber': 1.5, 'unit': 'per 100g'},
    'bulgogi': {'calories': 195, 'protein': 18, 'fat': 11, 'carbs': 6, 'fiber': 0.5, 'unit': 'per 100g'},
    'cassoulet': {'calories': 165, 'protein': 12, 'fat': 8, 'carbs': 12, 'fiber': 3, 'unit': 'per 100g'},
    'chicken_tikka_masala': {'calories': 150, 'protein': 14, 'fat': 8, 'carbs': 7, 'fiber': 1, 'unit': 'per 100g'},
    'chimichanga': {'calories': 245, 'protein': 12, 'fat': 13, 'carbs': 22, 'fiber': 2.5, 'unit': 'per 100g'},
    'croquettes': {'calories': 220, 'protein': 8, 'fat': 12, 'carbs': 20, 'fiber': 1.5, 'unit': 'per 100g'},
    'dim_sum': {'calories': 180, 'protein': 7, 'fat': 8, 'carbs': 20, 'fiber': 1, 'unit': 'per 100g'},
    'empanada': {'calories': 280, 'protein': 8, 'fat': 15, 'carbs': 28, 'fiber': 1.5, 'unit': 'per 100g'},
    'fajitas': {'calories': 160, 'protein': 14, 'fat': 7, 'carbs': 12, 'fiber': 2, 'unit': 'per 100g'},
    'fondue': {'calories': 240, 'protein': 15, 'fat': 18, 'carbs': 3, 'fiber': 0, 'unit': 'per 100g'},
    'jambalaya': {'calories': 145, 'protein': 9, 'fat': 5, 'carbs': 17, 'fiber': 1.5, 'unit': 'per 100g'},
    'kebab': {'calories': 210, 'protein': 18, 'fat': 13, 'carbs': 5, 'fiber': 1, 'unit': 'per 100g'},
    'korma': {'calories': 175, 'protein': 12, 'fat': 11, 'carbs': 8, 'fiber': 1.5, 'unit': 'per 100g'},
    'moussaka': {'calories': 160, 'protein': 9, 'fat': 10, 'carbs': 10, 'fiber': 2, 'unit': 'per 100g'},
    'osso_buco': {'calories': 195, 'protein': 20, 'fat': 11, 'carbs': 3, 'fiber': 0.5, 'unit': 'per 100g'},
    'panang_curry': {'calories': 155, 'protein': 10, 'fat': 9, 'carbs': 10, 'fiber': 2, 'unit': 'per 100g'},
    'pierogi': {'calories': 200, 'protein': 6, 'fat': 7, 'carbs': 28, 'fiber': 2, 'unit': 'per 100g'},
    'quesadilla': {'calories': 210, 'protein': 11, 'fat': 11, 'carbs': 18, 'fiber': 1.5, 'unit': 'per 100g'},
    'rendang': {'calories': 195, 'protein': 16, 'fat': 12, 'carbs': 6, 'fiber': 1, 'unit': 'per 100g'},
    'schnitzel': {'calories': 245, 'protein': 22, 'fat': 14, 'carbs': 10, 'fiber': 0.5, 'unit': 'per 100g'},
    'shepherd_pie': {'calories': 120, 'protein': 8, 'fat': 5, 'carbs': 12, 'fiber': 2, 'unit': 'per 100g'},
    'spanakopita': {'calories': 240, 'protein': 8, 'fat': 16, 'carbs': 18, 'fiber': 2, 'unit': 'per 100g'},
    'tempura': {'calories': 200, 'protein': 8, 'fat': 10, 'carbs': 20, 'fiber': 1, 'unit': 'per 100g'},
    'tom_yum': {'calories': 45, 'protein': 3, 'fat': 1.5, 'carbs': 6, 'fiber': 1, 'unit': 'per 100ml'},
    'vindaloo': {'calories': 160, 'protein': 14, 'fat': 9, 'carbs': 7, 'fiber': 1.5, 'unit': 'per 100g'},
    'banoffee_pie': {'calories': 320, 'protein': 3, 'fat': 18, 'carbs': 38, 'fiber': 1, 'unit': 'per 100g'},
    'boston_cream_pie': {'calories': 280, 'protein': 4, 'fat': 14, 'carbs': 35, 'fiber': 0.5, 'unit': 'per 100g'},
    'butter_tart': {'calories': 380, 'protein': 3.5, 'fat': 18, 'carbs': 50, 'fiber': 0.8, 'unit': 'per 100g'},
    'cobbler': {'calories': 195, 'protein': 2, 'fat': 7, 'carbs': 32, 'fiber': 1.5, 'unit': 'per 100g'},
    'eclair': {'calories': 262, 'protein': 6, 'fat': 16, 'carbs': 24, 'fiber': 0.5, 'unit': 'per 100g'},
    'gelato': {'calories': 190, 'protein': 3.5, 'fat': 8, 'carbs': 26, 'fiber': 0, 'unit': 'per 100g'},
    'lemon_bar': {'calories': 360, 'protein': 4, 'fat': 16, 'carbs': 52, 'fiber': 0.5, 'unit': 'per 100g'},
    'mochi': {'calories': 250, 'protein': 4, 'fat': 0.5, 'carbs': 58, 'fiber': 1, 'unit': 'per 100g'},
    'pavlova': {'calories': 280, 'protein': 3, 'fat': 8, 'carbs': 50, 'fiber': 0.5, 'unit': 'per 100g'},
    'profiterole': {'calories': 280, 'protein': 5, 'fat': 16, 'carbs': 28, 'fiber': 0.5, 'unit': 'per 100g'},
    'sorbet': {'calories': 130, 'protein': 0.5, 'fat': 0, 'carbs': 34, 'fiber': 1, 'unit': 'per 100g'},
    'trifle': {'calories': 200, 'protein': 3, 'fat': 8, 'carbs': 30, 'fiber': 0.5, 'unit': 'per 100g'},
    'avocado_toast': {'calories': 195, 'protein': 6, 'fat': 11, 'carbs': 19, 'fiber': 5, 'unit': 'per 100g'},
    'breakfast_sandwich': {'calories': 260, 'protein': 14, 'fat': 14, 'carbs': 20, 'fiber': 1.5, 'unit': 'per 100g'},
    'congee': {'calories': 65, 'protein': 1.5, 'fat': 0.2, 'carbs': 14, 'fiber': 0.2, 'unit': 'per 100g'},
    'frittata': {'calories': 150, 'protein': 10, 'fat': 11, 'carbs': 3, 'fiber': 0.5, 'unit': 'per 100g'},
    'hash_browns': {'calories': 265, 'protein': 3, 'fat': 17, 'carbs': 27, 'fiber': 2.5, 'unit': 'per 100g'},
    'overnight_oats': {'calories': 150, 'protein': 5, 'fat': 3, 'carbs': 27, 'fiber': 4, 'unit': 'per 100g'},
    'shakshuka': {'calories': 120, 'protein': 7, 'fat': 8, 'carbs': 6, 'fiber': 2, 'unit': 'per 100g'},
}

class CalorieDatabase:
    """Manager for food calorie and nutritional information"""
    
    def __init__(self, db_path=None):
        """
        Initialize the calorie database.
        
        Args:
            db_path: Path to the calorie database CSV file
        """
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
        """
        Get nutritional information for a food item.
        
        Args:
            food_name: Name of the food (normalized)
            serving_size: Serving size in grams (default 100g)
            
        Returns:
            Dictionary with nutritional information
        """
        food_name = food_name.lower().strip()
        
        # Try exact match first
        if food_name in self.database:
            info = self.database[food_name].copy()
        else:
            # Try to find partial match
            matches = [key for key in self.database.keys() if food_name in key or key in food_name]
            if matches:
                info = self.database[matches[0]].copy()
            else:
                # Return default values if not found
                logger.warning(f"Food item '{food_name}' not found in database")
                return self._default_nutrition()
        
        # Calculate for serving size if needed
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
        """
        Add a new food item to the database.
        
        Args:
            food_name: Name of the food
            nutrition_info: Dictionary with nutritional values
        """
        self.database[food_name.lower()] = nutrition_info
        logger.info(f"Added food item: {food_name}")
    
    def search_food(self, query):
        """
        Search for foods matching a query.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching food names
        """
        query = query.lower()
        matches = [food for food in self.database.keys() if query in food]
        return sorted(matches)
    
    def get_all_foods(self):
        """Get list of all foods in database"""
        return sorted(list(self.database.keys()))
    
    def save_database(self, output_path=None):
        """
        Save database to CSV file.
        
        Args:
            output_path: Path to save the database
        """
        if output_path is None:
            output_path = self.db_path
        
        df = pd.DataFrame.from_dict(self.database, orient='index')
        df.index.name = 'food_name'
        df.to_csv(output_path)
        logger.info(f"Database saved to {output_path}")
    
    def export_to_json(self, output_path):
        """
        Export database to JSON format.
        
        Args:
            output_path: Path to save the JSON file
        """
        with open(output_path, 'w') as f:
            json.dump(self.database, f, indent=2)
        logger.info(f"Database exported to {output_path}")


def estimate_calories(food_name, quantity=100, unit='grams'):
    """
    Quick function to estimate calories for a food.
    
    Args:
        food_name: Name of the food
        quantity: Quantity of food
        unit: Unit of measurement ('grams', 'ml', 'pieces')
        
    Returns:
        Estimated calorie count
    """
    db = CalorieDatabase()
    info = db.get_nutrition_info(food_name, serving_size=quantity)
    return info.get('calories', 0)


def get_macronutrients(food_name, serving_size=100):
    """
    Get macronutrient breakdown for a food.
    
    Args:
        food_name: Name of the food
        serving_size: Serving size in grams
        
    Returns:
        Dictionary with macronutrient values
    """
    db = CalorieDatabase()
    info = db.get_nutrition_info(food_name, serving_size)
    return {
        'protein': info.get('protein', 0),
        'fat': info.get('fat', 0),
        'carbs': info.get('carbs', 0),
        'fiber': info.get('fiber', 0)
    }
