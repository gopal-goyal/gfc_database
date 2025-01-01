import streamlit as st
from sheets_connection import update_cells
import pandas as pd
import os

# Define the file path for storing the data
DATA_FILE = "user_data.csv"

# Function to append data to the CSV file
def save_to_csv(data):
    # If the file doesn't exist, create it and add the header
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame([data])  # Convert to DataFrame
        df.to_csv(DATA_FILE, mode='w', header=True, index=False)
    else:
        # Append data to the CSV file
        df = pd.DataFrame([data])  # Convert to DataFrame
        df.to_csv(DATA_FILE, mode='a', header=False, index=False)

def builty():
    st.title("Google Sheets Update Interface")
    
    with st.expander("Update Buility Sheet Data", expanded=False):
        st.header("Edit Details for Sheet 2 (B1-B9 and C8)")

        # Create columns for a structured layout
        col1, col2 = st.columns(2)

        with col1:
            # Inputs for cells B1-B5
            b1_b5_data = [
                st.text_input("GR NO (B1):", ""),
                st.text_input("DATE (B2):", ""),
                st.text_input("FROM (B3):", "").upper(),
                st.text_input("TO (B4):", "").upper(),
                st.text_input("INVOICE NO (B5):", ""),
            ]

        with col2:
            # Inputs for cells B6-B9
            b6_b9_data = [
                st.text_input("EWAY BILL NO (B6):", ""),
                st.text_input("TRUCK NO (B7):", ""),
                st.text_input("CONSIGNEE (B8):", "").upper(),
                st.text_input("PRODUCT QUANTITY (B9):", ""),
            ]
            c8_data = st.text_input("CONSIGNEE PHONE (C8):", "")

        # Submit button
        if st.button("Update Google Sheet"):
            try:
                # Combine all inputs for updating
                b1_b9_values = [[value] for value in (b1_b5_data + b6_b9_data)]  # 2D list for B1-B9
                c8_values = [[c8_data]]  # 2D list for C8

                # Update Google Sheets
                update_cells("Sheet2!B1:B9", b1_b9_values)
                update_cells("Sheet2!C8", c8_values)

                st.success("Google Sheet updated successfully!")
                
                # Save entered data to a DataFrame for display
                user_data = {
                    "GR NO (B1)": b1_b5_data[0],
                    "DATE (B2)": b1_b5_data[1],
                    "FROM (B3)": b1_b5_data[2],
                    "TO (B4)": b1_b5_data[3],
                    "INVOICE NO (B5)": b1_b5_data[4],
                    "EWAY BILL NO (B6)": b6_b9_data[0],
                    "TRUCK NO (B7)": b6_b9_data[1],
                    "CONSIGNEE (B8)": b6_b9_data[2],
                    "PRODUCT QUANTITY (B9)": b6_b9_data[3],
                    "CONSIGNEE PHONE (C8)": c8_data,
                }
                
                save_to_csv(user_data)

                df = pd.DataFrame([user_data])  # Convert to DataFrame
                st.subheader("Entered Information:")
                st.dataframe(df)  # Display in a table

            except Exception as e:
                st.error(f"Error updating Google Sheet: {e}")
            
    # Button to show all previously entered information from the CSV file
    if st.button("Show All Information"):
        # Check if the file exists and read it
        if os.path.exists(DATA_FILE):
            all_data_df = pd.read_csv(DATA_FILE)
            st.subheader("All Entered Information:")
            st.dataframe(all_data_df)  # Display the full list of entries
        else:
            st.info("No information entered yet.")
