import tkinter as tk
from PIL import ImageTk, Image, ImageDraw

from src.ui.dashboard import Dashboard
from src.ui.inventory import Inventory
from src.ui.logs import Logs
from src.ui.settings import Settings

class HomeView:

    

    # Main containers below

    def header(self):
        header_frame = tk.Frame(self.root, bg='#529133', height=60)
        header_frame.pack(fill=tk.BOTH, padx=0, pady=0)
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
        
        self.logo = ImageTk.PhotoImage(rounded_image)

        self.logo_label = tk.Label(header_frame, image=self.logo, bg='#529133')
        self.logo_label.grid(row=0, column=0, padx=20, pady=15)
        
        # Title
        self.title_label = tk.Label(
            header_frame, 
            text="MedRX Inventory", 
            font=('Arial', 20, 'bold'),
            bg='#529133',
            fg='white'
        )
        self.title_label.grid(row=0, column=1, padx=20, pady=15, columnspan=2)

        # Name of user
        self.user_label = tk.Label(
            header_frame,
            text="Felino E. Doria",
            font=('Arial', 12),
            bg='#529133',
            fg='white'
        )
        self.user_label.grid(row=0, column=3, padx=20, pady=15, sticky='e')
   
    def main_container(self):
        self.main_container = tk.Frame(self.root, bg='white')
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def create_dashboard_view(self):
        dashboard = Dashboard(self.main_container)
        return dashboard

    def create_inventory_view(self):
        inventory = Inventory(self.main_container)
        return inventory

    def create_logs_view(self):
        logs = Logs(self.main_container)
        return logs

    def create_settings_view(self):
        settings = Settings(self.main_container)
        return settings

    def switch_view(self, view):
        #view = action

        for widget in self.main_container.winfo_children():
            widget.destroy()
        
        match view:
            case "dashboard":
                self.current_view = self.create_dashboard_view()
            case "Inventory":
                self.current_view = self.create_inventory_view()
            case "Logs":
                self.current_view = self.create_logs_view()
            case "Settings":
                self.current_view = self.create_settings_view()

    def sidebar(self):
        sidebar_frame = tk.Frame(self.root, bg='#2E531D', width=200)
        sidebar_frame.pack(fill=tk.Y, side=tk.LEFT)

        nav_items =[
            ("Dashboard", lambda: self.switch_view("dashboard")),
            ("Inventory", lambda: self.switch_view("Inventory")),
            ("Logs", lambda: self.switch_view("Logs")),
            ("Settings", lambda: self.switch_view("Settings")),
        ]

        for text, command in nav_items:
            btn = tk.Button(
                sidebar_frame,
                text=text,
                font=('Arial', 11),
                bg='#2E531D',
                fg='white',
                relief=tk.FLAT,
                anchor='w',
                padx=20,
                pady=15,
                command=command
            )
            btn.pack(fill=tk.X, padx=0, pady=0)
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#529133'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#2E531D'))

    
    def status_bar(self):
        pass
    

    def __init__(self, root):
        self.root = root
        self.current_view = None

        # Main frames
        self.header()
        self.sidebar()
        self.main_container()

        self.switch_view("dashboard") 
        # self.status_bar()