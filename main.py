from src.ui.homeview import HomeView
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    root.title("MedRX Inventory System")
    root.iconbitmap("assets/MedRx.ico")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")  # Top-left corner
    root.resizable(True, True)
    

    app = HomeView(root)
    root.mainloop()
