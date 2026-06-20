#!/usr/bin/env python
"""
Initialization script for the Food Recognition project
Sets up necessary directories and downloads/prepares data
"""

import os
import sys
from pathlib import Path
import subprocess
import json
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def setup_directories():
    """Create necessary project directories"""
    logger.info("Setting up project directories...")
    
    directories = [
        'data/food-101',
        'models/checkpoints',
        'output/logs',
        'output/results',
        'output/models',
        'uploads',
        'notebooks/checkpoints'
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Created {directory}")


def check_dependencies():
    """Check if all required packages are installed"""
    logger.info("Checking dependencies...")
    
    required_packages = {
        'tensorflow': 'TensorFlow',
        'keras': 'Keras',
        'numpy': 'NumPy',
        'pandas': 'Pandas',
        'PIL': 'Pillow',
        'cv2': 'OpenCV',
        'flask': 'Flask',
        'streamlit': 'Streamlit',
        'sklearn': 'scikit-learn'
    }
    
    missing_packages = []
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            logger.info(f"✓ {name} is installed")
        except ImportError:
            logger.warning(f"✗ {name} is NOT installed")
            missing_packages.append(name)
    
    if missing_packages:
        logger.warning(f"\nMissing packages: {', '.join(missing_packages)}")
        logger.info("Install them using: pip install -r requirements.txt")
        return False
    
    logger.info("✓ All dependencies are installed!")
    return True


def verify_dataset():
    """Check if Food-101 dataset is available"""
    logger.info("Checking for Food-101 dataset...")
    
    data_dir = Path('data/food-101')
    images_dir = data_dir / 'images'
    meta_dir = data_dir / 'meta'
    
    if images_dir.exists() and meta_dir.exists():
        logger.info("✓ Food-101 dataset found!")
        
        # Count images
        image_count = sum(1 for _ in images_dir.glob('*/*.jpg'))
        logger.info(f"  Found {image_count} images")
        
        return True
    else:
        logger.warning("✗ Food-101 dataset NOT found!")
        logger.info("\nTo download the dataset:")
        logger.info("1. Visit: https://www.kaggle.com/dansbecker/food-101")
        logger.info("2. Download the dataset")
        logger.info("3. Extract to: data/food-101/")
        logger.info("\nOr use Kaggle API:")
        logger.info("  kaggle datasets download -d dansbecker/food-101")
        logger.info("  unzip -q food-101.zip -d data/")
        
        return False


def create_sample_config():
    """Create sample configuration files"""
    logger.info("Creating configuration files...")
    
    # Sample API config
    api_config = {
        'host': '0.0.0.0',
        'port': 5000,
        'debug': True,
        'max_content_length': 16 * 1024 * 1024  # 16MB
    }
    
    with open('output/api_config.json', 'w') as f:
        json.dump(api_config, f, indent=2)
    
    logger.info("✓ Configuration files created")


def main():
    """Main setup function"""
    logger.info("=" * 60)
    logger.info("Food Recognition Project - Initialization")
    logger.info("=" * 60)
    
    # Setup directories
    setup_directories()
    
    logger.info("\n" + "=" * 60)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    logger.info("\n" + "=" * 60)
    
    # Verify dataset
    dataset_ok = verify_dataset()
    
    logger.info("\n" + "=" * 60)
    
    # Create config
    create_sample_config()
    
    logger.info("\n" + "=" * 60)
    logger.info("SETUP SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Dependencies OK: {deps_ok}")
    logger.info(f"Dataset Found: {dataset_ok}")
    
    if not dataset_ok:
        logger.info("\n⚠️  Dataset not found. Download before training.")
    
    if deps_ok and dataset_ok:
        logger.info("\n✓ All systems ready! You can now:")
        logger.info("  - Run: python train.py (to train the model)")
        logger.info("  - Run: streamlit run ui/app.py (to launch the UI)")
        logger.info("  - Run: python src/api.py (to start the API)")
    else:
        logger.warning("\n⚠️  Please complete the above steps before running the application.")
    
    logger.info("\n" + "=" * 60)


if __name__ == '__main__':
    main()
