"""
Food Recognition and Calorie Tracking System
Main package initialization
"""

__version__ = "1.0.0"
__author__ = "Food AI Team"
__description__ = "AI-powered food recognition and calorie tracking system"

# Import only the modules that don't require TensorFlow
from src.calorie_database import CalorieDatabase

# Try to import modules that may have optional dependencies
try:
    from src.model import FoodRecognitionModel
    MODEL_AVAILABLE = True
except ImportError:
    FoodRecognitionModel = None
    MODEL_AVAILABLE = False

try:
    from src.inference import FoodRecognitionInference, MealTracker
    INFERENCE_AVAILABLE = True
except ImportError:
    FoodRecognitionInference = None
    MealTracker = None
    INFERENCE_AVAILABLE = False

try:
    from src.image_utils import load_and_preprocess_image, augment_image
    IMAGE_UTILS_AVAILABLE = True
except ImportError:
    load_and_preprocess_image = None
    augment_image = None
    IMAGE_UTILS_AVAILABLE = False

__all__ = [
    'FoodRecognitionModel',
    'FoodRecognitionInference',
    'MealTracker',
    'CalorieDatabase',
    'load_and_preprocess_image',
    'augment_image',
    'MODEL_AVAILABLE',
    'INFERENCE_AVAILABLE',
    'IMAGE_UTILS_AVAILABLE'
]
