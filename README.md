# Food Recognition & Calorie Tracking System

A comprehensive AI-powered system to recognize food items from images and estimate their calorie content, enabling users to track their dietary intake and make informed food choices.

## 🎯 Features

- **Food Recognition**: Identifies 101 different food items using deep learning
- **Calorie Estimation**: Estimates calorie content using both lookup tables and regression
- **Multi-Task Learning**: Single model for both classification and regression
- **Web Interface**: Interactive Streamlit application
- **REST API**: Flask-based API for integration
- **Real-time Tracking**: Track daily meals and nutritional intake
- **Nutritional Analysis**: Detailed macronutrient breakdown (protein, fat, carbs, fiber)
- **User-Friendly**: Easy-to-use interface with image upload capability

## 📊 Architecture

### Model
- **Base**: EfficientNetB3 (transfer learning)
- **Classification Head**: Predicts 101 food classes with softmax activation
- **Regression Head**: Estimates calorie content
- **Multi-task Learning**: Joint optimization of classification and regression losses

### Stack
- **Backend**: Flask REST API
- **Frontend**: Streamlit Web Interface
- **ML Framework**: TensorFlow/Keras
- **Data Processing**: NumPy, Pandas, OpenCV, Albumentations
- **Database**: Calorie lookup (JSON/CSV format)

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone repository
cd d:\Projects\food

# Install dependencies
pip install -r requirements.txt

# (Optional) Configure GPU
# For CUDA 12.x: Install tensorflow-gpu with matching CUDA runtime
```

### 2. Download Dataset

Download the Food-101 dataset:

```bash
# Option 1: Manual download from Kaggle
# Visit: https://www.kaggle.com/dansbecker/food-101
# Extract to: ./data/food-101/

# Option 2: Using Kaggle API
kaggle datasets download -d dansbecker/food-101
unzip -q food-101.zip -d ./data/
```

### 3. Train Model

```bash
# Run training script
python train.py

# Or use Jupyter notebook for interactive training
jupyter notebook notebooks/01_food_recognition_training.ipynb
```

### 4. Launch Applications

#### Streamlit UI (Recommended)
```bash
streamlit run ui/app.py
```

#### Flask API
```bash
python src/api.py
```

Both will be available at:
- **Streamlit**: http://localhost:8501
- **Flask**: http://localhost:5000

## 📁 Project Structure

```
food/
├── data/
│   ├── food-101/              # Downloaded dataset
│   └── calorie_database.csv   # Calorie lookup table
├── models/
│   ├── checkpoints/           # Training checkpoints
│   └── food_recognition_final.h5
├── notebooks/
│   └── 01_food_recognition_training.ipynb
├── src/
│   ├── model.py              # Model architecture
│   ├── inference.py          # Inference engine & meal tracker
│   ├── calorie_database.py   # Calorie lookup system
│   ├── image_utils.py        # Image processing utilities
│   └── api.py                # Flask REST API
├── ui/
│   └── app.py                # Streamlit web interface
├── utils/
│   └── helpers.py            # Utility functions
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🎮 Usage

### Web Interface (Streamlit)

1. **Home**: View today's quick stats and meal summary
2. **Food Recognition**: Upload food image to identify items and get calorie info
3. **Add Meal**: Manually add meals with nutritional information
4. **Daily Summary**: View daily calorie intake and macronutrient breakdown
5. **Food Search**: Search the database for specific foods
6. **Analytics**: Visualize eating patterns and trends

### API Usage

#### Predict from Image
```bash
curl -X POST -F "file=@food_image.jpg" \
  http://localhost:5000/api/predict
```

Response:
```json
{
  "image_path": "food_image.jpg",
  "predictions": [
    {
      "food_name": "pizza",
      "class_index": 45,
      "confidence": 0.9234,
      "calories": 285,
      "protein": 12,
      "fat": 10,
      "carbs": 36,
      "fiber": 2
    }
  ]
}
```

