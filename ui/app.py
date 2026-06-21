"""
Streamlit Web Interface for Food Recognition and Calorie Tracking
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root: Path = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import logging
import hashlib
import json
import importlib

# Import local modules
from src.inference import FoodRecognitionInference
from src.calorie_database import CalorieDatabase
from src.database import FoodTrackerDB
from config import STREAMLIT_CONFIG

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title=STREAMLIT_CONFIG['page_title'],
    page_icon="🍽️",
    layout=STREAMLIT_CONFIG['layout'],
    initial_sidebar_state="expanded"
)

# Initialize database (without caching to pick up new methods)
def get_database():
    """Get database instance"""
    return FoodTrackerDB()

db = get_database()

def is_valid_gmail(email):
    """Check if email is a valid Gmail address"""
    import re
    gmail_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(gmail_pattern, email) is not None

def show_login_page():
    """Display login/registration page"""
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>🍽️ Food Recognition & Calorie Tracker</h1>
        <p style="font-size: 18px; color: #666;">Track your nutrition with AI-powered food recognition</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            email = st.text_input("Gmail Address", placeholder="your.email@gmail.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if email and password:
                    if not is_valid_gmail(email):
                        st.error("❌ Please use a valid Gmail address (@gmail.com)")
                    else:
                        # Try to find user by email
                        success, user_data = db.authenticate_user(email, password)
                        if success:
                            st.session_state.authenticated = True
                            st.session_state.user_id = user_data['id']
                            st.session_state.username = user_data['username']
                            st.session_state.user_data = user_data
                            st.success(f"✅ Welcome back, {user_data['name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
                else:
                    st.warning("⚠️ Please enter both email and password")
    
    with tab2:
        st.subheader("Create New Account")
        st.info("📧 Please use your real Gmail address for registration")
        
        with st.form("register_form"):
            new_name = st.text_input("Full Name", placeholder="John Doe")
            new_email = st.text_input("Gmail Address", placeholder="your.email@gmail.com")
            new_password = st.text_input("Password", type="password", help="Minimum 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            agree = st.checkbox("I agree to use my real Gmail address")
            
            register = st.form_submit_button("Register", use_container_width=True)
            
            if register:
                if not all([new_name, new_email, new_password, confirm_password]):
                    st.warning("⚠️ Please fill in all fields")
                elif not is_valid_gmail(new_email):
                    st.error("❌ Please use a valid Gmail address (@gmail.com)")
                elif not agree:
                    st.warning("⚠️ Please agree to use your real Gmail address")
                elif new_password != confirm_password:
                    st.error("❌ Passwords do not match")
                elif len(new_password) < 6:
                    st.error("❌ Password must be at least 6 characters long")
                else:
                    # Use email as username
                    success, message = db.create_user(new_email, new_password, new_name, new_email)
                    if success:
                        st.success("✅ " + message + " Please login with your Gmail address.")
                        st.balloons()
                    else:
                        st.error("❌ " + message)

# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Show login page if not authenticated
if not st.session_state.authenticated:
    show_login_page()
    st.stop()

# Initialize session state
if 'inference_engine' not in st.session_state:
    st.session_state.inference_engine = FoodRecognitionInference()

if 'calorie_db' not in st.session_state:
    st.session_state.calorie_db = CalorieDatabase()

if 'db' not in st.session_state:
    st.session_state.db = db

# Load CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("🍽️ Food Tracker")
    
    # Display user info
    if 'user_data' in st.session_state and st.session_state.user_data:
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;">
            <p style="margin: 0; font-size: 14px; color: #666;">Logged in as:</p>
            <p style="margin: 0; font-size: 16px; font-weight: bold;">👤 {st.session_state.user_data['name']}</p>
            <p style="margin: 0; font-size: 12px; color: #888;">📧 {st.session_state.user_data['email']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    selected = option_menu(
        "Main Menu",
        ["Home", "Food Recognition", "Add Meal", "Daily Summary", "Meal History", "Food Search", "Analytics"],
        icons=["house", "camera", "plus", "bar-chart", "clock-history", "search", "graph"],
        menu_icon="cast",
        default_index=0
    )
    
    st.divider()
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True, type="primary"):
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.user_data = None
        st.success("✅ Logged out successfully!")
        st.rerun()
    
    st.divider()
    st.info("""
    ### Quick Tips
    - Upload a photo of your food to identify it
    - Add meals manually or import from recognized images
    - Track your daily calorie intake
    - Get nutritional breakdown for each meal
    """)


# Home Page
if selected == "Home":
    st.title("🍽️ Food Recognition & Calorie Tracker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Display a nice food-themed visual using emojis and markdown
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
            <h1 style="font-size: 80px; margin: 0;">🍕🥗🍎</h1>
            <h2 style="margin: 10px 0;">Food Recognition</h2>
            <p style="font-size: 18px;">AI-Powered Nutrition Tracking</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.write("""
        ### Welcome to Your Personal Nutrition Assistant!
        
        This application uses **AI-powered image recognition** to identify food items and
        estimate their calorie content, helping you track your dietary intake and make
        informed food choices.
        
        #### Key Features:
        - **Food Recognition**: Upload photos of your meals to identify food items
        - **Calorie Tracking**: Automatic calorie estimation with nutritional breakdown
        - **Daily Summary**: Monitor your daily intake vs. recommended limits
        - **Food Database**: Search for nutritional information on 100+ food items
        - **Analytics**: Visualize your eating patterns and trends
        - **Meal History**: Keep records of all meals logged
        """)
    
    st.divider()
    
    # Display current stats
    st.subheader("📊 Today's Quick Stats")
    
    summary = db.get_daily_summary(st.session_state.user_id)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Calories", f"{summary['total_calories']:.0f}")
    
    with col2:
        st.metric("Protein", f"{summary['nutrition']['protein']:.1f}g")
    
    with col3:
        st.metric("Fat", f"{summary['nutrition']['fat']:.1f}g")
    
    with col4:
        st.metric("Carbs", f"{summary['nutrition']['carbs']:.1f}g")


# Food Recognition Page
elif selected == "Food Recognition":
    st.title("📸 Food Recognition")
    
    st.write("Upload an image of your food to identify it and get calorie information.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['jpg', 'jpeg', 'png', 'gif', 'bmp']
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        quantity_percentage = st.slider(
            "Serving Size Adjustment",
            min_value=0.25,
            max_value=2.0,
            value=1.0,
            step=0.25,
            help="Adjust if your portion is larger or smaller than 100g"
        )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Uploaded Image")
            st.image(image, use_column_width=True)
        
        with col2:
            st.subheader("Analysis")
            
            # Save temp file using tempfile module safely
            import tempfile
            import os
            
            fd, temp_file_path = tempfile.mkstemp(suffix=".jpg")
            try:
                os.close(fd)
                image.save(temp_file_path)
                
                with st.spinner("🤖 Analyzing image..."):
                    results = st.session_state.inference_engine.predict_single(Path(temp_file_path), top_k=5)
                
                if results and results['predictions']:
                    # Display predictions
                    st.write("**Top Predictions:**")
                    
                    for i, pred in enumerate(results['predictions'], 1):
                        with st.expander(
                            f"{i}. {pred['food_name'].title()} ({pred['confidence']*100:.1f}%)",
                            expanded=(i == 1)
                        ):
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                st.metric("Calories", f"{pred['calories']} (per 100g)")
                                st.metric("Protein", f"{pred['protein']}g")
                            
                            with col_b:
                                st.metric("Fat", f"{pred['fat']}g")
                                st.metric("Carbs", f"{pred['carbs']}g")
                            
                            st.metric("Fiber", f"{pred['fiber']}g")
                            
                            # Add to tracker button
                            if st.button(
                                f"Add '{pred['food_name']}' to Today",
                                key=f"add_{i}"
                            ):
                                db.add_meal(
                                    st.session_state.user_id,
                                    pred['food_name'],
                                    pred['calories'] * quantity_percentage,
                                    {
                                        'protein': pred['protein'] * quantity_percentage,
                                        'fat': pred['fat'] * quantity_percentage,
                                        'carbs': pred['carbs'] * quantity_percentage,
                                        'fiber': pred['fiber'] * quantity_percentage,
                                    }
                                )
                                st.success(f"✅ Added {pred['food_name']} to today's meals!")
            finally:
                # Clean up temp file safely
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)


# Add Meal Page
elif selected == "Add Meal":
    st.title("➕ Add Meal Manually")
    
    col1, col2 = st.columns(2)
    
    with col1:
        meal_type = st.selectbox(
            "Meal Type",
            ["Breakfast", "Lunch", "Dinner", "Snack", "Other"]
        )
    
    with col2:
        food_name = st.text_input("Food Name")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        calories = st.number_input("Calories", min_value=0, value=250)
    
    with col2:
        protein = st.number_input("Protein (g)", min_value=0.0, value=0.0, step=0.1)
    
    with col3:
        fat = st.number_input("Fat (g)", min_value=0.0, value=0.0, step=0.1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        carbs = st.number_input("Carbs (g)", min_value=0.0, value=0.0, step=0.1)
    
    with col2:
        fiber = st.number_input("Fiber (g)", min_value=0.0, value=0.0, step=0.1)
    
    if st.button("✅ Add Meal", use_container_width=True):
        if food_name.strip():
            db.add_meal(
                st.session_state.user_id,
                food_name,
                calories,
                {
                    'protein': protein,
                    'fat': fat,
                    'carbs': carbs,
                    'fiber': fiber
                },
                meal_type.lower()
            )
            st.success(f"✅ Added {food_name} to today's meals!")
            st.balloons()
        else:
            st.error("❌ Please enter a food name")


# Daily Summary Page
elif selected == "Daily Summary":
    st.title("📊 Daily Summary")
    
    summary = db.get_daily_summary(st.session_state.user_id)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Calories",
            f"{summary['total_calories']:.0f}",
            delta="2000 goal"
        )
    
    with col2:
        st.metric("Total Meals", summary['total_meals'])
    
    with col3:
        st.metric("Total Protein", f"{summary['nutrition']['protein']:.1f}g")
    
    with col4:
        st.metric("Total Carbs", f"{summary['nutrition']['carbs']:.1f}g")
    
    st.divider()
    
    # Macronutrient breakdown
    st.subheader("🥗 Macronutrient Breakdown")
    
    nutrition_data = summary['nutrition'].copy()
    nutrition_data.pop('fiber', None)
    
    fig = go.Figure(data=[
        go.Pie(
            labels=list(nutrition_data.keys()),
            values=list(nutrition_data.values()),
            hole=0.3
        )
    ])
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Meal breakdown
    st.subheader("🍽️ Meals by Type")
    
    breakdown = db.get_meal_breakdown(st.session_state.user_id)
    
    if breakdown:
        breakdown_df = pd.DataFrame(breakdown).T
        
        fig = px.bar(
            breakdown_df,
            y='calories',
            title="Calories by Meal Type",
            labels={'calories': 'Calories', 'index': 'Meal Type'},
            color='calories',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No meals added yet. Add meals to see breakdown.")
    
    st.divider()
    
    # Detailed meal list
    st.subheader("📝 Meal Details")
    
    meals = db.get_daily_meals(st.session_state.user_id)
    
    if meals:
        meals_df = pd.DataFrame(meals)
        meals_df = meals_df[['food_name', 'meal_type', 'calories']].rename(columns={
            'food_name': 'Food Name',
            'meal_type': 'Type',
            'calories': 'Calories'
        })
        st.dataframe(meals_df, use_container_width=True)
        
        # Reset button
        if st.button("🔄 Reset Daily Tracker"):
            db.reset_daily_meals(st.session_state.user_id)
            st.success("Daily tracker has been reset!")
            st.rerun()
    else:
        st.info("No meals logged today")


# Meal History Page
elif selected == "Meal History":
    st.title("🕐 Meal History")
    
    st.write("View your complete meal history and track your progress over time.")
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        days_back = st.selectbox(
            "Time Period",
            options=[7, 14, 30, 60, 90],
            format_func=lambda x: f"Last {x} days",
            index=0
        )
    
    with col2:
        filter_meal_type = st.selectbox(
            "Filter by Meal Type",
            options=["All", "breakfast", "lunch", "dinner", "snack", "other"]
        )
    
    # Get meal history
    meals = db.get_meal_history(st.session_state.user_id, days=days_back)
    
    if filter_meal_type != "All":
        meals = [m for m in meals if m['meal_type'] == filter_meal_type]
    
    if meals:
        st.subheader(f"📋 Found {len(meals)} meals")
        
        # Summary statistics
        total_calories = sum(m['calories'] for m in meals)
        avg_calories = total_calories / len(meals) if meals else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Meals", len(meals))
        
        with col2:
            st.metric("Total Calories", f"{total_calories:.0f}")
        
        with col3:
            st.metric("Avg Calories/Meal", f"{avg_calories:.0f}")
        
        with col4:
            total_protein = sum(m['protein'] for m in meals)
            st.metric("Total Protein", f"{total_protein:.1f}g")
        
        st.divider()
        
        # Group meals by date
        from datetime import datetime
        from collections import defaultdict
        
        meals_by_date = defaultdict(list)
        for meal in meals:
            meals_by_date[meal['meal_date']].append(meal)
        
        # Display meals grouped by date
        for date in sorted(meals_by_date.keys(), reverse=True):
            date_meals = meals_by_date[date]
            date_calories = sum(m['calories'] for m in date_meals)
            
            with st.expander(f"📅 {date} - {len(date_meals)} meals ({date_calories:.0f} cal)", expanded=False):
                for meal in date_meals:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        meal_time = meal['meal_time'].split()[1] if ' ' in meal['meal_time'] else meal['meal_time']
                        st.write(f"**{meal['food_name']}** ({meal['meal_type']}) - {meal_time}")
                    
                    with col2:
                        st.write(f"{meal['calories']:.0f} cal")
                    
                    with col3:
                        st.write(f"P: {meal['protein']:.1f}g")
                    
                    # Nutrition details in smaller text
                    st.caption(f"Fat: {meal['fat']:.1f}g | Carbs: {meal['carbs']:.1f}g | Fiber: {meal['fiber']:.1f}g")
                    st.divider()
        
        # Date range summary chart
        st.subheader("📊 Daily Calorie Trend")
        
        from datetime import date, timedelta
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)
        
        daily_summary = db.get_date_range_summary(st.session_state.user_id, start_date, end_date)
        
        if daily_summary:
            import plotly.graph_objects as go
            
            dates = [s['date'] for s in daily_summary]
            calories = [s['total_calories'] for s in daily_summary]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=calories,
                mode='lines+markers',
                name='Daily Calories',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))
            
            fig.add_hline(y=2000, line_dash="dash", line_color="red",
                         annotation_text="Daily Goal (2000 cal)")
            
            fig.update_layout(
                title="Daily Calorie Intake",
                xaxis_title="Date",
                yaxis_title="Calories",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No meals found in the last {days_back} days.")
        st.write("Start tracking your meals to see your history here!")


# Food Search Page
elif selected == "Food Search":
    st.title("🔍 Food Database Search")
    
    search_query = st.text_input(
        "Search for foods",
        placeholder="e.g., chicken, salad, pizza..."
    )
    
    if search_query:
        matches = st.session_state.calorie_db.search_food(search_query)
        
        if matches:
            st.write(f"Found {len(matches)} matching foods:")
            
            for food in matches[:10]:
                with st.expander(f"🍖 {food.replace('_', ' ').title()}"):
                    info = st.session_state.calorie_db.get_nutrition_info(food)
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Calories", f"{info['calories']}")
                    
                    with col2:
                        st.metric("Protein", f"{info['protein']}g")
                    
                    with col3:
                        st.metric("Fat", f"{info['fat']}g")
                    
                    with col4:
                        st.metric("Carbs", f"{info['carbs']}g")
                    
                    if st.button(f"Add to Today", key=f"quick_add_{food}"):
                        db.add_meal(
                            st.session_state.user_id,
                            food.replace('_', ' '),
                            info['calories'],
                            {
                                'protein': info['protein'],
                                'fat': info['fat'],
                                'carbs': info['carbs'],
                                'fiber': info['fiber']
                            }
                        )
                        st.success(f"Added {food.replace('_', ' ')} to today!")
        else:
            st.warning(f"No foods found matching '{search_query}'")
    
    st.divider()
    
    # Browse all foods
    if st.checkbox("Browse all available foods"):
        all_foods = st.session_state.calorie_db.get_all_foods()
        st.write(f"Total foods in database: {len(all_foods)}")
        
        # Create columns for displaying foods
        cols = st.columns(3)
        for idx, food in enumerate(all_foods):
            with cols[idx % 3]:
                with st.expander(food.replace('_', ' ').title()):
                    info = st.session_state.calorie_db.get_nutrition_info(food)
                    st.write(f"**Calories**: {info['calories']}")
                    st.write(f"**Protein**: {info['protein']}g")
                    st.write(f"**Carbs**: {info['carbs']}g")


# Analytics Page
elif selected == "Analytics":
    st.title("📈 Analytics & Insights")
    
    st.write("View your nutrition trends and eating patterns.")
    
    summary = db.get_daily_summary(st.session_state.user_id)
    
    # Daily goals comparison
    st.subheader("📋 Daily Goals Comparison")
    
    goals = {
        'Calories': 2000,
        'Protein': 50,
        'Fat': 65,
        'Carbs': 300
    }
    
    comparison_data = {
        'Nutrient': ['Calories', 'Protein (g)', 'Fat (g)', 'Carbs (g)'],
        'Consumed': [
            summary['total_calories'],
            summary['nutrition']['protein'],
            summary['nutrition']['fat'],
            summary['nutrition']['carbs']
        ],
        'Goal': [2000, 50, 65, 300]
    }
    
    comparison_df = pd.DataFrame(comparison_data)
    
    fig = go.Figure(data=[
        go.Bar(name='Consumed', x=comparison_df['Nutrient'], y=comparison_df['Consumed']),
        go.Bar(name='Goal', x=comparison_df['Nutrient'], y=comparison_df['Goal'])
    ])
    fig.update_layout(barmode='group', height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Meal type analysis
    st.subheader("🍽️ Meal Type Distribution")
    
    breakdown = db.get_meal_breakdown(st.session_state.user_id)
    
    if breakdown:
        breakdown_data = {
            'Meal Type': list(breakdown.keys()),
            'Count': [v['count'] for v in breakdown.values()],
            'Calories': [v['calories'] for v in breakdown.values()]
        }
        
        breakdown_df = pd.DataFrame(breakdown_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                breakdown_df,
                values='Count',
                names='Meal Type',
                title='Meal Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                breakdown_df,
                x='Meal Type',
                y='Calories',
                title='Calories by Meal Type',
                color='Calories',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add meals to see analytics")


# Footer
st.divider()
st.markdown("""
**Food Recognition & Calorie Tracker** | Powered by AI | v1.0
""")
