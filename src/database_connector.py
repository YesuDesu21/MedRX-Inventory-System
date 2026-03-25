# database_connector.py
import os
from dotenv import load_dotenv
import sqlite3
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

#SQLite connection
def create_connection():
    try:
        conn = sqlite3.connect("data/medrx_inventory.db")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_cursor(conn):
    if conn:
        return conn.cursor()
    return None

#Google Sheets connection
def sheets_connection():
    try:
        creds = Credentials.from_service_account_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Google Sheets connection error: {e}")
        return None

def sheet_id():
    return os.getenv("SPREADSHEET_ID")