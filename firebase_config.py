import firebase_admin
from firebase_admin import credentials, db
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

environment = os.getenv('DEV_ENV')
print(f"dev env: {environment}")

# Initialize Firebase App
def init_firebase():
    if not firebase_admin._apps:
        # Initialize Firebase
        if environment == 'False':
            # Use Streamlit secrets for production
            firebase_credentials = st.secrets["firebase"]
            # Initialize Firebase with the secrets from .streamlit/secrets.toml
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": firebase_credentials["project_id"],
                "private_key_id": firebase_credentials["private_key_id"],
                "private_key": firebase_credentials["private_key"],
                "client_email": firebase_credentials["client_email"],
                "client_id": firebase_credentials["client_id"],
                "auth_uri": firebase_credentials["auth_uri"],
                "token_uri": firebase_credentials["token_uri"],
                "auth_provider_x509_cert_url": firebase_credentials["auth_provider_x509_cert_url"],
                "client_x509_cert_url": firebase_credentials["client_x509_cert_url"],
                "universe_domain": firebase_credentials["universe_domain"]
            })
        else:
            cred = credentials.Certificate("goyal-fertilizer-app-firebase-adminsdk-sb50l-9dfb605f4f.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://goyal-fertilizer-app-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })

# Add User
def add_user(data):
    try:
        # Check if user already exists based on Aadhar number
        existing_user = get_user_by_aadhar(data['aadhar_number'])
        if existing_user:
            return False, "User with this Aadhar number already exists."
        
        ref = db.reference('users')
        ref.push(data)
        return True, "User added successfully."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"


# Get All Users
def get_users():
    ref = db.reference('users')
    return ref.get()

# Get User by Aadhar
def get_user_by_aadhar(aadhar_number):
    users = get_users()
    if users:
        for key, value in users.items():
            if value['aadhar_number'] == aadhar_number:
                return key, value
    return None

def search_users(filters):
    users = get_users()
    if not users:
        return []

    results = []
    
    # Ensure that the filters are treated as strings
    name_filter = filters.get('name', '').lower()
    phone_filter = str(filters.get('phone_number', '')).strip()
    aadhar_filter = str(filters.get('aadhar_number', '')).strip()
    location_filter = filters.get('location', '').lower()
    
    for user_id, user_data in users.items():
        # Convert user data fields to strings for consistent comparison
        user_name = user_data.get('name', '').lower()
        user_phone = str(user_data.get('phone', '')).strip()
        user_aadhar = str(user_data.get('aadhar_number', '')).strip()
        user_location = user_data.get('area', '').lower()

        # Perform search comparisons only for the available filter
        if name_filter and name_filter in user_name:
            results.append(user_data)
        elif phone_filter and phone_filter == user_phone:
            results.append(user_data)
        elif aadhar_filter and aadhar_filter == user_aadhar:
            results.append(user_data)
        elif location_filter and location_filter in user_location:
            results.append(user_data)

    return results
