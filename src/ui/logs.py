import customtkinter as ctk

class Logs:
    def __init__(self, parent):
        self.parent = parent
        self.create_logs()
    
    def create_logs(self):
        # Create logs content
        label = ctk.CTkLabel(self.parent, text="Logs", font=ctk.CTkFont(size=16, weight="bold"))
        label.pack(pady=20)