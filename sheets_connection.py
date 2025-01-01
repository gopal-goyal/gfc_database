from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os
from config import DEV_ENV, SPREADSHEET_ID
from dotenv import load_dotenv

load_dotenv()

if DEV_ENV:
    cred_path = os.getenv('FIREBASE_CRED_PATH')

# Define the scope for accessing Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

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