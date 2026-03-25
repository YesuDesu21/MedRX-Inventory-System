import tkinter as tk
import tkinter.ttk as ttk
from src.utils.database_manager import DatabaseManager
from tkinter import messagebox

class Inventory:
    def __init__(self, parent):
        self.parent = parent
        self.db_manager = DatabaseManager()
        self.create_widgets()
        self.retrieve_inventory()

    def create_widgets(self):
        # Main frame for inventory
        self.inventory_frame = tk.Frame(self.parent, bg='white')
        self.inventory_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            self.inventory_frame,
            text="Inventory Management",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2E531D'
        )
        title_label.pack(pady=(0, 20))
        
        # Create container for treeview and scrollbar
        tree_container = tk.Frame(self.inventory_frame, bg='white')
        tree_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create Treeview for inventory grid inside container
        columns = ('ID', 'Item Name', 'Quantity', 'Capital', 'Price', 'Expiration Date', 'Created Date', 'Updated Date')
        
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings', height=15)
        
        # Define column headings and widths
        column_widths = {'ID': 50, 'Item Name': 150, 'Quantity': 80, 'Capital': 80, 'Price': 80, 'Expiration Date': 120, 'Created Date': 120, 'Updated Date': 120}
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor='center')
        
        # Add scrollbar inside container
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar in container
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.inventory_frame, bg='white')
        buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Search bar
        search_label = tk.Label(
            buttons_frame,
            text="Search:",
            bg='white',
            font=('Arial', 10, 'bold')
        )
        search_label.pack(pady=(0, 5))
        
        self.search_entry = tk.Entry(
            buttons_frame,
            font=('Arial', 10),
            width=20
        )
        self.search_entry.pack(fill=tk.X, pady=(0, 15))
        self.search_entry.bind('<KeyRelease>', self.filter_inventory)
        
        # Action buttons
        tk.Button(
            buttons_frame,
            text="Add New Item",
            command=self.add_new_stock,
            bg='#529133',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(
            buttons_frame,
            text="Update Selected",
            command=self.update_item,
            bg='#2E531D',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_item,
            bg='#d32f2f',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(
            buttons_frame,
            text="Refresh",
            command=self.retrieve_inventory,
            bg='#1976d2',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(fill=tk.X)

    def center_screen(self, dialog):
        """Center the dialog on the screen"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

    def filter_inventory(self, event=None):
        """Filter inventory based on search term"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all data from database
        all_data = self.db_manager.get_inventory()
        
        # Filter data based on search term
        filtered_data = []
        for row in all_data:
            # Search in item name (case insensitive)
            if search_term == "" or search_term in str(row[1]).lower():
                filtered_data.append(row)
        
        # Insert filtered data into treeview
        for row in filtered_data:
            self.tree.insert('', tk.END, values=row)
        
        print(f"Found {len(filtered_data)} items matching '{search_term}'")

    def retrieve_inventory(self):
        """Retrieve and display all inventory items"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get fresh data from database
        data = self.db_manager.get_inventory()
        
        # Insert data into treeview
        for row in data:
            self.tree.insert('', tk.END, values=row)
        
        print(f"Loaded {len(data)} inventory items")

    def add_new_stock(self):
        # Create dialog for adding new item
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Item")
        dialog.geometry("400x250")
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog on screen
        self.center_screen(dialog)
        
        # Input fields
        dialog.columnconfigure(1, weight=1)
        
        tk.Label(dialog, text="Item Name:", bg='white').grid(row=0, column=0, padx=10, pady=8, sticky='w')
        name_entry = tk.Entry(dialog, width=20)
        name_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Quantity:", bg='white').grid(row=1, column=0, padx=10, pady=8, sticky='w')
        qty_entry = tk.Entry(dialog, width=20)
        qty_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Capital:", bg='white').grid(row=2, column=0, padx=10, pady=8, sticky='w')
        capital_entry = tk.Entry(dialog, width=20)
        capital_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Price:", bg='white').grid(row=3, column=0, padx=10, pady=8, sticky='w')
        price_entry = tk.Entry(dialog, width=20)
        price_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Expiration Date:", bg='white').grid(row=4, column=0, padx=10, pady=8, sticky='w')
        exp_date_entry = tk.Entry(dialog, width=20)
        exp_date_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=8)
        
        def save_item():
            name = name_entry.get().strip()
            qty = qty_entry.get().strip()
            capital = capital_entry.get().strip()
            price = price_entry.get().strip()
            exp_date = exp_date_entry.get().strip()
            
            if name and qty and capital and price and exp_date:
                try:
                    self.db_manager.add_item(name, int(qty), float(capital), float(price), exp_date)
                    self.retrieve_inventory()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Quantity and Capital must be numbers, Price must be a number")
            else:
                messagebox.showerror("Error", "All fields are required")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.grid(row=5, column=0, columnspan=2, pady=15, sticky='ew')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        tk.Button(button_frame, text="Save", command=save_item, bg='#529133', fg='white', padx=20).grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg='#d32f2f', fg='white', padx=20).grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    def update_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to update")
            return
        
        item_data = self.tree.item(selected_item[0])['values']
        item_id = item_data[0]
        current_name = item_data[1]
        current_qty = item_data[2]
        current_capital = item_data[3]
        current_price = item_data[4]
        current_exp_date = item_data[5]
        
        # Create dialog for updating item
        dialog = tk.Toplevel(self.parent)
        dialog.title("Update Item")
        dialog.geometry("400x250")
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        dialog.columnconfigure(1, weight=1)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog on screen
        self.center_screen(dialog)
        
        # Input fields with current values
        tk.Label(dialog, text="Item Name:", bg='white').grid(row=0, column=0, padx=10, pady=8, sticky='w')
        name_entry = tk.Entry(dialog, width=20)
        name_entry.insert(0, current_name)
        name_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Quantity:", bg='white').grid(row=1, column=0, padx=10, pady=8, sticky='w')
        qty_entry = tk.Entry(dialog, width=20)
        qty_entry.insert(0, current_qty)
        qty_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Capital:", bg='white').grid(row=2, column=0, padx=10, pady=8, sticky='w')
        capital_entry = tk.Entry(dialog, width=20)
        capital_entry.insert(0, current_capital)
        capital_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Price:", bg='white').grid(row=3, column=0, padx=10, pady=8, sticky='w')
        price_entry = tk.Entry(dialog, width=20)
        price_entry.insert(0, current_price)
        price_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Expiration Date:", bg='white').grid(row=4, column=0, padx=10, pady=8, sticky='w')
        exp_date_entry = tk.Entry(dialog, width=20)
        exp_date_entry.insert(0, current_exp_date)
        exp_date_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=8)
        
        def update():
            name = name_entry.get().strip()
            qty = qty_entry.get().strip()
            capital = capital_entry.get().strip()
            price = price_entry.get().strip()
            exp_date = exp_date_entry.get().strip()
            
            if name and qty and capital and price and exp_date:
                try:
                    self.db_manager.update_inventory(name, int(qty), float(capital), float(price), exp_date)
                    self.retrieve_inventory()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Quantity and Capital must be numbers, Price must be a number")
            else:
                messagebox.showerror("Error", "All fields are required")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.grid(row=5, column=0, columnspan=2, pady=15, sticky='ew')
    
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        tk.Button(button_frame, text="Update", command=update, bg='#529133', fg='white', padx=20).grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg='#d32f2f', fg='white', padx=20).grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete")
            return
        
        item_data = self.tree.item(selected_item[0])['values']
        item_id = item_data[0]
        item_name = item_data[1]
        
        # Confirm deletion
        result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{item_name}'?")
        if result:
            if self.db_manager.delete_item(item_id):
                self.retrieve_inventory()
                messagebox.showinfo("Success", "Item deleted successfully")
            else:
                messagebox.showerror("Error", "Failed to delete item")