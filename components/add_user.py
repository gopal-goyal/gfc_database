import re
import streamlit as st
from firebase_config import add_user

# Function to validate phone number (10 digits)
def validate_phone_number(phone):
    return len(phone) == 10 and phone.isdigit()

# Function to validate Aadhar number (12 digits)
def validate_aadhar_number(aadhar_number):
    return len(aadhar_number) == 12 and aadhar_number.isdigit()

# Function to validate email address format
def validate_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

# Function to validate name (only letters and spaces)
def validate_name(name):
    return bool(re.match(r"^[A-Za-z\s]+$", name))

def add_user_page():
    st.markdown(
        """
        <h3 style='text-align: center'>
        Add New User
        </h3>
        """,
        unsafe_allow_html=True
    )

    with st.form(key="add_user_form"):
        # Mandatory fields
        name = st.text_input("Name", placeholder="Enter full name")
        phone = st.text_input("Phone Number", placeholder="Enter 10-digit phone number")
        area = st.text_input("Area/Location", placeholder="Enter the user's area or location")
        aadhar_number = st.text_input("Aadhar Number (Unique ID)", placeholder="Enter 12-digit Aadhar number")
        
        # Optional fields
        a1, a2 = st.columns([1,1])
        b1, b2, b3 = st.columns([1,1,1])
        c1, c2 = st.columns([1,1])
        with a1:
            land = st.text_input("Land in Acquisition (Bigha/Acre)", placeholder="Enter the size of the land")
        with a2:
            email = st.text_input("Email", placeholder="Enter the user's email address")
        with b1:
            demand = st.text_input("Demand", placeholder="Enter the user's demand for products or services")
        with b2:
            payment_mode = st.selectbox(
                "Preferred Payment Mode", 
                ["Cash", "Online", "Other"], 
                help="Select the user's preferred payment method"
            )
        with b3:
            major_crops = st.multiselect(
                "Major Crops", 
                options=["Wheat", "Rice", "Mustard", "Barley", "Maize", "Sugarcane", "Other"],
                help="Select the crops grown by the user. You can select multiple."
            )
        with c1:
            challenges = st.text_input(
                "Common Challenges", 
                placeholder="Describe any challenges the user faces"
            )
        with c2:
            water_source = st.text_input(
                "Water Source and Availability", 
                placeholder="Describe the water sources available to the user"
            )

        # Submit button
        submit = st.form_submit_button("Submit")

        if submit:
            # Validate mandatory fields
            if not name or not phone or not area or not aadhar_number:
                st.error("Please fill in all mandatory fields: Name, Phone Number, Area, and Aadhar Number.")
            elif not validate_name(name):
                st.error("Name must only contain alphabetic characters and spaces.")
            elif not validate_phone_number(phone):
                st.error("Phone number must be a 10-digit number.")
            elif not validate_aadhar_number(aadhar_number):
                st.error("Aadhar number must be a 12-digit number.")
            elif email and not validate_email(email):
                st.error("Please enter a valid email address.")
            else:
                # Prepare user data
                user_data = {
                    "name": name,
                    "phone": phone,
                    "area": area,
                    "aadhar_number": aadhar_number,
                    "land": land,
                    "email": email,
                    "major_crops": major_crops,  # Already a list
                    "demand": demand,
                    "payment_mode": payment_mode,
                    "challenges": challenges,
                    "water_source": water_source
                }
                # Add user to Firebase
                success, message = add_user(user_data)
                if success:
                    st.success(message)
                else:
                    st.error(message)
