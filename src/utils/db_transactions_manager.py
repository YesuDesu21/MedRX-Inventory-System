from .database_connector import create_connection, create_cursor, sheets_connection, sheet_id
from .sync_database import SyncManager

class DBTransactionsManager:
    def __init__(self):
        self.conn = create_connection()
        self.cursor = create_cursor(self.conn)

        self.sheets_client = sheets_connection()
        self.sheet_id = sheet_id()
        self.sheet = None

        self.sync_manager = SyncManager(self)

    def create_transaction(self, user_id, items):
        """
        Create a new transaction with multiple items
        items: list of dicts with keys: item_id, quantity_bought, unit_price
        """
        try:
            # Calculate total price
            total_price = sum(item['quantity_bought'] * item['unit_price'] for item in items)
            
            # Create transaction record
            self.cursor.execute("""
                INSERT INTO transactions (user_id, total_price, date_processed)
                VALUES (?, ?, datetime('now', 'localtime'))
            """, (user_id, total_price))
            transaction_id = self.cursor.lastrowid
            
            # Add transaction items and update inventory
            for item in items:
                # Add to transaction_items
                self.cursor.execute("""
                    INSERT INTO transaction_items (transaction_id, item_id, quantity_bought, unit_price)
                    VALUES (?, ?, ?, ?)
                """, (transaction_id, item['item_id'], item['quantity_bought'], item['unit_price']))
                
                # Subtract from inventory
                self.cursor.execute("""
                    UPDATE products SET quantity = quantity - ?, updated_date = datetime('now', 'localtime')
                    WHERE item_id = ?
                """, (item['quantity_bought'], item['item_id']))
            
            self.conn.commit()
            self.sync_manager.sync_to_sheets()
            return transaction_id
        except Exception as e:
            print(f"Error creating transaction: {e}")
            self.conn.rollback()
            return False
    
    def get_transactions(self, search_term=None, date_from=None, date_to=None):
        """Get transactions with optional search filters - returns each item as separate row"""
        try:
            base_query = """
                SELECT t.transaction_id, 
                       p.item_name,
                       ti.quantity_bought,
                       ti.unit_price,
                       t.total_price, 
                       t.date_processed,
                       ti.transaction_item_id
                FROM transactions t
                LEFT JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
                LEFT JOIN products p ON ti.item_id = p.item_id
                WHERE 1=1
            """
            params = []
            
            if search_term:
                base_query += " AND (t.transaction_id LIKE ? OR p.item_name LIKE ?)"
                params.extend([f"%{search_term}%", f"%{search_term}%"])
            
            if date_from:
                base_query += " AND t.date_processed >= ?"
                params.append(date_from)
            
            if date_to:
                base_query += " AND t.date_processed <= ?"
                params.append(date_to)
            
            base_query += " ORDER BY t.transaction_id DESC, ti.transaction_item_id"
            
            self.cursor.execute(base_query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting transactions: {e}")
            return []
    
    def get_transaction_items(self, transaction_id):
        """Get all items in a transaction"""
        try:
            self.cursor.execute("""
                SELECT ti.transaction_item_id, ti.item_id, ti.quantity_bought, ti.unit_price,
                       p.item_name, p.product_type
                FROM transaction_items ti
                JOIN products p ON ti.item_id = p.item_id
                WHERE ti.transaction_id = ?
            """, (transaction_id,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error getting transaction items: {e}")
            return []
    
    def update_transaction_item(self, transaction_item_id, new_quantity):
        """
        Update transaction item quantity and adjust inventory
        Returns True if successful
        """
        try:
            # Get current item details
            self.cursor.execute("""
                SELECT transaction_id, item_id, quantity_bought
                FROM transaction_items
                WHERE transaction_item_id = ?
            """, (transaction_item_id,))
            current = self.cursor.fetchone()
            
            if not current:
                return False
            
            transaction_id, item_id, old_quantity = current
            quantity_diff = new_quantity - old_quantity
            
            # Update transaction item
            self.cursor.execute("""
                UPDATE transaction_items SET quantity_bought = ?
                WHERE transaction_item_id = ?
            """, (new_quantity, transaction_item_id))
            
            # Adjust inventory (add back old quantity, subtract new quantity)
            self.cursor.execute("""
                UPDATE products SET quantity = quantity - ?, updated_date = datetime('now', 'localtime')
                WHERE item_id = ?
            """, (quantity_diff, item_id))
            
            # Recalculate transaction total
            self.cursor.execute("""
                UPDATE transactions SET total_price = (
                    SELECT SUM(quantity_bought * unit_price)
                    FROM transaction_items
                    WHERE transaction_id = ?
                )
                WHERE transaction_id = ?
            """, (transaction_id, transaction_id))
            
            self.conn.commit()
            self.sync_manager.sync_to_sheets()
            return True
        except Exception as e:
            print(f"Error updating transaction item: {e}")
            self.conn.rollback()
            return False
    
    def delete_transaction_item(self, transaction_item_id):
        """
        Delete transaction item and restore inventory
        Returns True if successful
        """
        try:
            # Get item details before deletion
            self.cursor.execute("""
                SELECT transaction_id, item_id, quantity_bought
                FROM transaction_items
                WHERE transaction_item_id = ?
            """, (transaction_item_id,))
            item = self.cursor.fetchone()
            
            if not item:
                return False
            
            transaction_id, item_id, quantity = item
            
            # Delete transaction item
            self.cursor.execute("""
                DELETE FROM transaction_items WHERE transaction_item_id = ?
            """, (transaction_item_id,))
            
            # Restore inventory
            self.cursor.execute("""
                UPDATE products SET quantity = quantity + ?, updated_date = datetime('now', 'localtime')
                WHERE item_id = ?
            """, (quantity, item_id))
            
            # Recalculate transaction total
            self.cursor.execute("""
                UPDATE transactions SET total_price = (
                    SELECT COALESCE(SUM(quantity_bought * unit_price), 0)
                    FROM transaction_items
                    WHERE transaction_id = ?
                )
                WHERE transaction_id = ?
            """, (transaction_id, transaction_id))
            
            self.conn.commit()
            self.sync_manager.sync_to_sheets()
            return True
        except Exception as e:
            print(f"Error deleting transaction item: {e}")
            self.conn.rollback()
            return False
    
    def search_products_for_transaction(self, search_term=None):
        """Get products available for transaction (with quantity > 0)"""
        try:
            if search_term:
                self.cursor.execute("""
                    SELECT item_id, item_name, product_type, quantity, price, unit_cost, medicine_type, expiration_date
                    FROM products
                    WHERE quantity > 0 AND (item_name LIKE ? OR product_type LIKE ?)
                    ORDER BY item_name
                """, (f"%{search_term}%", f"%{search_term}%"))
            else:
                self.cursor.execute("""
                    SELECT item_id, item_name, product_type, quantity, price, unit_cost, medicine_type, expiration_date
                    FROM products
                    WHERE quantity > 0
                    ORDER BY item_name
                """)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error searching products: {e}")
            return []