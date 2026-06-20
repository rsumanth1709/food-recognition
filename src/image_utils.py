"""
Utility functions for image processing and data loading
"""
import numpy as np
from PIL import Image
import logging
from pathlib import Path
from config import MODEL_CONFIG

# Try to import OpenCV, but don't fail if it's not available
try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None

logger = logging.getLogger(__name__)


def load_and_preprocess_image(image_path, target_size=None):
    """
    Load and preprocess an image for model inference.
    
    Args:
        image_path: Path to the image file
        target_size: Target size for resizing (height, width)
        
    Returns:
        numpy array of preprocessed image
    """
    if target_size is None:
        target_size = MODEL_CONFIG['input_size']
    
    try:
        # Load image using PIL
        img = Image.open(image_path).convert('RGB')
        
        # Resize image
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img, dtype=np.float32)
        
        # Normalize to [0, 1]
        img_array = img_array / 255.0
        
        return img_array
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {str(e)}")
        return None


def load_batch_images(image_paths, target_size=None):
    """
    Load and preprocess a batch of images.
    
    Args:
        image_paths: List of paths to image files
        target_size: Target size for resizing
        
    Returns:
        numpy array of shape (batch_size, height, width, 3)
    """
    images = []
    valid_paths = []
    
    for path in image_paths:
        img = load_and_preprocess_image(path, target_size)
        if img is not None:
            images.append(img)
            valid_paths.append(path)
    
    if len(images) == 0:
        logger.warning("No valid images loaded")
        return None, []
    
    return np.array(images), valid_paths


def augment_image(image, augmentation_config=None):
    """
    Apply data augmentation to an image.
    
    Args:
        image: numpy array of image
        augmentation_config: Dictionary with augmentation parameters
        
    Returns:
        augmented image array
    """
    if augmentation_config is None:
        augmentation_config = {
            'rotation_range': 20,
            'width_shift_range': 0.2,
            'height_shift_range': 0.2,
            'horizontal_flip': True,
            'zoom_range': 0.2,
            'brightness_range': [0.8, 1.2]
        }
    
    try:
        # Random rotation
        if np.random.rand() > 0.5:
            angle = np.random.uniform(-augmentation_config['rotation_range'], 
                                      augmentation_config['rotation_range'])
            h, w = image.shape[:2]
            M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
            image = cv2.warpAffine(image, M, (w, h))
        
        # Random horizontal flip
        if augmentation_config['horizontal_flip'] and np.random.rand() > 0.5:
            image = cv2.flip(image, 1)
        
        # Random brightness
        brightness_factor = np.random.uniform(*augmentation_config['brightness_range'])
        image = np.clip(image * brightness_factor, 0, 1).astype(np.float32)
        
        return image
    except Exception as e:
        logger.error(f"Error augmenting image: {str(e)}")
        return image


def normalize_image(image, mean=None, std=None):
    """
    Normalize image using ImageNet statistics.
    
    Args:
        image: numpy array of image
        mean: Mean values for each channel
        std: Standard deviation values for each channel
        
    Returns:
        normalized image array
    """
    if mean is None:
        mean = [0.485, 0.456, 0.406]
    if std is None:
        std = [0.229, 0.224, 0.225]
    
    image = image.copy()
    for i in range(3):
        image[:, :, i] = (image[:, :, i] - mean[i]) / std[i]
    
    return image


def get_image_files(directory, extensions=None):
    """
    Get all image files from a directory.
    
    Args:
        directory: Path to directory
        extensions: List of file extensions to look for
        
    Returns:
        List of image file paths
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    directory = Path(directory)
    image_files = []
    
    for ext in extensions:
        image_files.extend(directory.glob(f'*{ext}'))
        image_files.extend(directory.glob(f'*{ext.upper()}'))
    
    return sorted(image_files)


def create_image_grid(images, labels=None, grid_size=(3, 3)):
    """
    Create a grid visualization of images.
    
    Args:
        images: List of image arrays
        labels: List of labels for images
        grid_size: Tuple of (rows, cols)
        
    Returns:
        combined image array
    """
    rows, cols = grid_size
    fig_height = rows * 3
    fig_width = cols * 3
    
    h, w = images[0].shape[:2]
    grid = np.zeros((fig_height, fig_width, 3), dtype=np.uint8)
    
    idx = 0
    for i in range(rows):
        for j in range(cols):
            if idx < len(images):
                y_start = i * h
                x_start = j * w
                grid[y_start:y_start+h, x_start:x_start+w] = (images[idx] * 255).astype(np.uint8)
                idx += 1
    
    return grid
