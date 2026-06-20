#!/usr/bin/env python
"""
Main training script for Food Recognition Model
Trains a multi-task learning model for food classification and calorie estimation
"""

import sys
import logging
from pathlib import Path

# Setup paths
sys.path.insert(0, str(Path(__file__).parent))

from src.model import FoodRecognitionModel
from config import MODEL_CONFIG, TRAINING_CONFIG, DATASET_CONFIG
import tensorflow as tf

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main training function"""
    
    logger.info("Starting Food Recognition Model Training")
    logger.info(f"TensorFlow version: {tf.__version__}")
    logger.info(f"GPU Available: {tf.test.is_built_with_cuda()}")
    
    # Create model manager
    model_manager = FoodRecognitionModel(num_classes=DATASET_CONFIG['num_classes'])
    
    # Build model
    logger.info("Building model architecture...")
    model_manager.build_model(use_pretrained=TRAINING_CONFIG['use_pretrained'])
    
    # Compile model
    logger.info("Compiling model...")
    model_manager.compile_model(learning_rate=MODEL_CONFIG['learning_rate'])
    
    # Get model summary
    model_manager.get_model_summary()
    
    # Train model
    train_dir = DATASET_CONFIG['train_dir']
    if train_dir.exists():
        logger.info(f"Starting training with data from {train_dir}")
        history = model_manager.train(
            str(train_dir),
            epochs=MODEL_CONFIG['epochs'],
            checkpoint_dir=TRAINING_CONFIG['checkpoint_dir']
        )
        
        # Plot training history
        logger.info("Plotting training history...")
        model_manager.plot_training_history(
            save_path=Path(TRAINING_CONFIG['checkpoint_dir']) / 'training_history.png'
        )
        
        # Save final model
        final_model_path = Path(TRAINING_CONFIG['checkpoint_dir']) / 'food_recognition_final.h5'
        model_manager.save_model(str(final_model_path))
        logger.info(f"✓ Training complete! Model saved to {final_model_path}")
    else:
        logger.error(f"Training data not found at {train_dir}")
        logger.info("Please download the Food-101 dataset from https://www.kaggle.com/dansbecker/food-101")
        logger.info(f"and extract it to {DATASET_CONFIG['train_dir']}")


if __name__ == '__main__':
    main()
