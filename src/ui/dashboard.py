import tkinter as tk

class Dashboard:
    def __init__(self, parent):
        self.parent = parent
        self.create_dashboard()
    
    def create_dashboard(self):
        label = tk.Label(self.parent, text="Dashboard", font=("Arial", 20), bg='white')
        label.pack(pady=20)
        
        stats_label = tk.Label(self.parent, text="Statistics here", bg='white')
        stats_label.pack(pady=10)