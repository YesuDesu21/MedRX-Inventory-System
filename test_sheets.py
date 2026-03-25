#!/usr/bin/env python3

import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

def test_sheets_connection():
    try:
        print("Testing Google Sheets connection...")
        
        # Step 1: Check credentials file
        if not os.path.exists('credentials.json'):
            print("❌ ERROR: credentials.json not found")
            return False
        print("✅ credentials.json found")
        
        # Step 2: Check environment variable
        sheet_id = os.getenv("SPREADSHEET_ID")
        if not sheet_id:
            print("❌ ERROR: SPREADSHEET_ID not found in .env")
            return False
        print(f"✅ SPREADSHEET_ID found: {sheet_id}")
        
        # Step 3: Test credentials loading
        try:
            creds = Credentials.from_service_account_file(
                'credentials.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            print("✅ Credentials loaded successfully")
        except Exception as e:
            print(f"❌ ERROR loading credentials: {e}")
            return False
        
        # Step 4: Test authentication
        try:
            client = gspread.authorize(creds)
            print("✅ Authentication successful")
        except Exception as e:
            print(f"❌ ERROR during authentication: {e}")
            return False
        
        # Step 5: Test sheet access
        try:
            sheet = client.open_by_key(sheet_id).sheet1
            print("✅ Sheet access successful")
        except Exception as e:
            print(f"❌ ERROR accessing sheet: {e}")
            print("💡 Make sure the service account email has 'Editor' access to the Google Sheet")
            return False
        
        # Step 6: Test write permission
        try:
            sheet.append_row(["Test", "Data"])
            print("✅ Write permission successful")
        except Exception as e:
            print(f"❌ ERROR writing to sheet: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_sheets_connection()
