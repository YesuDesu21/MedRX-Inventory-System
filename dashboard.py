import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import random

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create main frames
        self.create_header()
        self.create_sidebar()
        self.create_status_bar()  # Move this before create_main_content
        self.create_main_content()
        
        # Initialize data
        self.update_dashboard_data()
    
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            header_frame, 
            text="Dashboard", 
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Date and time
        self.datetime_label = tk.Label(
            header_frame,
            text="",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='white'
        )
        self.datetime_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        self.update_datetime()
    
    def create_sidebar(self):
        """Create the sidebar navigation"""
        sidebar_frame = tk.Frame(self.root, bg='#34495e', width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        sidebar_frame.pack_propagate(False)
        
        # Navigation buttons
        nav_items = [
            ("📊 Overview", self.show_overview),
            ("📦 Inventory", self.show_inventory),
            ("👥 Users", self.show_users),
            ("📈 Reports", self.show_reports),
            ("⚙️ Settings", self.show_settings)
        ]
        
        for text, command in nav_items:
            btn = tk.Button(
                sidebar_frame,
                text=text,
                font=('Arial', 11),
                bg='#34495e',
                fg='white',
                relief=tk.FLAT,
                anchor='w',
                padx=20,
                pady=15,
                command=command
            )
            btn.pack(fill=tk.X, padx=0, pady=0)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#2c3e50'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#34495e'))
    
    def create_main_content(self):
        """Create the main content area"""
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Show overview by default
        self.show_overview()
    
    def create_status_bar(self):
        """Create the status bar"""
        status_frame = tk.Frame(self.root, bg='#2c3e50', height=30)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='white'
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def clear_main_content(self):
        """Clear all widgets from main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_overview(self):
        """Show overview page with statistics"""
        self.clear_main_content()
        self.status_label.config(text="Overview")
        
        # Title
        title = tk.Label(
            self.main_frame,
            text="Overview",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0'
        )
        title.pack(pady=20)
        
        # Statistics cards frame
        cards_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create statistics cards
        stats = [
            ("Total Products", "1,234", "#3498db"),
            ("Low Stock Items", "23", "#e74c3c"),
            ("New Orders", "45", "#2ecc71"),
            ("Revenue", "$12,345", "#f39c12")
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = tk.Frame(cards_frame, bg='white', relief=tk.RAISED, bd=1)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
            
            # Configure grid weights
            cards_frame.grid_columnconfigure(i%2, weight=1)
            cards_frame.grid_rowconfigure(i//2, weight=1)
            
            # Card content
            title_label = tk.Label(
                card,
                text=title,
                font=('Arial', 12),
                bg='white',
                fg='gray'
            )
            title_label.pack(pady=(20, 5))
            
            value_label = tk.Label(
                card,
                text=value,
                font=('Arial', 24, 'bold'),
                bg='white',
                fg=color
            )
            value_label.pack(pady=(0, 20))
    
    def show_inventory(self):
        """Show inventory management page"""
        self.clear_main_content()
        self.status_label.config(text="Inventory Management")
        
        # Title
        title = tk.Label(
            self.main_frame,
            text="Inventory Management",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0'
        )
        title.pack(pady=20)
        
        # Create treeview for inventory
        tree_frame = tk.Frame(self.main_frame, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Treeview
        columns = ('ID', 'Product Name', 'Category', 'Stock', 'Price', 'Status')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        # Add sample data
        sample_data = [
            ('001', 'Paracetamol', 'Medicine', '150', '$5.99', 'In Stock'),
            ('002', 'Bandages', 'Medical Supplies', '45', '$12.99', 'In Stock'),
            ('003', 'Thermometer', 'Equipment', '8', '$25.99', 'Low Stock'),
            ('004', 'Face Masks', 'Medical Supplies', '5', '$2.99', 'Low Stock'),
            ('005', 'Vitamins', 'Supplements', '200', '$15.99', 'In Stock'),
        ]
        
        for item in sample_data:
            tree.insert('', tk.END, values=item)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        button_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Add Item",
            bg='#2ecc71',
            fg='white',
            padx=20,
            pady=5,
            command=lambda: messagebox.showinfo("Info", "Add Item clicked")
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Edit Item",
            bg='#3498db',
            fg='white',
            padx=20,
            pady=5,
            command=lambda: messagebox.showinfo("Info", "Edit Item clicked")
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Delete Item",
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=5,
            command=lambda: messagebox.showinfo("Info", "Delete Item clicked")
        ).pack(side=tk.LEFT, padx=5)
    
    def show_users(self):
        """Show users management page"""
        self.clear_main_content()
        self.status_label.config(text="User Management")
        
        # Title
        title = tk.Label(
            self.main_frame,
            text="User Management",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0'
        )
        title.pack(pady=20)
        
        # User list frame
        user_frame = tk.Frame(self.main_frame, bg='white', relief=tk.RAISED, bd=1)
        user_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sample users
        users = [
            "John Doe - Administrator",
            "Jane Smith - Manager",
            "Bob Johnson - Staff",
            "Alice Brown - Staff",
            "Charlie Wilson - Manager"
        ]
        
        for user in users:
            user_label = tk.Label(
                user_frame,
                text=user,
                font=('Arial', 11),
                bg='white',
                anchor='w'
            )
            user_label.pack(fill=tk.X, padx=20, pady=5)
    
    def show_reports(self):
        """Show reports page"""
        self.clear_main_content()
        self.status_label.config(text="Reports")
        
        # Title
        title = tk.Label(
            self.main_frame,
            text="Reports",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0'
        )
        title.pack(pady=20)
        
        # Report options
        reports = [
            "Sales Report",
            "Inventory Report",
            "User Activity Report",
            "Financial Report"
        ]
        
        for report in reports:
            btn = tk.Button(
                self.main_frame,
                text=report,
                font=('Arial', 11),
                bg='white',
                relief=tk.RAISED,
                bd=1,
                anchor='w',
                padx=20,
                pady=10,
                command=lambda r=report: messagebox.showinfo("Report", f"Generating {r}...")
            )
            btn.pack(fill=tk.X, padx=20, pady=5)
    
    def show_settings(self):
        """Show settings page"""
        self.clear_main_content()
        self.status_label.config(text="Settings")
        
        # Title
        title = tk.Label(
            self.main_frame,
            text="Settings",
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0'
        )
        title.pack(pady=20)
        
        # Settings frame
        settings_frame = tk.Frame(self.main_frame, bg='white', relief=tk.RAISED, bd=1)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sample settings
        settings = [
            ("Theme", "Light"),
            ("Language", "English"),
            ("Notifications", "Enabled"),
            ("Auto-save", "Enabled")
        ]
        
        for setting, value in settings:
            frame = tk.Frame(settings_frame, bg='white')
            frame.pack(fill=tk.X, padx=20, pady=10)
            
            tk.Label(
                frame,
                text=setting,
                font=('Arial', 11),
                bg='white',
                width=15,
                anchor='w'
            ).pack(side=tk.LEFT)
            
            tk.Label(
                frame,
                text=value,
                font=('Arial', 11),
                bg='white',
                fg='gray'
            ).pack(side=tk.LEFT)
    
    def update_datetime(self):
        """Update date and time display"""
        now = datetime.datetime.now()
        datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
        self.datetime_label.config(text=datetime_str)
        self.root.after(1000, self.update_datetime)
    
    def update_dashboard_data(self):
        """Update dashboard data periodically"""
        # This would typically fetch data from a database or API
        # For demo purposes, we'll just show a status update
        self.root.after(30000, self.update_dashboard_data)  # Update every 30 seconds

def main():
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
