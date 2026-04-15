import customtkinter as ctk
import tkinter.ttk as ttk
from datetime import datetime
from src.utils.logger import get_recent_logs

class Logs:
    def __init__(self, parent):
        self.parent = parent
        self.create_logs()
        self.refresh_logs()
    
    def create_logs(self):
        # Main frame
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="User Interaction Logs", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Control frame
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Log type selector
        ctk.CTkLabel(control_frame, text="Log Type:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(10, 5))
        self.log_type_var = ctk.StringVar(value="user_interactions")
        log_types = ["user_interactions", "system_operations", "database_operations", "errors"]
        self.log_type_menu = ctk.CTkOptionMenu(
            control_frame, 
            variable=self.log_type_var, 
            values=log_types, 
            command=self.refresh_logs,
            font=ctk.CTkFont(size=11)
        )
        self.log_type_menu.pack(side="left", padx=(0, 20))
        
        # Refresh button
        ctk.CTkButton(
            control_frame, 
            text="Refresh", 
            command=self.refresh_logs,
            font=ctk.CTkFont(size=11)
        ).pack(side="right", padx=(0, 10))
        
        # Clear logs button
        ctk.CTkButton(
            control_frame, 
            text="Clear Logs", 
            command=self.clear_logs,
            font=ctk.CTkFont(size=11),
            fg_color="red"
        ).pack(side="right", padx=5)
        
        # Logs display frame
        logs_frame = ctk.CTkFrame(main_frame)
        logs_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Create text widget for logs
        self.logs_text = ctk.CTkTextbox(
            logs_frame, 
            font=ctk.CTkFont(family="Courier", size=10),
            wrap="word"
        )
        self.logs_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure text tags for different log levels
        self.logs_text.tag_config("INFO", foreground="#00FF00")
        self.logs_text.tag_config("ERROR", foreground="#FF0000")
        self.logs_text.tag_config("SYSTEM", foreground="#00BFFF")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame, 
            text="Ready", 
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(pady=(5, 0))
    
    def refresh_logs(self):
        """Refresh the logs display"""
        try:
            log_type = self.log_type_var.get()
            logs = get_recent_logs(log_type, 500)  # Get last 500 lines
            
            # Clear existing content
            self.logs_text.delete("1.0", "end")
            
            if not logs:
                self.logs_text.insert("end", f"No logs found for {log_type}\n")
                self.status_label.configure(text=f"No logs found for {log_type}")
                return
            
            # Add logs to display
            for log_line in logs:
                log_line = log_line.strip()
                if not log_line:
                    continue
                    
                # Determine log level and apply appropriate tag
                if "ERROR" in log_line:
                    tag = "ERROR"
                elif "SYSTEM" in log_line:
                    tag = "SYSTEM"
                else:
                    tag = "INFO"
                
                # Insert log line with appropriate formatting
                self.logs_text.insert("end", log_line + "\n", tag)
            
            # Scroll to bottom
            self.logs_text.see("end")
            
            # Update status
            self.status_label.configure(text=f"Loaded {len(logs)} log entries from {log_type}")
            
        except Exception as e:
            self.logs_text.delete("1.0", "end")
            self.logs_text.insert("end", f"Error loading logs: {str(e)}\n")
            self.status_label.configure(text=f"Error: {str(e)}")
    
    def clear_logs(self):
        """Clear the logs display"""
        self.logs_text.delete("1.0", "end")
        self.status_label.configure(text="Logs cleared")