import streamlit as st
from firebase_config import init_firebase
from components.add_user import add_user_page
from components.search import search_page

# Initialize App
init_firebase()

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
