import tkinter as tk
import tkinter.ttk as ttk
from src.database_manager import DatabaseManager
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
        
        # Create Treeview for inventory grid
        columns = ('ID', 'Item Name', 'Quantity', 'Price', 'Created Date', 'Updated Date')
        
        self.tree = ttk.Treeview(self.inventory_frame, columns=columns, show='headings', height=15)
        
        # Define column headings and widths
        column_widths = {'ID': 50, 'Item Name': 200, 'Quantity': 100, 'Price': 100, 'Created Date': 150, 'Updated Date': 150}
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.inventory_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.inventory_frame, bg='white')
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
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
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            buttons_frame,
            text="Update Selected",
            command=self.update_item,
            bg='#2E531D',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_item,
            bg='#d32f2f',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(
            buttons_frame,
            text="Refresh",
            command=self.retrieve_inventory,
            bg='#1976d2',
            fg='white',
            font=('Arial', 10),
            padx=20,
            pady=5
        ).pack(side=tk.LEFT)

    def center_screen(self, dialog):
        """Center the dialog on the screen"""
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'{width}x{height}+{x}+{y}')

    def retrieve_inventory(self):
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
        dialog.geometry("300x200")
        dialog.configure(bg='white')
        
        # Make dialog modal
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog on screen
        self.center_screen(dialog)
        
        # Input fields
        tk.Label(dialog, text="Item Name:", bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        name_entry = tk.Entry(dialog, width=20)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Quantity:", bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')
        qty_entry = tk.Entry(dialog, width=20)
        qty_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Price:", bg='white').grid(row=2, column=0, padx=10, pady=10, sticky='w')
        price_entry = tk.Entry(dialog, width=20)
        price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def save_item():
            name = name_entry.get().strip()
            qty = qty_entry.get().strip()
            price = price_entry.get().strip()
            
            if name and qty and price:
                try:
                    self.db_manager.add_item(name, int(qty), float(price))
                    self.retrieve_inventory()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Quantity must be a number and Price must be a number")
            else:
                messagebox.showerror("Error", "All fields are required")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Save", command=save_item, bg='#529133', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg='#d32f2f', fg='white', padx=20).pack(side=tk.LEFT, padx=5)

    def update_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to update")
            return
        
        item_data = self.tree.item(selected_item[0])['values']
        item_id = item_data[0]
        current_name = item_data[1]
        current_qty = item_data[2]
        current_price = item_data[3]
        
        # Create dialog for updating item
        dialog = tk.Toplevel(self.parent)
        dialog.title("Update Item")
        dialog.geometry("300x200")
        dialog.configure(bg='white')
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog on screen
        self.center_screen(dialog)
        
        # Input fields with current values
        tk.Label(dialog, text="Item Name:", bg='white').grid(row=0, column=0, padx=10, pady=10, sticky='w')
        name_entry = tk.Entry(dialog, width=20)
        name_entry.insert(0, current_name)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Quantity:", bg='white').grid(row=1, column=0, padx=10, pady=10, sticky='w')
        qty_entry = tk.Entry(dialog, width=20)
        qty_entry.insert(0, current_qty)
        qty_entry.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Label(dialog, text="Price:", bg='white').grid(row=2, column=0, padx=10, pady=10, sticky='w')
        price_entry = tk.Entry(dialog, width=20)
        price_entry.insert(0, current_price)
        price_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def update():
            name = name_entry.get().strip()
            qty = qty_entry.get().strip()
            price = price_entry.get().strip()
            
            if name and qty and price:
                try:
                    self.db_manager.update_inventory(name, int(qty), float(price))
                    self.retrieve_inventory()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Quantity must be a number and Price must be a number")
            else:
                messagebox.showerror("Error", "All fields are required")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Update", command=update, bg='#529133', fg='white', padx=20).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg='#d32f2f', fg='white', padx=20).pack(side=tk.LEFT, padx=5)

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