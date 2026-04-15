import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.homeview import HomeView
from src.ui.login import Login
import customtkinter as ctk

class MedRXApp:
    def __init__(self):
        self.root = None
        self.login = None
        self.home_view = None
        self.current_user = None
        
    def setup_main_window(self):
        """Setup the main application window"""
        light_mode = ['dark',"light"]
        ctk.set_appearance_mode(light_mode[0]) 
        # ctk.set_default_color_theme("assets/my_theme.json")
        
        self.root = ctk.CTk()
        self.root.title("MedRX Inventory System")
        self.root.iconbitmap("assets/MedRx.ico") 
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")  # Top-left corner
        self.root.resizable(True, True)
    
    def on_login_success(self, username):
        """Called when login is successful"""
        self.current_user = username
        
        # Clear login screen
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Reset window to full screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)
        
        # Create main application with logout callback
        self.home_view = HomeView(self.root, on_logout=self.on_logout)
        
        # Update user label in header if it exists
        if hasattr(self.home_view, 'user_label'):
            self.home_view.user_label.configure(text=username)
    
    def on_logout(self):
        """Called when user clicks logout"""
        self.current_user = None
        
        # Clear main application
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Show login screen again
        self.login = Login(self.root, self.on_login_success)
    
    def run(self):
        """Start the application"""
        self.setup_main_window()
        
        # Show login screen first
        self.login = Login(self.root, self.on_login_success)
        
        # Start the main loop
        self.root.mainloop()

if __name__ == '__main__':
    app = MedRXApp()
    app.run()
