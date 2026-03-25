import tkinter as tk

class Settings:
    def __init__(self, parent):
        self.parent = parent
        self.setting_widget()
    
    def setting_widget(self):
        self.setting_frame = tk.Frame(self.parent, bg='white')
        self.setting_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.setting_frame.columnconfigure(1, weight=1)

        title_label = tk.Label(
            self.setting_frame,
            text="Settings",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2E531D'
        )
        title_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)
        

        #label
        username_label = tk.Label(
            self.setting_frame,
            text="Username",
            font=('Arial', 12),
            bg='white',
            fg='#2E531D'
        )
        username_label.grid(row=1, column=0, sticky='w', padx=10, pady=10)
        
        email_label = tk.Label(
            self.setting_frame,
            text="Email",
            font=('Arial', 12),
            bg='white',
            fg='#2E531D'
        )
        email_label.grid(row=2, column=0, sticky='w', padx=10, pady=10)

        password_label = tk.Label(
            self.setting_frame,
            text="Password",
            font=('Arial', 12),
            bg='white',
            fg='#2E531D'
        )
        password_label.grid(row=3, column=0, sticky='w', padx=10, pady=10)

        sheet_link_label = tk.Label(
            self.setting_frame,
            text="Sheet Link",
            font=('Arial', 12),
            bg='white',
            fg='#2E531D'
        )
        sheet_link_label.grid(row=4, column=0, sticky='w', padx=10, pady=10)

        sheet_id_label = tk.Label(
            self.setting_frame,
            text="Sheet ID",
            font=('Arial', 12),
            bg='white',
            fg='#2E531D'
        )
        sheet_id_label.grid(row=5, column=0, sticky='w', padx=10, pady=10)

        #input
        username_entry = tk.Entry(
            self.setting_frame,
            font=('Arial', 12),
            width=30
        )
        username_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=10)
        
        email_entry = tk.Entry(
            self.setting_frame,
            font=('Arial', 12),
            width=30
        )
        email_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=10)
        
        password_entry = tk.Entry(
            self.setting_frame,
            font=('Arial', 12),
            width=30
        )
        password_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=10)
        
        sheet_link_entry = tk.Entry(
            self.setting_frame,
            font=('Arial', 12),
            width=30
        )
        sheet_link_entry.grid(row=4, column=1, sticky='ew', padx=10, pady=10)
        
        sheet_id_entry = tk.Entry(
            self.setting_frame,
            font=('Arial', 12),
            width=30
        )
        sheet_id_entry.grid(row=5, column=1, sticky='ew', padx=10, pady=10)