#### Get Calorie Estimate
```bash
curl -X POST -F "file=@food_image.jpg" \
  -F "quantity_percentage=1.5" \
  http://localhost:5000/api/calorie-estimate
```

#### Add Meal to Tracker
```bash
curl -X POST http://localhost:5000/api/add-meal \
  -H "Content-Type: application/json" \
  -d '{
    "food_name": "chicken curry",
    "calories": 165,
    "nutrition": {"protein": 18, "fat": 8, "carbs": 6},
    "meal_type": "lunch"
  }'
```

#### Search Food Database
```bash
curl "http://localhost:5000/api/food-search?query=chicken"
```

#### Get Daily Summary
```bash
curl "http://localhost:5000/api/daily-summary?daily_limit=2000"
```

## 📊 Model Performance

### Expected Metrics (Food-101 Dataset)
- **Classification Accuracy**: ~80-85%
- **Top-5 Accuracy**: ~95-97%
- **Calorie Estimation MAE**: ±20-30 cal/100g
- **Training Time**: ~2-4 hours (GPU)

### Notes
- Actual performance depends on hardware and training configuration
- Transfer learning from ImageNet provides strong initial performance
- Fine-tuning on Food-101 improves domain-specific accuracy

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Model settings
MODEL_CONFIG = {
    'architecture': 'EfficientNetB3',
    'input_size': (224, 224),
    'batch_size': 32,
    'epochs': 50,
    'learning_rate': 0.001
}

# Training settings
TRAINING_CONFIG = {
    'augmentation': True,
    'use_pretrained': True,
    'early_stopping_patience': 10,
    'reduce_lr_patience': 5
}

# API settings
API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'debug': True
}
```

## 📦 Dependencies

### Core Libraries
- TensorFlow 2.13.0+
- Keras 2.13.0+
- PyTorch (optional, for alternative models)
- NumPy, Pandas, Matplotlib, Seaborn

### ML/CV
- scikit-learn
- OpenCV (cv2)
- Albumentations
- Pillow

### Web/API
- Flask, Flask-CORS
- Streamlit, Streamlit-option-menu
- Plotly (visualization)

### Utilities
- tqdm (progress bars)
- python-dotenv (environment management)
- requests (HTTP)

## 🎯 Use Cases

1. **Dietary Tracking**: Monitor daily calorie and macro intake
2. **Weight Management**: Track progress towards fitness goals
3. **Nutritional Analysis**: Understand eating patterns and balance
4. **Restaurant Decision**: Compare calorie content of menu items
5. **Health Monitoring**: Track diet for specific health conditions
6. **Meal Planning**: Plan balanced meals with calorie targets

## 🔮 Future Enhancements

- [ ] Advanced portion size detection
- [ ] Allergen detection and warnings
- [ ] Personalized recommendations
- [ ] Integration with fitness trackers
- [ ] Voice-based meal logging
- [ ] Multi-language support
- [ ] Mobile app (React Native/Flutter)
- [ ] Database synchronization across devices
- [ ] Social features (share meals, recipes)
- [ ] Advanced analytics (trends, patterns)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: support@foodtracker.ai
- Documentation: [Full Documentation](docs/)

## 🙏 Acknowledgments

- Food-101 Dataset: https://www.kaggle.com/dansbecker/food-101
- Transfer Learning: ImageNet pre-trained models
- Community: TensorFlow, Keras, and open-source ML community

## 📚 References

- EfficientNet: [Paper](https://arxiv.org/abs/1905.11946)
- Food-101 Dataset: [Paper](https://www.vision.ee.ethz.ch/datasets/food-101/)
- Multi-task Learning: [Survey](https://arxiv.org/abs/1707.08114)
- Transfer Learning: [Guide](https://cs231n.github.io/transfer-learning/)

## ⚠️ Disclaimer

This system is intended for informational purposes and should not be used as a substitute for professional nutritional or medical advice. Always consult with healthcare professionals for personalized dietary recommendations.

---

**Happy Tracking! 🍎🥗💪**

Created with ❤️ for healthy living and informed food choices.
