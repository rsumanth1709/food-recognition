"""
Flask API for Food Recognition and Calorie Tracking
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import logging
from pathlib import Path
from src.inference import FoodRecognitionInference, MealTracker
from src.calorie_database import CalorieDatabase
from config import API_CONFIG

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize models
inference_engine = None
meal_tracker = MealTracker()
calorie_db = CalorieDatabase()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.before_request
def initialize_models():
    """Initialize models on first request"""
    global inference_engine
    if inference_engine is None:
        logger.info("Initializing inference engine...")
        inference_engine = FoodRecognitionInference()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': inference_engine is not None if inference_engine else False
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict food items from uploaded image.
    
    Request: POST with image file
    Response: JSON with predictions and nutrition info
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = app.config['UPLOAD_FOLDER'] + '/' + filename
        file.save(filepath)
        
        # Make prediction
        results = inference_engine.predict_single(filepath, top_k=5)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        if results:
            return jsonify(results)
        else:
            return jsonify({'error': 'Prediction failed'}), 500
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict-batch', methods=['POST'])
def predict_batch():
    """
    Predict food items from multiple images.
    
    Request: POST with multiple files
    Response: JSON array with predictions
    """
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        if not files:
            return jsonify({'error': 'No files selected'}), 400
        
        # Save files and collect paths
        file_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = app.config['UPLOAD_FOLDER'] + '/' + filename
                file.save(filepath)
                file_paths.append(filepath)
        
        if not file_paths:
            return jsonify({'error': 'No valid files'}), 400
        
        # Batch prediction
        results = inference_engine.predict_batch(file_paths, top_k=3)
        
        # Clean up
        for filepath in file_paths:
            os.remove(filepath)
        
        return jsonify({'predictions': results})
    
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/calorie-estimate', methods=['POST'])
def calorie_estimate():
    """
    Estimate calories from image with optional quantity adjustment.
    
    Request: POST with image and optional quantity_percentage
    Response: JSON with calorie estimate and nutrition
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        quantity_percentage = float(request.form.get('quantity_percentage', 1.0))
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = app.config['UPLOAD_FOLDER'] + '/' + filename
        file.save(filepath)
        
        # Estimate calories
        result = inference_engine.estimate_meal_calories(filepath, quantity_percentage)
        
        # Clean up
        os.remove(filepath)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Could not estimate calories'}), 500
    
    except Exception as e:
        logger.error(f"Calorie estimation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/add-meal', methods=['POST'])
def add_meal():
    """
    Add a meal to daily tracker.
    
    Request: POST with food_name, calories, nutrition, meal_type
    Response: JSON with updated daily summary
    """
    try:
        data = request.get_json()
        
        required_fields = ['food_name', 'calories']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        nutrition_info = data.get('nutrition', {})
        meal_type = data.get('meal_type', 'other')
        
        meal_tracker.add_meal(
            data['food_name'],
            data['calories'],
            nutrition_info,
            meal_type
        )
        
        return jsonify(meal_tracker.get_daily_summary())
    
    except Exception as e:
        logger.error(f"Error adding meal: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/daily-summary', methods=['GET'])
def daily_summary():
    """Get daily meal and calorie summary"""
    daily_limit = request.args.get('daily_limit', 2000, type=int)
    
    summary = meal_tracker.get_daily_summary()
    summary['warning'] = meal_tracker.get_calorie_warning(daily_limit)
    summary['breakdown'] = meal_tracker.get_meal_breakdown()
    
    return jsonify(summary)


@app.route('/api/reset-daily', methods=['POST'])
def reset_daily():
    """Reset daily tracking"""
    meal_tracker.reset_daily()
    return jsonify({'status': 'Daily tracker reset'})


@app.route('/api/food-search', methods=['GET'])
def food_search():
    """
    Search for foods in the database.
    
    Query: ?query=<search_string>
    Response: JSON list of matching foods with nutrition info
    """
    query = request.args.get('query', '').strip()
    
    if not query:
        return jsonify({'error': 'Query required'}), 400
    
    matches = calorie_db.search_food(query)
    
    results = []
    for food in matches[:10]:  # Limit to 10 results
        info = calorie_db.get_nutrition_info(food)
        results.append({
            'food_name': food.replace('_', ' '),
            'calories': info.get('calories'),
            'protein': info.get('protein'),
            'fat': info.get('fat'),
            'carbs': info.get('carbs'),
            'fiber': info.get('fiber')
        })
    
    return jsonify({'results': results})


@app.route('/api/food-alternatives', methods=['GET'])
def food_alternatives():
    """
    Get alternative foods similar to the provided food.
    
    Query: ?food_name=<food_name>
    Response: JSON list of similar foods
    """
    food_name = request.args.get('food_name', '').strip()
    
    if not food_name:
        return jsonify({'error': 'Food name required'}), 400
    
    alternatives = inference_engine.get_food_alternatives(food_name, limit=5)
    
    return jsonify({'alternatives': alternatives})


@app.route('/api/nutrition-info/<food_name>', methods=['GET'])
def nutrition_info(food_name):
    """
    Get nutrition information for a specific food.
    
    Query: ?serving_size=<grams>
    Response: JSON with nutrition data
    """
    serving_size = request.args.get('serving_size', 100, type=int)
    
    info = calorie_db.get_nutrition_info(food_name, serving_size)
    
    return jsonify({
        'food_name': food_name.replace('_', ' '),
        'serving_size': f"{serving_size}g",
        'nutrition': info
    })


@app.route('/api/model-stats', methods=['GET'])
def model_stats():
    """Get information about the loaded model"""
    stats = inference_engine.get_model_stats() if inference_engine else None
    
    if stats:
        return jsonify(stats)
    else:
        return jsonify({'error': 'Model not loaded'}), 500


@app.route('/api/all-foods', methods=['GET'])
def all_foods():
    """Get list of all foods in database"""
    foods = calorie_db.get_all_foods()
    return jsonify({'foods': [f.replace('_', ' ') for f in foods]})


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    logger.info(f"Starting API server on {API_CONFIG['host']}:{API_CONFIG['port']}")
    app.run(
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        debug=API_CONFIG['debug']
    )
