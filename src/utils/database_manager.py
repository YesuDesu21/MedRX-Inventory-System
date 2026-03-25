from src.utils.database_connector import create_connection, create_cursor, sheets_connection, sheet_id
from src.utils.sync_database import SyncManager

class DatabaseManager:
    def __init__(self):
        self.conn = create_connection()
        self.cursor = create_cursor(self.conn)

        self.sheets_client = sheets_connection()
        self.sheet_id = sheet_id()
        self.sheet = None

        self.sync_manager = SyncManager(self)

    def get_inventory(self):
        self.cursor.execute('SELECT * FROM items')
        data = self.cursor.fetchall()
        return data

    def update_inventory(self, name, qty, capital, price, expiration_date):
        try:
            sql = '''UPDATE items SET quantity = ?, capital = ?, price = ?, expiration_date = ?, updated_date = datetime('now', 'localtime') WHERE item_name = ?'''
            self.cursor.execute(sql, (qty, capital, price, expiration_date, name))
            self.conn.commit()
            self.sync_manager.sync_to_sheets()
            return True
        except Exception as e:
            print(f"Error updating item: {e}")
            return False

    def add_item(self, name, qty, capital, price, expiration_date):
        try:
            sql = '''INSERT INTO items (item_name, quantity, capital, price, expiration_date, date_added, updated_date)
                    VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))'''
            self.cursor.execute(sql, (name, qty, capital, price, expiration_date))
            self.conn.commit() # This "saves" the changes like clicking Write Changes
            self.sync_manager.sync_to_sheets()
            print(f"Successfully added {name}")
            return True
        except Exception as e:
            print(f"Error adding item: {e}")
            return False

    def delete_item(self, item_id):
        try:
            self.cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
            self.conn.commit()
            self.sync_manager.sync_to_sheets()
            return True
        except Exception as e:
            print(f"Error deleting item: {e}")
            return False
    
    
