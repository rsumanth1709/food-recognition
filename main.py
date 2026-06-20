#!/usr/bin/env python
"""
Food Recognition & Calorie Tracker - Main Entry Point
Provides interactive menu for all application modes
"""

import sys
import subprocess
from pathlib import Path
import argparse


def print_header():
    """Print application header"""
    print("\n" + "=" * 70)
    print("🍽️  FOOD RECOGNITION & CALORIE TRACKING SYSTEM")
    print("=" * 70)
    print()


def show_menu():
    """Display main menu"""
    print("SELECT MODE:")
    print("  1. 🎓 Jupyter Notebook (Training & Exploration)")
    print("  2. 🎨 Streamlit Web UI (Interactive Interface)")
    print("  3. 🔌 Flask REST API (Backend Service)")
    print("  4. 🚂 Train Model (Command Line)")
    print("  5. 🔍 Inference (Make Predictions)")
    print("  6. ⚙️  Initialize Project (Setup)")
    print("  0. ❌ Exit")
    print()


def run_notebook():
    """Launch Jupyter notebook"""
    print("\n📔 Launching Jupyter Notebook...")
    print("   Notebook: notebooks/01_food_recognition_training.ipynb\n")
    
    try:
        subprocess.run([
            'jupyter', 'notebook',
            'notebooks/01_food_recognition_training.ipynb'
        ])
    except FileNotFoundError:
        print("❌ Jupyter not found. Install with: pip install jupyter")


def run_streamlit():
    """Launch Streamlit UI"""
    print("\n🎨 Launching Streamlit Web Interface...")
    print("   URL: http://localhost:8501\n")
    
    try:
        subprocess.run(['streamlit', 'run', 'ui/app.py'])
    except FileNotFoundError:
        print("❌ Streamlit not found. Install with: pip install streamlit")


def run_flask_api():
    """Launch Flask API"""
    print("\n🔌 Launching Flask REST API...")
    print("   URL: http://localhost:5000\n")
    
    try:
        subprocess.run([sys.executable, 'src/api.py'])
    except FileNotFoundError:
        print("❌ API file not found")


def run_training():
    """Run model training"""
    print("\n🚂 Starting Model Training...")
    print("   This may take 2-4 hours depending on hardware\n")
    
    try:
        subprocess.run([sys.executable, 'train.py'])
    except FileNotFoundError:
        print("❌ Training script not found")


def run_inference():
    """Interactive inference mode"""
    print("\n🔍 Inference Mode - Make Predictions\n")
    
    from src.inference import FoodRecognitionInference
    from pathlib import Path
    
    try:
        inference = FoodRecognitionInference()
        
        while True:
            image_path = input("Enter image path (or 'quit' to exit): ").strip()
            
            if image_path.lower() == 'quit':
                break
            
            if not Path(image_path).exists():
                print("❌ File not found")
                continue
            
            print("\n⏳ Processing image...")
            results = inference.predict_single(image_path, top_k=5)
            
            if results and results['predictions']:
                print("\n📊 Predictions:")
                for i, pred in enumerate(results['predictions'], 1):
                    confidence = pred['confidence'] * 100
                    print(f"\n  {i}. {pred['food_name'].title()}")
                    print(f"     Confidence: {confidence:.2f}%")
                    print(f"     Calories: {pred['calories']} cal/100g")
                    print(f"     Protein: {pred['protein']}g | Fat: {pred['fat']}g | Carbs: {pred['carbs']}g")
            else:
                print("❌ No predictions could be made")
            
            print()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure the model is trained first by running: python train.py")


def run_initialization():
    """Run project initialization"""
    print("\n⚙️  Initializing Project...\n")
    
    try:
        subprocess.run([sys.executable, 'initialize.py'])
    except FileNotFoundError:
        print("❌ Initialization script not found")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Food Recognition & Calorie Tracking System'
    )
    parser.add_argument(
        '--mode',
        choices=['notebook', 'streamlit', 'api', 'train', 'inference', 'init'],
        help='Run in specific mode without menu'
    )
    
    args = parser.parse_args()
    
    print_header()
    
    if args.mode:
        # Direct mode selection
        modes = {
            'notebook': run_notebook,
            'streamlit': run_streamlit,
            'api': run_flask_api,
            'train': run_training,
            'inference': run_inference,
            'init': run_initialization
        }
        modes[args.mode]()
    else:
        # Interactive menu
        while True:
            show_menu()
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == '1':
                run_notebook()
            elif choice == '2':
                run_streamlit()
            elif choice == '3':
                run_flask_api()
            elif choice == '4':
                run_training()
            elif choice == '5':
                run_inference()
            elif choice == '6':
                run_initialization()
            elif choice == '0':
                print("\n👋 Goodbye!\n")
                break
            else:
                print("\n❌ Invalid choice. Please try again.\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
