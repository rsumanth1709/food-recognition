# Quick Start Guide - Food Recognition & Calorie Tracker

## 📋 Prerequisites

- Python 3.8+
- Git
- ~5GB disk space (for Food-101 dataset)
- (Optional) NVIDIA GPU for faster training

## ⚡ 5-Minute Quick Start

### Step 1: Clone and Setup (2 minutes)

```bash
# Navigate to project
cd d:\Projects\food

# Install dependencies
pip install -r requirements.txt

# Initialize project
python initialize.py
```

### Step 2: Download Dataset (2-3 minutes)

Option A - Manual Download:
1. Visit https://www.kaggle.com/dansbecker/food-101
2. Click "Download" button
3. Extract to `data/food-101/`

Option B - Kaggle CLI:
```bash
kaggle datasets download -d dansbecker/food-101
unzip -q food-101.zip -d data/
```

### Step 3: Launch UI (30 seconds)

```bash
streamlit run ui/app.py
```

Visit: http://localhost:8501

## 🎬 Next Steps

### Train the Model
```bash
python train.py
# Training takes 2-4 hours on GPU
```

### Start the API
```bash
python src/api.py
# Available at http://localhost:5000
```

### Use Jupyter Notebook
```bash
jupyter notebook notebooks/01_food_recognition_training.ipynb
```

## 💡 Common Tasks

### 1. Make Predictions
```python
from src.inference import FoodRecognitionInference

inference = FoodRecognitionInference(model_path='models/food_recognition_final.h5')
results = inference.predict_single('path/to/image.jpg')
print(results)
```

### 2. Add Meal to Tracker
```python
from src.inference import MealTracker

tracker = MealTracker()
tracker.add_meal('chicken curry', 165, {'protein': 18, 'fat': 8, 'carbs': 6})
summary = tracker.get_daily_summary()
print(summary)
```

### 3. Search Calorie Database
```python
from src.calorie_database import CalorieDatabase

db = CalorieDatabase()
matches = db.search_food('pizza')
print(matches)
```

### 4. Get Nutritional Info
```python
from src.calorie_database import estimate_calories

calories = estimate_calories('chicken_curry', quantity=150)
print(f"Calories for 150g: {calories}")
```

## 🐛 Troubleshooting

### Issue: "No module named 'tensorflow'"
```bash
pip install --upgrade tensorflow
```

### Issue: "Dataset not found"
```bash
# Download from: https://www.kaggle.com/dansbecker/food-101
# Extract to: data/food-101/
python initialize.py
```

### Issue: "CUDA Out of Memory"
- Reduce `BATCH_SIZE` in `config.py`
- Use CPU instead: Set `TRAINING_CONFIG['gpu'] = False`

### Issue: "Port 5000/8501 already in use"
```bash
# Change port in config.py
# Or kill existing process:
# Windows: taskkill /PID <process_id>
# Linux: kill -9 <process_id>
```

## 📊 Project Statistics

- **Dataset Size**: ~101K images (750+ per class)
- **Model Parameters**: ~10M (EfficientNetB3)
- **Training Time**: 2-4 hours (GPU)
- **Inference Time**: ~100ms per image
- **Model Size**: ~150MB (H5 format)

## 🎯 Performance Tips

1. **GPU Usage**: Install CUDA for 10-20x faster training
2. **Batch Size**: Increase for faster training (if GPU memory allows)
3. **Data Loading**: Enable caching for repeated epochs
4. **Early Stopping**: Prevents overfitting and saves time

## 📱 Using the Web Interface

### Home Page
- View today's meal summary
- Quick access to all features

### Food Recognition
- Upload food image
- See top-5 predictions with confidence scores
- View calorie and nutrition info
- Add meal to tracker with one click

### Add Meal
- Manually enter meal details
- Customize serving size
- Track specific meals

### Daily Summary
- View total calories consumed
- See macronutrient breakdown
- Compare to daily targets
- Track meal types

### Food Search
- Search 100+ foods by name
- Browse complete database
- Get instant nutrition info

### Analytics
- Visualize eating patterns
- Compare to daily goals
- Track trends over time

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/predict` | Predict from image |
| POST | `/api/calorie-estimate` | Estimate calories |
| POST | `/api/add-meal` | Add meal to tracker |
| GET | `/api/daily-summary` | Get daily summary |
| GET | `/api/food-search` | Search database |
| GET | `/api/health` | Health check |

## 📚 Documentation

- [README.md](README.md) - Full documentation
- [config.py](config.py) - Configuration reference
- [Notebook](notebooks/01_food_recognition_training.ipynb) - Interactive tutorial
- [API Docs](src/api.py) - API reference

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Project initialized: `python initialize.py`
- [ ] Dataset downloaded to `data/food-101/`
- [ ] Streamlit runs: `streamlit run ui/app.py`
- [ ] API runs: `python src/api.py`

## 🆘 Need Help?

1. Check [README.md](README.md) for detailed information
2. Review error messages carefully
3. Run `python initialize.py` to verify setup
4. Check Jupyter notebook for examples
5. See `config.py` for configuration options

## 🎓 Learning Resources

- [TensorFlow Transfer Learning](https://www.tensorflow.org/tutorials/images/transfer_learning)
- [EfficientNet Paper](https://arxiv.org/abs/1905.11946)
- [Multi-task Learning](https://arxiv.org/abs/1707.08114)
- [Food-101 Dataset Paper](https://www.vision.ee.ethz.ch/publications/papers/proceedings/papers/eth_biwi_00898.pdf)

---

**Happy food tracking! 🍎🥗💪**

For the latest updates, visit: [Project Repository](https://github.com/yourusername/food-tracker)
