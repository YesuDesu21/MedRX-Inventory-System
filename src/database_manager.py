from src.database_connector import create_connection, create_cursor, sheets_connection, sheet_id

class DatabaseManager:
    def __init__(self):
        self.conn = create_connection()
        self.cursor = create_cursor(self.conn)

        self.sheets_client = sheets_connection()
        self.sheet_id = sheet_id()


    def get_inventory(self):
        self.cursor.execute('SELECT * FROM items')
        data = self.cursor.fetchall()
        return data

    def update_inventory(self, name, qty, price):
        try:
            sql = '''UPDATE items SET quantity = ?, price = ?, updated_date = datetime('now', 'localtime') WHERE item_name = ?'''
            self.cursor.execute(sql, (qty, price, name))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error updating item: {e}")
            return False

    def add_item(self, name, qty, price):
        try:
            sql = '''INSERT INTO items (item_name, quantity, price, created_date, updated_date)
                    VALUES (?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))'''
            self.cursor.execute(sql, (name, qty, price))
            self.conn.commit() # This "saves" the changes like clicking Write Changes
            print(f"Successfully added {name}")
            return True
        except Exception as e:
            print(f"Error adding item: {e}")
            return False

    def delete_item(self, item_id):
        try:
            self.cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting item: {e}")
            return False


# Example usage
# if __name__ == "__main__":
#     db = DatabaseManager()
#     # db.add_item("Test Item", 10, 100)
#     data = db.get_inventory()
#     if data is not None:
#         print(f"--- Found {len(data)} Items ---")
#         print(data)
#     else:
#         print("No data retrieved - check database connection")

