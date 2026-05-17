import customtkinter as ctk
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
from src.utils.db_transactions_manager import DBTransactionsManager
from src.utils.logger import log_user_action, log_database_operation, log_error

class Transaction:
    def __init__(self, parent):
        self.parent = parent
        self.db_manager = DBTransactionsManager()
        self.create_transaction_ui()
        log_user_action("Opened Transactions", "Transactions")

    def center_screen(self, dialog):
        """Center the dialog on the main window"""
        dialog.update_idletasks()
        dialog.update()
        
        # Get dialog dimensions
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        
        # Get the root window (main window) - need to traverse up the hierarchy
        parent = self.parent
        while parent.master:  # Traverse up to get the root window
            parent = parent.master
        
        # Get main window position and dimensions
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # Calculate center relative to main window
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')

    def create_transaction_ui(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Transactions", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(anchor='w', pady=(0, 10))
        
        # Search frame
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(search_frame, text="Search:", font=ctk.CTkFont(size=11)).pack(side='left', padx=(0, 5))
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var, width=200, font=ctk.CTkFont(size=11), text_color="white")
        self.search_entry.pack(side='left', padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.filter_transactions)
        
        # Sort by dropdown
        sort_frame = ctk.CTkFrame(search_frame)
        sort_frame.pack(side='left', padx=(0, 10))

        ctk.CTkLabel(sort_frame, text="Sort by:", font=ctk.CTkFont(size=11)).pack(side='left', padx=(0, 5))
        self.sort_by_options = ["Transaction ID", "Date Processed", "Item Name", "Quantity", "Unit Price", "Total Price"]
        self.sort_by_var = ctk.StringVar(value=self.sort_by_options[0])
        self.sort_by_option_menu = ctk.CTkOptionMenu(sort_frame, variable=self.sort_by_var, values=self.sort_by_options, font=ctk.CTkFont(size=11), command=self.filter_transactions)
        self.sort_by_option_menu.pack(side='left')
        
        # Buttons
        button_frame = ctk.CTkFrame(search_frame)
        button_frame.pack(side='right')
        
        ctk.CTkButton(button_frame, text="Add Transaction", command=self.open_add_transaction_modal, font=ctk.CTkFont(size=11)).pack(side='left', padx=5)
        ctk.CTkButton(button_frame, text="Refresh", command=self.load_transactions, font=ctk.CTkFont(size=11)).pack(side='left', padx=5)
        ctk.CTkButton(button_frame, text="Delete Transaction", command=self.delete_transaction, fg_color="red", font=ctk.CTkFont(size=11)).pack(side='left', padx=5)
        
        # Transactions table
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # Treeview for transactions
        columns = ('Transaction ID', 'Item', 'Quantity', 'Unit Price', 'Total Price', 'Date Processed')
        self.transaction_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure larger font for treeview
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 11))
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))
        style.configure("Treeview", rowheight=30)  # Increase row height for better readability
        
        # Define headings
        self.transaction_tree.heading('Transaction ID', text='Transaction ID')
        self.transaction_tree.heading('Item', text='Item')
        self.transaction_tree.heading('Quantity', text='Quantity')
        self.transaction_tree.heading('Unit Price', text='Unit Price')
        self.transaction_tree.heading('Total Price', text='Total Price')
        self.transaction_tree.heading('Date Processed', text='Date Processed')
        
        # Configure column widths
        self.transaction_tree.column('Transaction ID', width=100)
        self.transaction_tree.column('Item', width=200)
        self.transaction_tree.column('Quantity', width=80)
        self.transaction_tree.column('Unit Price', width=80)
        self.transaction_tree.column('Total Price', width=100)
        self.transaction_tree.column('Date Processed', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transaction_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind double-click for viewing details
        self.transaction_tree.bind('<Double-1>', self.view_transaction_details)
        
        # Load initial data
        self.load_transactions()

    def load_transactions(self):
        """Load transactions into treeview"""
        # Clear existing items
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        # Get filtered transactions
        search_term = self.search_var.get().strip()
        sort_by = self.sort_by_var.get()
        
        transactions = self.db_manager.get_transactions(search_term, None, None)
        log_database_operation("Retrieved transaction data", "transactions", f"Loaded {len(transactions)} records")
        
        # Sort transactions based on selected option
        if sort_by == "Transaction ID":
            transactions.sort(key=lambda x: x[0], reverse=True)
        elif sort_by == "Date Processed":
            transactions.sort(key=lambda x: x[5] if len(x) > 5 else "", reverse=True)
        elif sort_by == "Item Name":
            transactions.sort(key=lambda x: x[1] if len(x) > 1 else "", reverse=False)
        elif sort_by == "Quantity":
            transactions.sort(key=lambda x: x[2] if len(x) > 2 else 0, reverse=False)
        elif sort_by == "Unit Price":
            transactions.sort(key=lambda x: x[3] if len(x) > 3 else 0, reverse=False)
        elif sort_by == "Total Price":
            transactions.sort(key=lambda x: x[4] if len(x) > 4 else 0, reverse=False)
        
        # Track transaction IDs to avoid duplicate headers
        current_transaction_id = None
        
        for transaction in transactions:
            transaction_id = transaction[0]
            item_name = transaction[1] if transaction[1] else ""
            quantity = transaction[2] if transaction[2] else ""
            unit_price = transaction[3] if transaction[3] else 0
            total_price = transaction[4] if transaction[4] else 0
            date_processed = transaction[5] if len(transaction) > 5 else ""
            
            # Format the values for display
            if current_transaction_id != transaction_id:
                # First item for this transaction - show all details
                values = (
                    transaction_id,
                    item_name,
                    f"x{quantity}" if quantity else "",
                    f"₱{unit_price:.2f}" if unit_price else "",
                    f"₱{total_price:.2f}" if total_price else "",
                    date_processed
                )
                current_transaction_id = transaction_id
            else:
                # Additional items for same transaction - only show item details
                values = (
                    "",  # Empty transaction ID
                    item_name,
                    f"x{quantity}" if quantity else "",
                    f"₱{unit_price:.2f}" if unit_price else "",
                    "",  # Empty total price
                    ""   # Empty date
                )
            
            self.transaction_tree.insert('', 'end', values=values)

    def filter_transactions(self, event=None):
        """Filter transactions based on search and date criteria"""
        self.load_transactions()

    def open_add_transaction_modal(self):
        """Open modal to add new transaction"""
        log_user_action("Opened Add Transaction dialog", "Transactions")
        modal = AddTransactionModal(self.parent, self.db_manager, self.load_transactions)

    def view_transaction_details(self, event):
        """View and edit transaction details"""
        selection = self.transaction_tree.selection()
        if not selection:
            return
        
        item = self.transaction_tree.item(selection[0])
        transaction_id = item['values'][0]
        
        # If transaction_id is empty (additional row), find the parent transaction ID
        if not transaction_id:
            # Look for the first row above that has a transaction ID
            selected_index = self.transaction_tree.index(selection[0])
            for i in range(selected_index - 1, -1, -1):
                parent_item = self.transaction_tree.get_children()[i]
                parent_values = self.transaction_tree.item(parent_item)['values']
                if parent_values[0]:  # If this row has a transaction ID
                    transaction_id = parent_values[0]
                    break
        
        if transaction_id:
            modal = TransactionDetailsModal(self.parent, self.db_manager, transaction_id, self.load_transactions)

    def delete_transaction(self):
        """Delete selected transaction and restore inventory"""
        selection = self.transaction_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a transaction to delete.")
            return
        
        item = self.transaction_tree.item(selection[0])
        transaction_id = item['values'][0]
        
        # If transaction_id is empty (additional row), find the parent transaction ID
        if not transaction_id:
            # Look for the first row above that has a transaction ID
            selected_index = self.transaction_tree.index(selection[0])
            for i in range(selected_index - 1, -1, -1):
                parent_item = self.transaction_tree.get_children()[i]
                parent_values = self.transaction_tree.item(parent_item)['values']
                if parent_values[0]:  # If this row has a transaction ID
                    transaction_id = parent_values[0]
                    break
        
        if not transaction_id:
            messagebox.showwarning("No Transaction", "No transaction found to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this transaction? This will restore all items to inventory."):
            # Get all transaction items to restore inventory
            items = self.db_manager.get_transaction_items(transaction_id)
            
            # Delete each transaction item (which restores inventory)
            success = True
            for transaction_item in items:
                if not self.db_manager.delete_transaction_item(transaction_item[0]):
                    success = False
                    break
            
            if success:
                # Delete the transaction record
                try:
                    self.db_manager.cursor.execute("DELETE FROM transactions WHERE transaction_id = ?", (transaction_id,))
                    self.db_manager.conn.commit()
                    self.db_manager.sync_manager.sync_to_sheets()
                    messagebox.showinfo("Success", "Transaction deleted and inventory restored.")
                    self.load_transactions()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete transaction: {e}")
            else:
                messagebox.showerror("Error", "Failed to delete transaction items.")


class AddTransactionModal:
    def __init__(self, parent, db_manager, refresh_callback):
        self.parent = parent
        self.db_manager = db_manager
        self.refresh_callback = refresh_callback
        self.selected_items = []  # List of (item_id, item_name, quantity, unit_price)
        
        self.window = ctk.CTkToplevel(parent)
        self.window.title("Add Transaction")
        self.window.geometry("650x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_ui()
        
        # Center the modal on screen
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def create_ui(self):
        # Main container
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        # Product search section
        search_frame = ctk.CTkFrame(main_frame)
        search_frame.pack(fill='x', pady=(0, 15))

        search_label = ctk.CTkLabel(search_frame, text="Search Products", font=ctk.CTkFont(size=14, weight="bold"))
        search_label.pack(anchor='w', padx=15, pady=(10, 5))

        search_input_frame = ctk.CTkFrame(search_frame)
        search_input_frame.pack(fill='x', padx=15, pady=(0, 10))

        ctk.CTkLabel(search_input_frame, text="Search:", font=ctk.CTkFont(size=12)).pack(side='left', padx=(0, 5))
        self.product_search_var = tk.StringVar()
        self.product_search_entry = ctk.CTkEntry(search_input_frame, textvariable=self.product_search_var, width=250, font=ctk.CTkFont(size=12), height=32)
        self.product_search_entry.pack(side='left', padx=(0, 10))
        self.product_search_entry.bind('<KeyRelease>', self.search_products)

        # Products list
        products_frame = ctk.CTkFrame(main_frame)
        products_frame.pack(fill='both', expand=True, pady=(0, 15))

        products_label = ctk.CTkLabel(products_frame, text="Available Products", font=ctk.CTkFont(size=14, weight="bold"))
        products_label.pack(anchor='w', padx=15, pady=(10, 5))

        # Products treeview
        product_columns = ('ID', 'Name', 'Type', 'Available Qty', 'Price')
        self.products_tree = ttk.Treeview(products_frame, columns=product_columns, show='headings', height=8)

        for col in product_columns:
            self.products_tree.heading(col, text=col)

        self.products_tree.column('ID', width=50)
        self.products_tree.column('Name', width=200)
        self.products_tree.column('Type', width=100)
        self.products_tree.column('Available Qty', width=100)
        self.products_tree.column('Price', width=80)

        product_scrollbar = ttk.Scrollbar(products_frame, orient='vertical', command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=product_scrollbar.set)

        self.products_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        product_scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)

        # Bind double-click to add product
        self.products_tree.bind('<Double-1>', self.add_product_to_transaction)

        # Selected items section
        selected_frame = ctk.CTkFrame(main_frame)
        selected_frame.pack(fill='both', expand=True, pady=(0, 15))

        selected_label = ctk.CTkLabel(selected_frame, text="Transaction Items", font=ctk.CTkFont(size=14, weight="bold"))
        selected_label.pack(anchor='w', padx=15, pady=(10, 5))

        # Selected items treeview
        selected_columns = ('ID', 'Name', 'Quantity', 'Unit Price', 'Total')
        self.selected_tree = ttk.Treeview(selected_frame, columns=selected_columns, show='headings', height=6)

        for col in selected_columns:
            self.selected_tree.heading(col, text=col)

        self.selected_tree.column('ID', width=50)
        self.selected_tree.column('Name', width=200)
        self.selected_tree.column('Quantity', width=80)
        self.selected_tree.column('Unit Price', width=80)
        self.selected_tree.column('Total', width=80)

        selected_scrollbar = ttk.Scrollbar(selected_frame, orient='vertical', command=self.selected_tree.yview)
        self.selected_tree.configure(yscrollcommand=selected_scrollbar.set)

        self.selected_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        selected_scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)

        # Buttons for selected items
        selected_buttons_frame = ctk.CTkFrame(selected_frame)
        selected_buttons_frame.pack(fill='x', padx=15, pady=10)

        ctk.CTkButton(selected_buttons_frame, text="Remove Item", command=self.remove_selected_item, font=ctk.CTkFont(size=12), width=120, height=32).pack(side='left', padx=5)
        ctk.CTkButton(selected_buttons_frame, text="Edit Quantity", command=self.edit_item_quantity, font=ctk.CTkFont(size=12), width=120, height=32).pack(side='left', padx=5)
        ctk.CTkButton(selected_buttons_frame, text="Save", command=self.save_transaction, font=ctk.CTkFont(size=12), width=120, height=32).pack(side='left', padx=5)

        # Total and action buttons
        bottom_frame = ctk.CTkFrame(main_frame)
        bottom_frame.pack(fill='x', pady=(15, 0))

        self.total_label = ctk.CTkLabel(bottom_frame, text="Total: ₱0.00", font=ctk.CTkFont(size=16, weight="bold"))
        self.total_label.pack(side='left', padx=15, pady=10)

        button_frame = ctk.CTkFrame(bottom_frame)
        button_frame.pack(side='right', padx=15, pady=10)

        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=self.window.destroy, font=ctk.CTkFont(size=12), width=120, height=35)
        cancel_btn.pack(side='left', padx=(0, 10))

        save_btn = ctk.CTkButton(button_frame, text="Save Transaction", command=self.save_transaction, font=ctk.CTkFont(size=12), width=140, height=35)
        save_btn.pack(side='left', padx=(10, 0))

        # Load initial products
        self.search_products()

    def search_products(self, event=None):
        """Search for available products"""
        search_term = self.product_search_var.get().strip()
        products = self.db_manager.search_products_for_transaction(search_term)
        
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Add products to treeview
        for product in products:
            self.products_tree.insert('', 'end', values=product)

    def add_product_to_transaction(self, event=None):
        """Add selected product to transaction"""
        selection = self.products_tree.selection()
        if not selection:
            return
        
        item = self.products_tree.item(selection[0])
        product_data = item['values']
        
        item_id = product_data[0]
        item_name = product_data[1]
        available_qty = product_data[3]
        unit_price = product_data[4]
        
        # Check if already added
        for selected_item in self.selected_items:
            if selected_item[0] == item_id:
                messagebox.showwarning("Already Added", "This item is already in the transaction.")
                return
        
        # Ask for quantity
        quantity_dialog = QuantityDialog(self.window, item_name, available_qty)
        self.window.wait_window(quantity_dialog.dialog)
        
        if quantity_dialog.result:
            quantity = quantity_dialog.result
            self.selected_items.append((item_id, item_name, quantity, unit_price))
            self.update_selected_items_display()

    def remove_selected_item(self):
        """Remove selected item from transaction"""
        selection = self.selected_tree.selection()
        if not selection:
            return
        
        item = self.selected_tree.item(selection[0])
        item_id = item['values'][0]
        
        self.selected_items = [item for item in self.selected_items if item[0] != item_id]
        self.update_selected_items_display()

    def edit_item_quantity(self):
        """Edit quantity of selected item"""
        selection = self.selected_tree.selection()
        if not selection:
            return
        
        item = self.selected_tree.item(selection[0])
        item_id = item['values'][0]
        item_name = item['values'][1]
        current_qty = item['values'][2]
        
        # Get available quantity from products
        product = self.db_manager.search_products_for_transaction()
        available_qty = 0
        for p in product:
            if p[0] == item_id:
                available_qty = p[3] + current_qty  # Add back current quantity to available
                break
        
        quantity_dialog = QuantityDialog(self.window, item_name, available_qty, current_qty)
        self.window.wait_window(quantity_dialog.dialog)
        
        if quantity_dialog.result:
            # Update the item in selected_items
            for i, (iid, name, qty, price) in enumerate(self.selected_items):
                if iid == item_id:
                    self.selected_items[i] = (item_id, item_name, quantity_dialog.result, price)
                    break
            self.update_selected_items_display()

    def update_selected_items_display(self):
        """Update the selected items treeview and total"""
        # Clear existing items
        for item in self.selected_tree.get_children():
            self.selected_tree.delete(item)
        
        total = 0
        for item_id, item_name, quantity, unit_price in self.selected_items:
            item_total = quantity * unit_price
            total += item_total
            self.selected_tree.insert('', 'end', values=(
                item_id, item_name, quantity, f"₱{unit_price:.2f}", f"₱{item_total:.2f}"
            ))
        
        self.total_label.configure(text=f"Total: ₱{total:.2f}")

    def save_transaction(self):
        """Save the transaction"""
        if not self.selected_items:
            messagebox.showwarning("No Items", "Please add at least one item to the transaction.")
            return
        
        try:
            # Prepare items for database
            items = []
            for item_id, item_name, quantity, unit_price in self.selected_items:
                items.append({
                    'item_id': item_id,
                    'quantity_bought': quantity,
                    'unit_price': unit_price
                })
            
            # Create transaction
            transaction_id = self.db_manager.create_transaction(items)
            
            if transaction_id:
                messagebox.showinfo("Success", f"Transaction created successfully with ID: {transaction_id}")
                self.refresh_callback()
                self.window.destroy()
            else:
                messagebox.showerror("Error", "Failed to create transaction.")
        except Exception as e:
            messagebox.showerror("Error", f"Error creating transaction: {e}")


