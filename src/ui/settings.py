import customtkinter as ctk

class Settings:
    def __init__(self, parent):
        self.parent = parent
        self.setting_widget()
    
    def setting_widget(self):
        self.setting_frame = ctk.CTkFrame(self.parent)
        self.setting_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        self.setting_frame.columnconfigure(1, weight=1)

        title_label = ctk.CTkLabel(
            self.setting_frame,
            text="Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)
        

        #label
        username_label = ctk.CTkLabel(
            self.setting_frame,
            text="Username",
            font=ctk.CTkFont(size=12)
        )
        username_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)
        
        email_label = ctk.CTkLabel(
            self.setting_frame,
            text="Email",
            font=ctk.CTkFont(size=12)
        )
        email_label.grid(row=2, column=0, sticky='w', padx=10, pady=10)

        password_label = ctk.CTkLabel(
            self.setting_frame,
            text="Password",
            font=ctk.CTkFont(size=12)
        )
        password_label.grid(row=3, column=0, sticky='w', padx=10, pady=10)

        sheet_link_label = ctk.CTkLabel(
            self.setting_frame,
            text="Sheet Link",
            font=ctk.CTkFont(size=12)
        )
        sheet_link_label.grid(row=4, column=0, sticky='w', padx=10, pady=10)


        #input
        username_entry = ctk.CTkEntry(
            self.setting_frame,
            font=ctk.CTkFont(size=12),
            width=30
        )
        username_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=10)
        
        email_entry = ctk.CTkEntry(
            self.setting_frame,
            font=ctk.CTkFont(size=12),
            width=30
        )
        email_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=10)
        
        password_entry = ctk.CTkEntry(
            self.setting_frame,
            font=ctk.CTkFont(size=12),
            width=30,
            show="*"
        )
        password_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=10)
        
        sheet_link_entry = ctk.CTkEntry(
            self.setting_frame,
            font=ctk.CTkFont(size=12),
            width=30
        )
        sheet_link_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=10)

        save_button = ctk.CTkButton(
            self.setting_frame,
            text="Save",
            command=self.save_settings,
            font=ctk.CTkFont(size=10)
        )
        save_button.grid(row=5, column=1, sticky='e', padx=10, pady=10)

    def save_settings(self):
        """Save settings to file or database"""
        # TODO: Implement settings save functionality
        print("Settings saved (placeholder)")
