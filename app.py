import streamlit as st
from firebase_config import init_firebase
from components.add_user import add_user_page
from components.search import search_page
from config import DEV_ENV
from dotenv import load_dotenv
import os

# Load Environment
load_dotenv()

# Initialize App
init_firebase()

if DEV_ENV:
    PASSWORD = os.getenv('PASSWORD')
else:
    auth_credentials = st.secrets["auth"]
    PASSWORD = auth_credentials["password"]

def main():
    # App Configuration
    st.set_page_config(page_title="GFC Database 👨🏾‍🌾", layout="centered")
    
    # Fancy Title
    st.markdown(
        """
        <h1 style='text-align: center; font-size: 3rem; color: #4CAF50; font-family: "Trebuchet MS", sans-serif;'>
            🌾 GFC Database 👨🏾‍🌾
        </h1>
        """, 
        unsafe_allow_html=True
    )

    # Password prompt
    password = st.text_input("Enter Password", type="password")

    # Check if password is correct
    if password == PASSWORD:
        # Sidebar Navigation
        menu = st.sidebar.selectbox("Menu", ["Search Users", "Add New User"])

        # Route to pages
        if menu == "Search Users":
            search_page()
        elif menu == "Add New User":
            add_user_page()

# Entry Point
if __name__ == "__main__":
    main()