class TransactionDetailsModal:
    def __init__(self, parent, db_manager, transaction_id, refresh_callback):
        self.parent = parent
        self.db_manager = db_manager
        self.transaction_id = transaction_id
        self.refresh_callback = refresh_callback
        
        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Transaction Details - ID: {transaction_id}")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_ui()
        
        # Center the modal on screen
        # Get the parent's center_screen method
        parent_instance = None
        for attr in dir(parent):
            if hasattr(getattr(parent, attr), 'center_screen'):
                parent_instance = getattr(parent, attr)
                break
        if parent_instance and hasattr(parent_instance, 'center_screen'):
            parent_instance.center_screen(self.window)
        else:
            # Fallback: create a simple center function
            self.window.update_idletasks()
            width = self.window.winfo_width()
            height = self.window.winfo_height()
            x = (self.window.winfo_screenwidth() // 2) - (width // 2)
            y = (self.window.winfo_screenheight() // 2) - (height // 2)
            self.window.geometry(f'{width}x{height}+{x}+{y}')

    def create_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Transaction info
        info_frame = ttk.LabelFrame(main_frame, text="Transaction Information")
        info_frame.pack(fill='x', pady=(0, 10))
        
        # Get transaction details
        transactions = self.db_manager.get_transactions()
        transaction_data = None
        for t in transactions:
            if t[0] == self.transaction_id:
                transaction_data = t
                break
        
        if transaction_data:
            ttk.Label(info_frame, text=f"Transaction ID: {transaction_data[0]}").pack(anchor='w', padx=10, pady=2)
            ttk.Label(info_frame, text=f"Date: {transaction_data[2]}").pack(anchor='w', padx=10, pady=2)
            ttk.Label(info_frame, text=f"User: {transaction_data[3]}").pack(anchor='w', padx=10, pady=2)
            
            # Handle total calculation - if it's a string of items, calculate from transaction items
            try:
                total_value = float(transaction_data[1])
            except (ValueError, TypeError):
                # If total is stored as string of items, calculate it from transaction items
                total_value = 0.0
                try:
                    items = self.db_manager.get_transaction_items(self.transaction_id)
                    for item in items:
                        total_value += item[2] * item[3]  # quantity * unit_price
                except:
                    total_value = 0.0
            
            ttk.Label(info_frame, text=f"Total: ₱{total_value:.2f}").pack(anchor='w', padx=10, pady=2)
        
        # Items list
        items_frame = ttk.LabelFrame(main_frame, text="Transaction Items")
        items_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Items treeview
        item_columns = ('Transaction Item ID', 'Item Name', 'Quantity', 'Unit Price', 'Total')
        self.items_tree = ttk.Treeview(items_frame, columns=item_columns, show='headings')
        
        for col in item_columns:
            self.items_tree.heading(col, text=col)
        
        self.items_tree.column('Transaction Item ID', width=100, anchor='center')
        self.items_tree.column('Item Name', width=180)
        self.items_tree.column('Quantity', width=70, anchor='center')
        self.items_tree.column('Unit Price', width=90, anchor='e')
        self.items_tree.column('Total', width=90, anchor='e')
        
        items_scrollbar = ttk.Scrollbar(items_frame, orient='vertical', command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=items_scrollbar.set)
        
        self.items_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        items_scrollbar.pack(side='right', fill='y', padx=(0, 10), pady=10)
        
        # Load items
        self.load_transaction_items()
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        # Create buttons with consistent styling and better spacing
        close_btn = ttk.Button(button_frame, text="Close", command=self.window.destroy)
        close_btn.pack(side='right', padx=(5, 0))
        
        edit_btn = ttk.Button(button_frame, text="Edit Quantity", command=self.edit_item_quantity)
        edit_btn.pack(side='right', padx=(5, 5))
            
        delete_btn = ttk.Button(button_frame, text="Delete Item", command=self.delete_item)
        delete_btn.pack(side='right', padx=(0, 5))

    def load_transaction_items(self):
        """Load transaction items"""
        items = self.db_manager.get_transaction_items(self.transaction_id)
        
        # Display each transaction item as separate row
        for item in items:
            transaction_item_id = item[0]  # Transaction item ID
            item_id = item[1]  # Product ID
            quantity = item[2]  # Quantity bought
            unit_price = float(item[3]) if item[3] else 0.0  # Unit price
            item_name = item[4]  # Product name
            item_total = quantity * unit_price
            
            self.items_tree.insert('', 'end', values=(
                transaction_item_id,
                item_name,  # Product name
                quantity,  # Quantity
                f"₱{unit_price:.2f}",
                f"₱{item_total:.2f}"
            ))

    def edit_item_quantity(self):
        """Edit quantity of selected item"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to edit.")
            return
        
        item = self.items_tree.item(selection[0])
        transaction_item_id = item['values'][0]
        item_name = item['values'][1]
        current_quantity = item['values'][2]
        
        quantity_dialog = QuantityDialog(self.window, item_name, 999, current_quantity)
        self.window.wait_window(quantity_dialog.dialog)
        
        if quantity_dialog.result:
            if self.db_manager.update_transaction_item(transaction_item_id, quantity_dialog.result):
                messagebox.showinfo("Success", "Item quantity updated successfully.")
                self.refresh_treeview()
            else:
                messagebox.showerror("Error", "Failed to update item quantity.")

    def delete_item(self):
        """Delete selected item"""
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select an item to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item? The quantity will be restored to inventory."):
            item = self.items_tree.item(selection[0])
            transaction_item_id = item['values'][0]
            
            if self.db_manager.delete_transaction_item(transaction_item_id):
                messagebox.showinfo("Success", "Item deleted and inventory restored.")
                self.refresh_treeview()
            else:
                messagebox.showerror("Error", "Failed to delete item.")

    def refresh_treeview(self):
        """Refresh the items treeview"""
        # Clear existing items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        # Reload items
        self.load_transaction_items()


class QuantityDialog:
    def __init__(self, parent, item_name, max_quantity, current_quantity=1):
        self.result = None
        
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title(f"Enter Quantity - {item_name}")
        self.dialog.geometry("320x150")  # Increased height to ensure buttons are visible
        self.dialog.resizable(False, False)  # Make modal non-resizable
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Main frame
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(main_frame, text=f"Item: {item_name}", font=ctk.CTkFont(size=12)).pack(anchor='w', pady=(0, 10))
        # ctk.CTkLabel(main_frame, text=f"Available: {max_quantity}", font=ctk.CTkFont(size=12)).pack(anchor='w', pady=(0, 10))
        
        # Quantity input
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill='x', pady=(0, 20))
        
        ctk.CTkLabel(input_frame, text="Quantity:", font=ctk.CTkFont(size=12)).pack(side='left')
        self.quantity_var = tk.StringVar(value=str(current_quantity))
        self.quantity_entry = ctk.CTkEntry(input_frame, textvariable=self.quantity_var, width=100, font=ctk.CTkFont(size=12), height=32)
        self.quantity_entry.pack(side='left', padx=(10, 0))
        self.quantity_entry.select_range(0, tk.END)
        self.quantity_entry.focus()
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill='x', pady=(10, 0))
        
        ctk.CTkButton(button_frame, text="OK", command=self.ok_clicked, font=ctk.CTkFont(size=12), width=80, height=32).pack(side='right', padx=(5, 0))
        ctk.CTkButton(button_frame, text="Cancel", command=self.cancel_clicked, font=ctk.CTkFont(size=12), width=80, height=32).pack(side='right')
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self.cancel_clicked())
        
        # Center the dialog on main window
        self.dialog.update_idletasks()
        self.dialog.update()
        
        # Get dialog dimensions
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        # Get the root window - traverse up hierarchy from parent
        parent = parent
        while parent.master:  # Traverse up to get the root window
            parent = parent.master
        
        # Get main window position and dimensions
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # Calculate center relative to main window
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.dialog.geometry(f'{dialog_width}x{dialog_height}+{x}+{y}')

    def ok_clicked(self):
        """Handle OK button click"""
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                messagebox.showwarning("Invalid Quantity", "Quantity must be greater than 0.")
                return
            self.result = quantity
            self.dialog.destroy()
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number.")

    def cancel_clicked(self):
        """Handle Cancel button click"""
        self.dialog.destroy()