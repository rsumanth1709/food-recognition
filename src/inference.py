"""
Inference module for food recognition and calorie estimation
"""
import numpy as np
from pathlib import Path
import logging
from src.calorie_database import CalorieDatabase
from config import INFERENCE_CONFIG, MODEL_CONFIG, FOOD_CATEGORIES

# Try to import TensorFlow, but don't fail if it's not available
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    tf = None

# Try to import image utils, but don't fail if dependencies are missing
try:
    from src.image_utils import load_and_preprocess_image, load_batch_images
    IMAGE_UTILS_AVAILABLE = True
except ImportError:
    IMAGE_UTILS_AVAILABLE = False
    load_and_preprocess_image = None
    load_batch_images = None

logger = logging.getLogger(__name__)


class FoodRecognitionInference:
    """Handle inference for food recognition and calorie estimation"""
    
    def __init__(self, model_path=None):
        """
        Initialize the inference engine.
        
        Args:
            model_path: Path to the trained model
        """
        self.model_path = model_path or INFERENCE_CONFIG['model_path']
        self.model = None
        self.calorie_db = CalorieDatabase()
        self.food_categories = FOOD_CATEGORIES
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        if not TF_AVAILABLE:
            logger.warning("TensorFlow is not installed. Model loading disabled.")
            logger.info("Install TensorFlow to enable food recognition: pip install tensorflow")
            return False
            
        if not Path(self.model_path).exists():
            logger.warning(f"Model file not found at {self.model_path}")
            logger.info("Make sure to train the model first")
            return False
        
        try:
            self.model = tf.keras.models.load_model(self.model_path)
            logger.info(f"Model loaded successfully from {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            return False
    
    def predict_single(self, image_path, top_k=5):
        """
        Predict food items in a single image.
        
        Args:
            image_path: Path to the image file
            top_k: Number of top predictions to return
            
        Returns:
            Dictionary with predictions and confidence scores
        """
        if self.model is None:
            logger.error("Model not loaded")
            return None
        
        try:
            # Load and preprocess image
            image = load_and_preprocess_image(image_path)
            if image is None:
                return None
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            # Make prediction
            predictions = self.model.predict(image, verbose=0)
            
            # Get top predictions
            top_indices = np.argsort(predictions[0])[-top_k:][::-1]
            
            results = {
                'image_path': str(image_path),
                'predictions': []
            }
            
            for idx in top_indices:
                food_name = self.food_categories[idx]
                confidence = float(predictions[0][idx])
                
                # Get calorie information
                nutrition = self.calorie_db.get_nutrition_info(food_name)
                
                results['predictions'].append({
                    'food_name': food_name.replace('_', ' '),
                    'class_index': int(idx),
                    'confidence': round(confidence, 4),
                    'calories': nutrition.get('calories', 'N/A'),
                    'protein': nutrition.get('protein', 'N/A'),
                    'fat': nutrition.get('fat', 'N/A'),
                    'carbs': nutrition.get('carbs', 'N/A'),
                    'fiber': nutrition.get('fiber', 'N/A'),
                })
            
            return results
        
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return None
    
    def predict_batch(self, image_paths, top_k=5):
        """
        Predict food items in multiple images.
        
        Args:
            image_paths: List of image file paths
            top_k: Number of top predictions per image
            
        Returns:
            List of prediction results
        """
        if self.model is None:
            logger.error("Model not loaded")
            return []
        
        images, valid_paths = load_batch_images(image_paths)
        if images is None:
            return []
        
        all_results = []
        
        for i, (image, path) in enumerate(zip(images, valid_paths)):
            # Make prediction
            image = np.expand_dims(image, axis=0)
            predictions = self.model.predict(image, verbose=0)
            
            # Get top predictions
            top_indices = np.argsort(predictions[0])[-top_k:][::-1]
            
            results = {
                'image_path': str(path),
                'predictions': []
            }
            
            for idx in top_indices:
                food_name = self.food_categories[idx]
                confidence = float(predictions[0][idx])
                
                nutrition = self.calorie_db.get_nutrition_info(food_name)
                
                results['predictions'].append({
                    'food_name': food_name.replace('_', ' '),
                    'class_index': int(idx),
                    'confidence': round(confidence, 4),
                    'calories': nutrition.get('calories', 'N/A'),
                })
            
            all_results.append(results)
        
        return all_results
    
    def estimate_meal_calories(self, image_path, quantity_percentage=1.0):
        """
        Estimate total calories for a meal from image.
        
        Args:
            image_path: Path to the meal image
            quantity_percentage: Percentage of estimated serving (0-2.0)
            
        Returns:
            Dictionary with calorie estimates
        """
        predictions = self.predict_single(image_path, top_k=1)
        
        if not predictions or not predictions['predictions']:
            return None
        
        top_prediction = predictions['predictions'][0]
        calories = top_prediction['calories']
        
        if isinstance(calories, (int, float)):
            estimated_calories = calories * quantity_percentage
            
            return {
                'food_item': top_prediction['food_name'],
                'confidence': top_prediction['confidence'],
                'estimated_calories': round(estimated_calories, 1),
                'serving_size': '100g',
                'quantity_factor': quantity_percentage,
                'nutrition': {
                    'protein': top_prediction['protein'],
                    'fat': top_prediction['fat'],
                    'carbs': top_prediction['carbs'],
                }
            }
        
        return None
    
    def get_food_alternatives(self, food_name, limit=5):
        """
        Get similar food alternatives from the database.
        
        Args:
            food_name: Name of the food
            limit: Number of alternatives to return
            
        Returns:
            List of similar foods with calorie info
        """
        similar_foods = self.calorie_db.search_food(food_name)
        
        alternatives = []
        for food in similar_foods[:limit]:
            info = self.calorie_db.get_nutrition_info(food)
            alternatives.append({
                'food_name': food.replace('_', ' '),
                'calories': info.get('calories', 'N/A'),
                'protein': info.get('protein', 'N/A'),
                'carbs': info.get('carbs', 'N/A'),
            })
        
        return alternatives
    
    def get_model_stats(self):
        """Get information about the model"""
        if self.model is None:
            return None
        
        return {
            'input_shape': tuple(self.model.input_shape[1:]),
            'output_shape': tuple(self.model.output_shape[1:]),
            'total_params': self.model.count_params(),
            'num_classes': len(self.food_categories),
            'model_path': str(self.model_path)
        }


class MealTracker:
    """Track daily meal intake and calorie consumption"""
    
    def __init__(self):
        """Initialize meal tracker"""
        self.meals = []
        self.daily_calories = 0
        self.daily_nutrition = {
            'protein': 0,
            'fat': 0,
            'carbs': 0,
            'fiber': 0
        }
    
    def add_meal(self, food_name, calories, nutrition_info, meal_type='other'):
        """
        Add a meal to the tracker.
        
        Args:
            food_name: Name of the food
            calories: Calorie content
            nutrition_info: Dictionary with nutritional values
            meal_type: Type of meal (breakfast, lunch, dinner, snack)
        """
        meal = {
            'food_name': food_name,
            'calories': calories,
            'meal_type': meal_type,
            'nutrition': nutrition_info,
            'timestamp': pd.Timestamp.now()
        }
        
        self.meals.append(meal)
        self.daily_calories += calories
        
        for key in self.daily_nutrition:
            if key in nutrition_info:
                self.daily_nutrition[key] += nutrition_info[key]
        
        logger.info(f"Added meal: {food_name} ({calories} cal)")
    
    def get_daily_summary(self):
        """Get summary of daily intake"""
        return {
            'total_calories': round(self.daily_calories, 1),
            'total_meals': len(self.meals),
            'nutrition': {k: round(v, 1) for k, v in self.daily_nutrition.items()},
            'meals': self.meals
        }
    
    def get_meal_breakdown(self):
        """Get breakdown by meal type"""
        breakdown = {}
        for meal in self.meals:
            meal_type = meal['meal_type']
            if meal_type not in breakdown:
                breakdown[meal_type] = {'count': 0, 'calories': 0}
            breakdown[meal_type]['count'] += 1
            breakdown[meal_type]['calories'] += meal['calories']
        
        return breakdown
    
    def get_calorie_warning(self, daily_limit=2000):
        """
        Get warning if daily limit exceeded.
        
        Args:
            daily_limit: Daily calorie limit
            
        Returns:
            Warning message or None
        """
        if self.daily_calories > daily_limit:
            excess = round(self.daily_calories - daily_limit, 1)
            return f"Warning: Exceeded daily limit by {excess} calories"
        
        remaining = round(daily_limit - self.daily_calories, 1)
        return f"Remaining daily allowance: {remaining} calories"
    
    def reset_daily(self):
        """Reset daily tracking"""
        self.meals = []
        self.daily_calories = 0
        self.daily_nutrition = {key: 0 for key in self.daily_nutrition}


# Import pandas for timestamps
try:
    import pandas as pd
except ImportError:
    pass


def quick_predict(image_path, model_path=None):
    """
    Quick function to make a prediction.
    
    Args:
        image_path: Path to image
        model_path: Path to model (optional)
        
    Returns:
        Prediction results
    """
    inference = FoodRecognitionInference(model_path)
    return inference.predict_single(image_path)
