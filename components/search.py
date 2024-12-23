import streamlit as st
from firebase_config import search_users, get_users
import pandas as pd

def search_page():
    # Search Options
    search_option = st.selectbox(
        "Search By",
        ["Name", "Phone Number", "Aadhar Number", "Location"]
    )

    # Input Field Based on Selected Search Option
    if search_option == "Name":
        search_value = st.text_input("Enter Name")
    elif search_option == "Phone Number":
        search_value = st.text_input("Enter Phone Number")
    elif search_option == "Aadhar Number":
        search_value = st.text_input("Enter Aadhar Number")
    elif search_option == "Location":
        search_value = st.text_input("Enter Location")

    # Search Button
    if st.button("Search"):
        # Prepare Filters Based on Selection
        filters = {search_option.lower().replace(" ", "_"): search_value}

        # Perform Search
        results = search_users(filters=filters)
        if results:
            st.success(f"Found {len(results)} result(s)")
            # Convert the results into a DataFrame for tabular display
            user_data_list = []
            for user in results:
                user_data_list.append({
                    "Name": user.get('name'),
                    "Phone": user.get('phone'),
                    "Aadhar Number": user.get('aadhar_number'),
                    "Area": user.get('area'),
                    "Email": user.get('email'),
                    "Land": user.get('land'),
                    "Major Crops": ", ".join(user.get('major_crops', [])),
                    "Demand": user.get('demand'),
                    "Payment Mode": user.get('payment_mode'),
                    "Challenges": user.get('challenges'),
                    "Water Source": user.get('water_source')
                })
            
            # Create a DataFrame from the list of user data
            df = pd.DataFrame(user_data_list)

            # Display the DataFrame as a table
            st.dataframe(df, use_container_width=True)
        else:
            st.error("No matching users found.")
    
    # Show All Data Button
    if st.button("Show All Data"):
        # Get all users from the database
        users = get_users()

        if users:
            st.success(f"Found {len(users)} user(s)")

            # Convert the results into a DataFrame for tabular display
            all_user_data_list = []
            for user in users.values():
                all_user_data_list.append({
                    "Name": user.get('name'),
                    "Phone": user.get('phone'),
                    "Aadhar Number": user.get('aadhar_number'),
                    "Area": user.get('area'),
                    "Email": user.get('email'),
                    "Land": user.get('land'),
                    "Major Crops": ", ".join(user.get('major_crops', [])),
                    "Demand": user.get('demand'),
                    "Payment Mode": user.get('payment_mode'),
                    "Challenges": user.get('challenges'),
                    "Water Source": user.get('water_source')
                })
            
            # Create a DataFrame from the list of all user data
            df_all_users = pd.DataFrame(all_user_data_list)

            # Display the DataFrame as a table
            st.dataframe(df_all_users, use_container_width=True)
        else:
            st.error("No users found.")