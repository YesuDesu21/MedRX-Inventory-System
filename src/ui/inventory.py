import customtkinter as ctk
import tkinter.ttk as ttk
import tkinter as tk
from src.utils.db_inventory_manager import DBInventoryManager
from tkinter import messagebox

class Inventory:
    def __init__(self, parent):
        self.parent = parent
        self.db_manager = DBInventoryManager()
        self.create_widgets()
        self.retrieve_inventory()

    def create_widgets(self):
        # Main frame for inventory
        self.inventory_frame = ctk.CTkFrame(self.parent)
        self.inventory_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            self.inventory_frame,
            text="Inventory Management",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create container for treeview and scrollbar
        tree_container = ctk.CTkFrame(self.inventory_frame)
        tree_container.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        
        # Create Treeview for inventory grid inside container
        columns = ('ID', 'Product Name', 'Product Type', 'Quantity', 'Unit Cost', 'Price', 'Medicine Type', 'Expiration Date', 'Created Date', 'Updated Date')
        
        self.tree = ttk.Treeview(tree_container, columns=columns, show='headings', height=15)
        
        # Configure font for treeview
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 11))
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))
        style.configure("Treeview", rowheight=25)  # Increase row height for better readability
        
        # Define column headings and widths
        column_widths = {
            'ID': 50, 
            'Product Name': 150, 
            'Product Type': 100, 
            'Quantity': 80, 
            'Unit Cost': 80, 
            'Price': 80, 
            'Medicine Type': 100, 
            'Expiration Date': 120, 
            'Created Date': 120, 
            'Updated Date': 120
        }
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100), anchor='center')
        
        # Add scrollbar inside container
        scrollbar = ttk.Scrollbar(tree_container, orient=ctk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview and scrollbar in container
        self.tree.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.inventory_frame)
        buttons_frame.pack(side=ctk.RIGHT, fill=ctk.Y, padx=(10, 0))
        
        # Search bar
        search_label = ctk.CTkLabel(
            buttons_frame,
            text="Search:",
            font=ctk.CTkFont(size=10, weight="bold")
        )
        search_label.pack(pady=(0, 5))
        
        self.search_entry = ctk.CTkEntry(
            buttons_frame,
            font=ctk.CTkFont(size=10),
            width=20
        )
        self.search_entry.pack(fill=ctk.X, pady=(0, 15))
        self.search_entry.bind('<KeyRelease>', self.filter_inventory)
        
        # Sort by dropdown
        sort_frame = ctk.CTkFrame(buttons_frame)
        sort_frame.pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkLabel(sort_frame, text="Sort by:", font=ctk.CTkFont(size=11)).pack(side='left', padx=(0, 5))
        self.sort_by_options = ["ID", "Product Name", "Product Type", "Quantity", "Unit Cost", "Price", "Medicine Type", "Expiration Date", "Created Date", "Updated Date"]
        self.sort_by_var = ctk.StringVar(value=self.sort_by_options[0])
        self.sort_by_option_menu = ctk.CTkOptionMenu(sort_frame, variable=self.sort_by_var, values=self.sort_by_options, font=ctk.CTkFont(size=10), command=self.filter_inventory)
        self.sort_by_option_menu.pack(side='left', padx=(10, 0))
        
        # Action buttons
        ctk.CTkButton(
            buttons_frame,
            text="Add New Item",
            command=self.add_new_stock,
            font=ctk.CTkFont(size=11)
        ).pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="Update Selected",
            command=self.update_item,
            font=ctk.CTkFont(size=11)
        ).pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_item,
            font=ctk.CTkFont(size=11),
            fg_color="red"
        ).pack(fill=ctk.X, pady=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="Refresh",
            command=self.retrieve_inventory,
            font=ctk.CTkFont(size=11)
        ).pack(fill=ctk.X)

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

    def filter_inventory(self, event=None):
        """Filter and sort inventory based on search term and sort option"""
        search_term = self.search_entry.get().strip().lower()
        sort_by = self.sort_by_var.get()
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all data from database
        all_data = self.db_manager.get_inventory()
        
        # Filter data based on search term
        filtered_data = []
        for row in all_data:
            # Search in product name (case insensitive)
            if search_term == "" or search_term in str(row[1]).lower():
                filtered_data.append(row)
        
        # Sort data based on selected option
        if sort_by == "ID":
            filtered_data.sort(key=lambda x: x[0], reverse=False)
        elif sort_by == "Product Name":
            filtered_data.sort(key=lambda x: str(x[1]), reverse=False)
        elif sort_by == "Product Type":
            filtered_data.sort(key=lambda x: str(x[2]), reverse=False)
        elif sort_by == "Quantity":
            filtered_data.sort(key=lambda x: x[3] if x[3] is not None else 0, reverse=False)
        elif sort_by == "Unit Cost":
            filtered_data.sort(key=lambda x: x[4] if x[4] is not None else 0, reverse=False)
        elif sort_by == "Price":
            filtered_data.sort(key=lambda x: x[5] if x[5] is not None else 0, reverse=False)
        elif sort_by == "Medicine Type":
            filtered_data.sort(key=lambda x: str(x[6]), reverse=False)
        elif sort_by == "Expiration Date":
            filtered_data.sort(key=lambda x: x[7] if x[7] is not None else "", reverse=False)
        elif sort_by == "Created Date":
            filtered_data.sort(key=lambda x: x[8] if x[8] is not None else "", reverse=False)
        elif sort_by == "Updated Date":
            filtered_data.sort(key=lambda x: x[9] if x[9] is not None else "", reverse=False)
        
        # Insert filtered and sorted data into treeview
        for row in filtered_data:
            self.tree.insert('', ctk.END, values=row)
        
        print(f"Found {len(filtered_data)} items matching '{search_term}', sorted by '{sort_by}'")

    # show data to treeview
    def retrieve_inventory(self):
        """Retrieve and display all inventory items"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get fresh data from database
        data = self.db_manager.get_inventory()
        
        # Insert data into treeview
        for row in data:
            self.tree.insert('', ctk.END, values=row)
        
        print(f"Loaded {len(data)} inventory items")

    def add_new_stock(self):
        # Create dialog for adding new item
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Item")
        dialog.geometry("500x400")
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        
        # Make dialog modal
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog on screen
        self.center_screen(dialog)
        
        # Input fields
        dialog.columnconfigure(1, weight=1)
        
        # Product Name field
        label_font = ('Arial', 11)
        entry_font = ('Arial', 10)
        
        tk.Label(dialog, text="Product Name:", bg='white', font=label_font).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        name_entry = tk.Entry(dialog, width=20, font=entry_font)
        name_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=8)
        
        # Product Type field
        tk.Label(dialog, text="Product Type:", bg='white', font=label_font).grid(row=1, column=0, padx=10, pady=8, sticky='w')
        product_type_var = tk.StringVar(value="medicine")
        product_type_frame = tk.Frame(dialog, bg='white')
        product_type_frame.grid(row=1, column=1, sticky='ew', padx=10, pady=8)
        
        product_type_menu = tk.OptionMenu(product_type_frame, product_type_var, "medicine", "supplies")
        product_type_menu.config(font=entry_font)
        product_type_menu.pack(side=tk.LEFT)
        product_type_menu.bind('<Configure>', lambda e: self.update_medicine_type_options(medicine_type_frame, product_type_var.get()))
        
        # Medicine Type field (initially for medicine)
        self.medicine_type_var = tk.StringVar(value="branded")
        medicine_type_frame = tk.Frame(dialog, bg='white')
        medicine_type_frame.grid(row=2, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Medicine Type:", bg='white', font=label_font).grid(row=2, column=0, padx=10, pady=8, sticky='w')
        self.medicine_type_menu = tk.OptionMenu(medicine_type_frame, self.medicine_type_var, "branded", "unbranded")
        self.medicine_type_menu.config(font=entry_font)
        self.medicine_type_menu.pack(side=tk.LEFT)
        
        # Quantity field
        tk.Label(dialog, text="Quantity:", bg='white', font=label_font).grid(row=3, column=0, padx=10, pady=8, sticky='w')
        qty_entry = tk.Entry(dialog, width=20, font=entry_font)
        qty_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=8)
        
        # Unit Cost field
        tk.Label(dialog, text="Unit Cost:", bg='white', font=label_font).grid(row=4, column=0, padx=10, pady=8, sticky='w')
        unit_cost_entry = tk.Entry(dialog, width=20, font=entry_font)
        unit_cost_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=8)
        
        # Price field
        tk.Label(dialog, text="Price:", bg='white', font=label_font).grid(row=5, column=0, padx=10, pady=8, sticky='w')
        price_entry = tk.Entry(dialog, width=20, font=entry_font)
        price_entry.grid(row=5, column=1, sticky='ew', padx=10, pady=8)
        
        # Expiration Date field
        tk.Label(dialog, text="Expiration Date:", bg='white', font=label_font).grid(row=6, column=0, padx=10, pady=8, sticky='w')
        exp_date_entry = tk.Entry(dialog, width=20, font=entry_font)
        exp_date_entry.grid(row=6, column=1, sticky='ew', padx=10, pady=8)
        
        def save_item():
            name = name_entry.get().strip()
            product_type = product_type_var.get()
            medicine_type = self.medicine_type_var.get() if product_type.lower() == 'medicine' else 'N/A'
            qty = qty_entry.get().strip()
            unit_cost = unit_cost_entry.get().strip()
            price = price_entry.get().strip()
            exp_date = exp_date_entry.get().strip()
            
            if name and qty and unit_cost and price and exp_date:
                try:
                    self.db_manager.add_product(name, product_type, int(qty), float(unit_cost), float(price), medicine_type, exp_date)
                    self.retrieve_inventory()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Quantity and Unit Cost must be numbers, Price must be a number")
            else:
                messagebox.showerror("Error", "All fields are required")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.grid(row=7, column=0, columnspan=2, pady=15, sticky='ew')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        tk.Button(button_frame, text="Save", command=save_item, bg='#529133', fg='white', padx=20, font=entry_font).grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg='#d32f2f', fg='white', padx=20, font=entry_font).grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    def update_medicine_type_options(self, frame, product_type):
        """Update medicine type options based on product type"""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        if product_type.lower() == 'medicine':
            self.medicine_type_var = tk.StringVar(value="branded")
            medicine_menu = tk.OptionMenu(frame, self.medicine_type_var, "branded", "unbranded")
            medicine_menu.pack(side=tk.LEFT)
        else:
            # For non-medicine products, show N/A label
            na_label = tk.Label(frame, text="N/A", bg='white', fg='#666')
            na_label.pack(side=tk.LEFT)

    def update_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to update")
            return
        
        item_data = self.tree.item(selected_item[0])['values']
        item_id = item_data[0]
        current_name = item_data[1]
        current_product_type = item_data[2]
        current_qty = item_data[3]
        current_unit_cost = item_data[4]
        current_price = item_data[5]
        current_medicine_type = item_data[6]
        current_exp_date = item_data[7]
        
        # Create dialog for updating item
        dialog = tk.Toplevel(self.parent)
        dialog.title("Update Item")
        dialog.geometry("500x350")
        dialog.configure(bg='white')
        dialog.resizable(False, False)
        dialog.columnconfigure(1, weight=1)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog on screen
        self.center_screen(dialog)
        
        # Input fields with current values
        label_font = ('Arial', 11)
        entry_font = ('Arial', 10)
        
        tk.Label(dialog, text="Product Name:", bg='white', font=label_font).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        name_entry = tk.Entry(dialog, width=20, font=entry_font)
        name_entry.insert(0, current_name)
        name_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=8)
        
        # Product Type field
        tk.Label(dialog, text="Product Type:", bg='white', font=label_font).grid(row=1, column=0, padx=10, pady=8, sticky='w')
        product_type_var = tk.StringVar(value=current_product_type if current_product_type in ['medicine', 'supplies'] else 'medicine')
        product_type_frame = tk.Frame(dialog, bg='white')
        product_type_frame.grid(row=1, column=1, sticky='ew', padx=10, pady=8)
        
        product_type_menu = tk.OptionMenu(product_type_frame, product_type_var, "medicine", "supplies")
        product_type_menu.config(font=entry_font)
        product_type_menu.pack(side=tk.LEFT)
        product_type_menu.bind('<Configure>', lambda e: self.update_medicine_type_options(medicine_type_frame, product_type_var.get()))
        
        # Medicine Type field
        medicine_type_frame = tk.Frame(dialog, bg='white')
        medicine_type_frame.grid(row=2, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Medicine Type:", bg='white', font=label_font).grid(row=2, column=0, padx=10, pady=8, sticky='w')
        
        if current_product_type.lower() == 'medicine':
            self.medicine_type_var = tk.StringVar(value=current_medicine_type if current_medicine_type != 'N/A' else 'branded')
            medicine_type_menu = tk.OptionMenu(medicine_type_frame, self.medicine_type_var, "branded", "unbranded")
            medicine_type_menu.config(font=entry_font)
            medicine_type_menu.pack(side=tk.LEFT)
        else:
            na_label = tk.Label(medicine_type_frame, text="N/A", bg='white', fg='#666', font=entry_font)
            na_label.pack(side=tk.LEFT)
        
        tk.Label(dialog, text="Quantity:", bg='white', font=label_font).grid(row=3, column=0, padx=10, pady=8, sticky='w')
        qty_entry = tk.Entry(dialog, width=20, font=entry_font)
        qty_entry.insert(0, current_qty)
        qty_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Unit Cost:", bg='white', font=label_font).grid(row=4, column=0, padx=10, pady=8, sticky='w')
        unit_cost_entry = tk.Entry(dialog, width=20, font=entry_font)
        unit_cost_entry.insert(0, current_unit_cost)
        unit_cost_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Price:", bg='white', font=label_font).grid(row=5, column=0, padx=10, pady=8, sticky='w')
        price_entry = tk.Entry(dialog, width=20, font=entry_font)
        price_entry.insert(0, current_price)
        price_entry.grid(row=5, column=1, sticky='ew', padx=10, pady=8)
        
        tk.Label(dialog, text="Expiration Date:", bg='white', font=label_font).grid(row=6, column=0, padx=10, pady=8, sticky='w')
        exp_date_entry = tk.Entry(dialog, width=20, font=entry_font)
        exp_date_entry.insert(0, current_exp_date)
        exp_date_entry.grid(row=6, column=1, sticky='ew', padx=10, pady=8)
        
        def update():
            name = name_entry.get().strip()
            product_type = product_type_var.get()
            medicine_type = self.medicine_type_var.get() if product_type.lower() == 'medicine' else 'N/A'
            qty = qty_entry.get().strip()
            unit_cost = unit_cost_entry.get().strip()
            price = price_entry.get().strip()
            exp_date = exp_date_entry.get().strip()
            
            if name and qty and unit_cost and price and exp_date:
                try:
                    self.db_manager.update_inventory(name, int(qty), float(unit_cost), float(price), exp_date, product_type, medicine_type)
                    self.retrieve_inventory()
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Quantity and Unit Cost must be numbers, Price must be a number")
            else:
                messagebox.showerror("Error", "All fields are required")
        
        # Initialize medicine type options based on current product type
        self.update_medicine_type_options(medicine_type_frame, current_product_type)
        
        # Buttons
        button_frame = tk.Frame(dialog, bg='white')
        button_frame.grid(row=7, column=0, columnspan=2, pady=15, sticky='ew')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        tk.Button(button_frame, text="Update", command=update, bg='#529133', fg='white', padx=20, font=entry_font).grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg='#d32f2f', fg='white', padx=20, font=entry_font).grid(row=0, column=1, sticky='ew', padx=5, pady=5)

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
