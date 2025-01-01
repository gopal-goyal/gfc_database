from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from firebase_admin import credentials
import os
from config import DEV_ENV, SPREADSHEET_ID
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
# Define the scope for accessing Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

if DEV_ENV:
    cred_path = os.getenv('FIREBASE_CRED_PATH')
else:
    # Define the credentials for production using Streamlit secrets
    firebase_credentials = st.secrets["firebase"]
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
    # Use the certificate for Google Sheets API
    credentials = Credentials.from_service_account_info(cred, scopes=SCOPES)

# Authenticate with Google Sheets API
credentials = Credentials.from_service_account_file(cred_path, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

def read_google_sheet(range_name):
    """Reads data from the Google Sheet in the given range."""
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    return result.get('values', [])

def write_google_sheet(range_name, values):
    """Writes data to the Google Sheet in the specified range."""
    sheet = service.spreadsheets()
    body = {'values': values}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    return result

def update_cells(range_name, values):
    """
    Update specific cells in the Google Sheet.
    Args:
        range_name (str): The range to update (e.g., 'Sheet1!B1:B10').
        values (list): The data to write as a 2D list.
    """
    sheet = service.spreadsheets()
    body = {'values': values}
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    return result