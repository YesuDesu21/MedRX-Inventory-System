import customtkinter as ctk
from PIL import ImageTk, Image, ImageDraw

from src.ui.dashboard import Dashboard
from src.ui.inventory import Inventory
from src.ui.transaction import Transaction
from src.ui.logs import Logs
from src.ui.settings import Settings
from src.utils.logger import log_user_action, log_system_event

class HomeView:

    def header(self):
        header_frame = ctk.CTkFrame(self.root, height=60, corner_radius=0)
        header_frame.pack(fill=ctk.BOTH, padx=0, pady=0)
        header_frame.pack_propagate(False)

        #Allows the title to be centered and the name to be at the right side
        header_frame.grid_columnconfigure(2, weight=1)

        original_image = Image.open("assets/MedRX_logo.png")
        resized_image = original_image.resize((50, 50))
        
        # Create rounded corners
        size = 50
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (size, size)], radius=80, fill=255)
        
        # Apply the mask to create rounded image
        rounded_image = Image.new('RGBA', (size, size))
        rounded_image.paste(resized_image, (0, 0))
        rounded_image.putalpha(mask)
        
        self.logo = ctk.CTkImage(rounded_image, size=(50, 50))

        self.logo_label = ctk.CTkLabel(header_frame, image=self.logo, text="")
        self.logo_label.grid(row=0, column=0, padx=20, pady=15)
        
        # Title
        self.title_label = ctk.CTkLabel(
            header_frame, 
            text="MedRX Inventory", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=1, padx=20, pady=15, columnspan=2)

        # Name of user
        self.user_label = ctk.CTkLabel(
            header_frame,
            text="Felino E. Doria",
            font=ctk.CTkFont(size=16)
        )
        self.user_label.grid(row=0, column=3, padx=20, pady=15, sticky='e')
   
    def main_container(self):
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

    def create_dashboard_view(self):
        dashboard = Dashboard(self.main_container)
        return dashboard

    def create_inventory_view(self):
        inventory = Inventory(self.main_container)
        return inventory

    def create_logs_view(self):
        logs = Logs(self.main_container)
        return logs

    def create_transactions_view(self):
        transaction = Transaction(self.main_container)
        return transaction

    def create_settings_view(self):
        settings = Settings(self.main_container)
        return settings

    def switch_view(self, view):
        #view = action
        
        # Log navigation action
        if view != "Logout":
            log_user_action(f"Navigated to {view}", "Navigation")

        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        match view:
            case "dashboard":
                self.current_view = self.create_dashboard_view()
            case "Inventory":
                self.current_view = self.create_inventory_view()
            case 'Transactions':
                self.current_view = self.create_transactions_view()
            case "Logs":
                self.current_view = self.create_logs_view()
            case "Settings":
                self.current_view = self.create_settings_view()
            case "Logout":
                log_user_action("User logged out", "Navigation")
                if self.on_logout:
                    self.on_logout()

    def sidebar(self):
        sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        sidebar_frame.pack(fill=ctk.Y, side=ctk.LEFT)
        sidebar_frame.pack_propagate(False)

        nav_items =[
            ("Dashboard", lambda: self.switch_view("dashboard")),
            ("Inventory", lambda: self.switch_view("Inventory")),
            ("Transactions", lambda: self.switch_view("Transactions")),
            ("Logs", lambda: self.switch_view("Logs")),
            ("Settings", lambda: self.switch_view("Settings")),
            ("Logout", lambda: self.switch_view("Logout"))
        ]

        for text, command in nav_items:
            btn = ctk.CTkButton(
                sidebar_frame,
                text=text,
                font=ctk.CTkFont(size=14),
                anchor='w',
                height=45,
                command=command
            )
            btn.pack(fill=ctk.X, padx=10, pady=5)

    
    def status_bar(self):
        pass
    

    def __init__(self, root, on_logout=None):
        self.root = root
        self.current_view = None
        self.on_logout = on_logout

        # Log application startup
        log_system_event("MedRX Inventory System started")

        # Main frames
        self.header()
        self.sidebar()
        self.main_container()

        self.switch_view("dashboard") 
        # self.status_bar()