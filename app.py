import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import os

# File to store the data
DATA_FILE = "weekly_ratings.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return pd.DataFrame(data)
    return pd.DataFrame(columns=['Date', 'School', 'Work', 'Sleep', 'Health', 'Hobbies'])

def save_data(df):
    with open(DATA_FILE, "w") as f:
        json.dump(df.to_dict('records'), f)

# Load data from file
if 'data' not in st.session_state:
    st.session_state.data = load_data()

def is_sunday():
    return datetime.now().weekday() == 6

def get_last_sunday():
    today = datetime.now().date()
    return today - timedelta(days=(today.weekday() + 1) % 7)

st.title("Weekly Rating App")
st.write("Welcome to the Weekly Rating App! This app allows you to track your weekly ratings for School, Work, Sleep, Health, and Hobbies.")

# Instructions for deploying on Streamlit Sharing
st.sidebar.title("App Instructions")
st.sidebar.write("""
Please enter a rating, 1-10, for each category.
Come back every Sunday to track your progress!
""")

if is_sunday():
    st.write("It's Sunday! Time to add your weekly ratings.")
    
    ratings = {}
    for category in ['School', 'Work', 'Sleep', 'Health', 'Hobbies']:
        ratings[category] = st.slider(f"Rate your {category} (1-10)", 1, 10, 5)
    
    if st.button("Submit Ratings"):
        new_entry = pd.DataFrame({
            'Date': [get_last_sunday().strftime('%Y-%m-%d')],  # Convert date to string for JSON serialization
            **ratings
        })
        st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
        save_data(st.session_state.data)  # Save data to file
        st.success("Ratings submitted successfully!")
else:
    st.write("You can only submit ratings on Sundays. Check back on the next Sunday!")

# Display the data
st.subheader("Your Weekly Ratings")
st.dataframe(st.session_state.data)

# Visualization
if not st.session_state.data.empty:
    st.subheader("Rating Trends")
    chart_data = st.session_state.data.melt('Date', var_name='Category', value_name='Rating')
    chart_data['Date'] = pd.to_datetime(chart_data['Date'])  # Convert Date back to datetime for charting
    st.line_chart(chart_data.pivot(index='Date', columns='Category', values='Rating'))

# Add an option to clear all data
if st.button("Clear All Data"):
    st.session_state.data = pd.DataFrame(columns=['Date', 'School', 'Work', 'Sleep', 'Health', 'Hobbies'])
    save_data(st.session_state.data)
    st.success("All data has been cleared!")