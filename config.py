"""
Configuration settings for the Food Recognition and Calorie Tracking System
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Create directories if they don't exist
for directory in [DATA_DIR, MODELS_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Model configurations
MODEL_CONFIG = {
    'name': 'food_recognition_model',
    'architecture': 'EfficientNetB3',  # Lightweight but accurate
    'input_size': (224, 224),
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.001,
    'validation_split': 0.2,
    'seed': 42
}

# Dataset configurations
DATASET_CONFIG = {
    'name': 'food-101',
    'train_dir': DATA_DIR / 'food-101' / 'images',
    'num_classes': 101,
    'min_images_per_class': 750,  # Roughly 750 images per food class
}

# Training configurations
TRAINING_CONFIG = {
    'augmentation': True,
    'use_pretrained': True,
    'gpu': True,
    'early_stopping_patience': 10,
    'reduce_lr_patience': 5,
    'checkpoint': True,
    'checkpoint_dir': MODELS_DIR / 'checkpoints'
}

# Inference configurations
INFERENCE_CONFIG = {
    'confidence_threshold': 0.3,
    'top_k': 5,  # Return top 5 predictions
    'model_path': MODELS_DIR / 'food_recognition_final.h5',
}

# Calorie database settings
CALORIE_DB_CONFIG = {
    'db_path': DATA_DIR / 'calorie_database.csv',
    'default_serving_size': 100,  # grams
}

# API configurations
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True,
}

# Streamlit configurations
STREAMLIT_CONFIG = {
    'page_title': 'Food Recognition & Calorie Tracker',
    'layout': 'wide',
    'theme': 'light'
}

# Logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}

# Food categories (101 classes in Food-101 dataset)
FOOD_CATEGORIES = [
    'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare',
    'beet_salad', 'beignets', 'bibimbap', 'bishop_bread', 'black_bean_soup',
    'black_eyed_peas', 'blood_orange', 'blow_fish', 'blueberry_pie', 'boiled_egg',
    'borscht', 'boston_cream_pie', 'bouillon', 'bread_pudding', 'breakfast_burrito',
    'breast_milk_ice_cream', 'brewed_coffee', 'brioche', 'brittle', 'broccoli',
    'broken_wheat_bread', 'brown_bread', 'brunch', 'bubble_tea', 'bucatini',
    'buddha_bowl', 'buffalo_wings', 'bugs_bunny', 'burritos', 'butter_noodles',
    'buttermilk_pancakes', 'caesar_salad', 'cannelloni', 'cant_see_toes',
    'cacio_e_pepe', 'caesar_salad', 'cakes', 'calzone', 'cambodian_food',
    'caramel', 'caramelize', 'carrot_cake', 'carrot_juice', 'cars_2',
    'cartwheel', 'cassava_cake', 'caviar', 'ceviche', 'cheese_ball',
    'cheese_plate', 'cheesecake', 'chef_salad', 'chemical_brothers', 'cherry_pie',
    'chicago_style_hot_dog', 'chicken_curry', 'chicken_fingers', 'chicken_teriyaki',
    'chickpea_curry', 'chief_keefs', 'chile_relleno', 'chinese_food',
    'chinese_noodles', 'chocolate_cake', 'chocolate_mousse', 'chocolate_syrup',
    'churro', 'chop_suey', 'chow_fun', 'chow_mein', 'christmas_cookie'
]
