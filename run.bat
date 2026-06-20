@echo off
REM Food Recognition & Calorie Tracker - Windows Launch Script
REM This script helps Windows users run the application easily

setlocal enabledelayedexpansion

echo.
echo ========================================================================
echo  FOOD RECOGNITION ^& CALORIE TRACKING SYSTEM
echo ========================================================================
echo.

if "%1"=="" (
    REM No arguments - show menu
    echo SELECT MODE:
    echo   1 - Streamlit Web UI (Recommended)
    echo   2 - Flask REST API
    echo   3 - Jupyter Notebook
    echo   4 - Train Model
    echo   5 - Initialize Project
    echo   6 - Direct Inference
    echo   0 - Exit
    echo.
    
    set /p CHOICE="Enter your choice (0-6): "
    
    if "!CHOICE!"=="1" goto streamlit
    if "!CHOICE!"=="2" goto api
    if "!CHOICE!"=="3" goto notebook
    if "!CHOICE!"=="4" goto train
    if "!CHOICE!"=="5" goto init
    if "!CHOICE!"=="6" goto inference
    if "!CHOICE!"=="0" goto end
    
    echo Invalid choice!
    goto end
)

if "%1"=="streamlit" goto streamlit
if "%1"=="api" goto api
if "%1"=="notebook" goto notebook
if "%1"=="train" goto train
if "%1"=="init" goto init
if "%1"=="inference" goto inference

:streamlit
echo.
echo Launching Streamlit Web Interface...
echo URL: http://localhost:8501
echo.
python -m streamlit run ui/app.py
goto end

:api
echo.
echo Launching Flask REST API...
echo URL: http://localhost:5000
echo.
python src/api.py
goto end

:notebook
echo.
echo Launching Jupyter Notebook...
echo.
python -m jupyter notebook notebooks/01_food_recognition_training.ipynb
goto end

:train
echo.
echo Starting Model Training...
echo This will take 2-4 hours on GPU
echo.
python train.py
goto end

:init
echo.
echo Initializing Project...
echo.
python initialize.py
goto end

:inference
echo.
echo Running Inference Mode...
echo.
python main.py --mode inference
goto end

:end
echo.
pause
