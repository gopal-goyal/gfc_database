import os
import streamlit as st
from io import BytesIO
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from config import DEV_ENV, SPREADSHEET_ID
import os
from dotenv import load_dotenv

load_dotenv()

if DEV_ENV:
    cred_path = os.getenv('FIREBASE_CRED_PATH')

# Define the SCOPES for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/spreadsheets.readonly']

# PDF export options
EXPORT_MIME_TYPE = 'application/pdf'

def authenticate_google_drive():
    """Authenticate and return the Google Drive API service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    return service

def download_sheet_as_pdf():
    """Download the Google Sheet as a PDF."""
    service = authenticate_google_drive()
    file_id = SPREADSHEET_ID
    request = service.files().export_media(fileId=file_id, mimeType=EXPORT_MIME_TYPE)
    
    # Save the PDF to memory (BytesIO)
    pdf_data = BytesIO(request.execute())
    return pdf_data

