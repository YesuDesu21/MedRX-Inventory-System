import os
from dotenv import load_dotenv

load_dotenv()

sheet_id = os.getenv("SPREADSHEET_ID")
print(f"Connected to Sheet: {sheet_id}")

