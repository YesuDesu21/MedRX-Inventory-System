import time
import re

class SyncManager:
    def __init__(self, db_manager):
        self.db = db_manager

    # Extracts the ID from a URL like:
    # https://docs.google.com/spreadsheets/d/1AbC_123_XYZ/edit#gid=0
    def link_user_spreadsheet(self, url):
        """
        Extracts the ID from a URL like:
        https://docs.google.com/spreadsheets/d/1AbC_123_XYZ/edit#gid=0
        """
        try:
            # Regex to find the ID between /d/ and /edit
            match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
            if match:
                spreadsheet_id = match.group(1)
                
                # Save this ID to your local SQLite settings table
                self.db.update_setting("spreadsheet_id", spreadsheet_id)
                
                # Reset the internal sheet connection so it uses the new ID next time
                self.sheet = None 
                print(f"Successfully linked to Sheet ID: {spreadsheet_id}")
                return True
            else:
                print("Invalid Google Sheets URL.")
                return False
        except Exception as e:
            print(f"Error linking sheet: {e}")
            return False

    # Downloads data from the linked GSheet into local SQLite
    def import_from_sheet(self):
        """Downloads data from the linked GSheet into local SQLite"""
        try:
            # 1. Connect to the user's specific sheet
            sheet_id = self.db.get_setting("spreadsheet_id")
            sheet = self.db.sheets_client.open_by_key(sheet_id).sheet1
            
            # 2. Get all records as a list of dictionaries
            records = sheet.get_all_records()
            
            if not records:
                print("⚠️ The sheet is empty. Nothing to import.")
                return False

            # 3. Clear local items and replace with Cloud items
            # (Warning: This overwrites local data!)
            self.db.cursor.execute("DELETE FROM items")
            
            for row in records:
                # Map the GSheet columns to your SQLite columns
                self.db.add_item(
                    name=row.get('Item Name') or row.get('Name'),
                    qty=row.get('Quantity') or row.get('Qty'),
                    capital=row.get('Capital (Puhunan)') or 0,
                    price=row.get('Price (Benta)') or 0,
                    expiry=row.get('Expiration') or ""
                )
            
            print(f"Successfully imported {len(records)} items from the Cloud!")
            return True
        except Exception as e:
            print(f"Import Error: {e}")
            return False

    # Whenever user makes updates, this sends data to local and cloud storage
    def sync_to_sheets(self):
        try:
            # Open the specific spreadsheet using the ID from your .env
            if not hasattr(self, 'sheet') or self.sheet is None:
                self.sheet = self.db.sheets_client.open_by_key(self.db.sheet_id).sheet1
            
            # Get the latest data from your SQLite table and Convert tuples to lists for gspread compatibility
            inventory_data = [list(row) for row in self.db.get_inventory()]
            if not inventory_data:
                print("No data in SQLite to sync.")
                return

            # Clear data and ensure headers exist
            all_data = self.sheet.get_all_values()
            
            # Check if headers exist (first row should contain headers)
            has_headers = all_data and len(all_data) > 0 and "ID" in str(all_data[0])
            
            if not has_headers:
                # Sheet is empty or has no headers - add them
                headers = ["ID", "Item Name", "Quantity", "Capital (Puhunan)", "Price (Benta)", "Expiration", "Date Added", "Last Updated"]
                self.sheet.append_row(headers)
                print("Added headers to Google Sheet")
            else:
                # Clear only data rows, preserve headers
                self.sheet.batch_clear(["A2:H"])
            
            for i in range(0, len(inventory_data), 100):  # 100 rows at a time
                self.sheet.append_rows(inventory_data[i:i+100])
            print("Successfully synced SQLite data to Google Sheets!")
            return True
        
        except Exception as e:
            print(f"Google Sheets Sync Error: {e}")
            return False