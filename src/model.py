"""
Food Recognition Model - Training and evaluation
Using transfer learning with EfficientNet
"""
import numpy as np
import logging
from pathlib import Path
from config import MODEL_CONFIG, TRAINING_CONFIG, DATASET_CONFIG

# Try to import TensorFlow and related modules
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import EfficientNetB3
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.callbacks import (
        EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, TensorBoard
    )
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    tf = None
    keras = None
    layers = None
    models = None
    EfficientNetB3 = None
    ImageDataGenerator = None
    EarlyStopping = None
    ReduceLROnPlateau = None
    ModelCheckpoint = None
    TensorBoard = None

try:
    import matplotlib.pyplot as plt
    PLT_AVAILABLE = True
except ImportError:
    PLT_AVAILABLE = False
    plt = None

logger = logging.getLogger(__name__)


class FoodRecognitionModel:
    """Deep learning model for food recognition"""
    
    def __init__(self, num_classes=101):
        """
        Initialize the food recognition model.
        
        Args:
            num_classes: Number of food classes (default: 101 for Food-101 dataset)
        """
        self.num_classes = num_classes
        self.model = None
        self.history = None
        self.input_shape = (*MODEL_CONFIG['input_size'], 3)
    
    def build_model(self, use_pretrained=True):
        """
        Build the neural network model using transfer learning.
        
        Args:
            use_pretrained: Whether to use pretrained weights
            
        Returns:
            Compiled Keras model
        """
        logger.info(f"Building {MODEL_CONFIG['architecture']} model...")
        
        # Load pretrained base model
        base_model = EfficientNetB3(
            input_shape=self.input_shape,
            include_top=False,
            weights='imagenet' if use_pretrained else None
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Build custom top layers
        inputs = keras.Input(shape=self.input_shape)
        
        # Data augmentation layer
        x = layers.RandomFlip("horizontal")(inputs)
        x = layers.RandomRotation(0.2)(x)
        x = layers.RandomZoom(0.2)(x)
        
        # Normalization
        x = layers.Normalization()(x)
        
        # Base model
        x = base_model(x, training=False)
        
        # Global average pooling
        x = layers.GlobalAveragePooling2D()(x)
        
        # Dense layers with dropout
        x = layers.Dense(512, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.5)(x)
        
        x = layers.Dense(256, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.4)(x)
        
        x = layers.Dense(128, activation='relu')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Dropout(0.3)(x)
        
        # Output layer
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        self.model = models.Model(inputs, outputs)
        
        logger.info("Model built successfully")
        return self.model
    
    def compile_model(self, learning_rate=0.001):
        """
        Compile the model.
        
        Args:
            learning_rate: Learning rate for optimizer
        """
        optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        
        self.model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=[
                'accuracy',
                keras.metrics.TopKCategoricalAccuracy(k=5, name='top_5_accuracy')
            ]
        )
        
        logger.info("Model compiled successfully")
    
    def get_callbacks(self, checkpoint_dir):
        """
        Get training callbacks.
        
        Args:
            checkpoint_dir: Directory to save model checkpoints
            
        Returns:
            List of Keras callbacks
        """
        checkpoint_dir = Path(checkpoint_dir)
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=TRAINING_CONFIG['early_stopping_patience'],
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=TRAINING_CONFIG['reduce_lr_patience'],
                min_lr=1e-7,
                verbose=1
            ),
            ModelCheckpoint(
                filepath=str(checkpoint_dir / 'best_model.h5'),
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            TensorBoard(
                log_dir=str(checkpoint_dir / 'logs'),
                histogram_freq=1
            )
        ]
        
        return callbacks
    
    def prepare_data(self, train_dir, validation_split=0.2):
        """
        Prepare data generators for training.
        
        Args:
            train_dir: Path to training directory
            validation_split: Fraction of data to use for validation
            
        Returns:
            Tuple of (train_generator, validation_generator)
        """
        # Training data augmentation
        train_datagen = ImageDataGenerator(
            rescale=1.0/255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            validation_split=validation_split
        )
        
        # Load training data
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=MODEL_CONFIG['input_size'],
            batch_size=MODEL_CONFIG['batch_size'],
            class_mode='categorical',
            subset='training'
        )
        
        validation_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=MODEL_CONFIG['input_size'],
            batch_size=MODEL_CONFIG['batch_size'],
            class_mode='categorical',
            subset='validation'
        )
        
        logger.info(f"Data generators created - Train: {len(train_generator)}, Val: {len(validation_generator)}")
        
        return train_generator, validation_generator
    
    def train(self, train_dir, epochs=None, checkpoint_dir=None):
        """
        Train the model.
        
        Args:
            train_dir: Path to training data directory
            epochs: Number of epochs to train (default from config)
            checkpoint_dir: Directory to save checkpoints
            
        Returns:
            Training history
        """
        if epochs is None:
            epochs = MODEL_CONFIG['epochs']
        if checkpoint_dir is None:
            checkpoint_dir = TRAINING_CONFIG['checkpoint_dir']
        
        # Prepare data
        train_gen, val_gen = self.prepare_data(train_dir)
        
        # Get callbacks
        callbacks = self.get_callbacks(checkpoint_dir)
        
        # Train model
        logger.info(f"Starting training for {epochs} epochs...")
        self.history = self.model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        logger.info("Training completed")
        return self.history
    
    def evaluate(self, val_generator):
        """
        Evaluate model on validation data.
        
        Args:
            val_generator: Validation data generator
            
        Returns:
            Dictionary with evaluation metrics
        """
        logger.info("Evaluating model...")
        results = self.model.evaluate(val_generator)
        
        evaluation_results = {
            'loss': results[0],
            'accuracy': results[1],
            'top_5_accuracy': results[2]
        }
        
        logger.info(f"Evaluation Results: {evaluation_results}")
        return evaluation_results
    
    def save_model(self, save_path):
        """
        Save the trained model.
        
        Args:
            save_path: Path to save the model
        """
        self.model.save(save_path)
        logger.info(f"Model saved to {save_path}")
    
    def load_model(self, model_path):
        """
        Load a pretrained model.
        
        Args:
            model_path: Path to the model file
        """
        self.model = keras.models.load_model(model_path)
        logger.info(f"Model loaded from {model_path}")
    
    def plot_training_history(self, save_path=None):
        """
        Plot training history.
        
        Args:
            save_path: Path to save the plot
        """
        if self.history is None:
            logger.warning("No training history available")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        axes[0].plot(self.history.history['accuracy'], label='Training Accuracy')
        axes[0].plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Accuracy')
        axes[0].set_title('Model Accuracy')
        axes[0].legend()
        axes[0].grid(True)
        
        # Plot loss
        axes[1].plot(self.history.history['loss'], label='Training Loss')
        axes[1].plot(self.history.history['val_loss'], label='Validation Loss')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('Loss')
        axes[1].set_title('Model Loss')
        axes[1].legend()
        axes[1].grid(True)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Training history plot saved to {save_path}")
        
        plt.show()
    
    def get_model_summary(self):
        """Print model summary"""
        if self.model:
            self.model.summary()
        else:
            logger.warning("Model not built yet")


def create_and_train_model(train_dir, epochs=50):
    """
    Convenience function to create and train a model.
    
    Args:
        train_dir: Path to training data
        epochs: Number of epochs to train
        
    Returns:
        Trained model
    """
    model_manager = FoodRecognitionModel(num_classes=101)
    model_manager.build_model(use_pretrained=True)
    model_manager.compile_model(learning_rate=MODEL_CONFIG['learning_rate'])
    
    model_manager.train(train_dir, epochs=epochs)
    
    return model_manager
