import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.ui.homeview import HomeView
import customtkinter as ctk

if __name__ == '__main__':
    light_mode = ['dark',"light"]

    ctk.set_appearance_mode(light_mode[0]) 
    # ctk.set_default_color_theme("assets/my_theme.json")
    
    root = ctk.CTk()
    root.title("MedRX Inventory System")
    root.iconbitmap("assets/MedRx.ico") 

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")  # Top-left corner
    root.resizable(True, True)
    

    app = HomeView(root)
    root.mainloop()
