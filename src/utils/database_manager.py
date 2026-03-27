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
        self.cursor.execute("SELECT * FROM products")
        data = self.cursor.fetchall()
        return data

    def update_inventory(self, product_name, quantity, unit_cost, price, expiration_date, product_type=None, medicine_type=None):
        try:
            # Handle medicine_type logic if provided
            if product_type and medicine_type:
                if product_type.lower() == 'medicine':
                    if medicine_type not in ['branded', 'unbranded']:
                        medicine_type = 'branded'
                else:
                    medicine_type = 'N/A'
            
            # Build dynamic SQL based on provided parameters
            if product_type and medicine_type:
                sql = '''UPDATE products SET quantity = ?, unit_cost = ?, price = ?, expiration_date = ?, product_type = ?, medicine_type = ?, updated_date = datetime('now', 'localtime') WHERE product_name = ?'''
                self.cursor.execute(sql, (quantity, unit_cost, price, expiration_date, product_type, medicine_type, product_name))
            else:
                sql = '''UPDATE products SET quantity = ?, unit_cost = ?, price = ?, expiration_date = ?, updated_date = datetime('now', 'localtime') WHERE product_name = ?'''
                self.cursor.execute(sql, (quantity, unit_cost, price, expiration_date, product_name))
            
            self.conn.commit()
            self.sync_manager.sync_to_sheets()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False

    def add_product_with_id(self, product_id, product_name, product_type, quantity, unit_cost, price, medicine_type, expiration_date):
        """Add product with specific ID"""
        try:
            # Set medicine_type based on product_type logic
            if product_type.lower() == 'medicine':
                if medicine_type not in ['branded', 'unbranded']:
                    medicine_type = 'branded'  # Default for medicines
            else:
                medicine_type = 'N/A'  # For non-medicines
            
            sql = '''INSERT INTO products (product_id, product_name, product_type, quantity, unit_cost, price, medicine_type, expiration_date, date_added, updated_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))'''
            self.cursor.execute(sql, (product_id, product_name, product_type, quantity, unit_cost, price, medicine_type, expiration_date))
            self.conn.commit()
            self.sync_manager.sync_to_sheets()
            print(f"Successfully added {product_name} with ID {product_id}")
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False

    def get_available_ids(self):
        """Get list of deleted IDs that can be reused"""
        self.cursor.execute("""
            WITH RECURSIVE seq(n) AS (
                SELECT 1
                UNION ALL
                SELECT n+1 FROM seq WHERE n < 1000
            )
            SELECT n FROM seq
            WHERE n NOT IN (SELECT product_id FROM products)
            AND n <= (SELECT COALESCE(MAX(product_id), 0) + 1 FROM products)
            ORDER BY n
        """)
        return [row[0] for row in self.cursor.fetchall()]
    def get_next_available_id(self):
        """Get the next available ID (reusing deleted IDs if possible)"""
        available_ids = self.get_available_ids()
        if available_ids:
            return available_ids[0]
        else:
            # No deleted IDs, get the next autoincrement
            self.cursor.execute("SELECT COALESCE(MAX(product_id), 0) + 1 FROM products")
            return self.cursor.fetchone()[0]
    
    def add_product(self, product_name, product_type, quantity, unit_cost, price, medicine_type, expiration_date):
        """Add product with automatic ID assignment (reuses deleted IDs)"""
        next_id = self.get_next_available_id()
        return self.add_product_with_id(next_id, product_name, product_type, quantity, unit_cost, price, medicine_type, expiration_date)

    def delete_item(self, product_id):
        try:
            self.cursor.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
            self.conn.commit()
            self.sync_manager.sync_to_sheets()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
