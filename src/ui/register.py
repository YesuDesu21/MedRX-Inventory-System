import customtkinter as ctk
from PIL import ImageTk, Image, ImageDraw
import hashlib
import re
from src.utils.logger import log_user_action, log_system_event, log_database_operation, log_error
from src.utils.database_connector import create_connection, create_cursor

class Register:
    def __init__(self, root, on_register_success, on_back_to_login):
        self.root = root
        self.on_register_success = on_register_success
        self.on_back_to_login = on_back_to_login
        
        self.create_register_ui()
        log_system_event("Registration screen initialized")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password_strength(self, password):
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'\d', password):
            return False, "Password must contain at least one digit"
        
        return True, "Password is strong"
    
    def check_username_exists(self, username):
        """Check if username already exists in database"""
        try:
            conn = create_connection()
            if not conn:
                return True  # Assume exists if can't connect
            
            cursor = create_cursor(conn)
            cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
        except Exception as e:
            log_system_event(f"Error checking username existence: {e}")
            return True  # Assume exists on error
    
    def create_user_in_database(self, username, password, email):
        """Create new user in database"""
        try:
            conn = create_connection()
            if not conn:
                return False, "Database connection failed"
            
            cursor = create_cursor(conn)
            hashed_password = self.hash_password(password)
            
            cursor.execute("""
                INSERT INTO users (username, password, email)
                VALUES (?, ?, ?)
            """, (username, hashed_password, email))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            log_database_operation(f"Created user {username}", "users", f"User ID: {user_id}")
            return True, "User created successfully"
            
        except Exception as e:
            log_error(f"Error creating user: {e}", "Register")
            return False, f"Error creating user: {e}"
    
    def create_register_ui(self):
        """Create the registration interface"""
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set window properties for registration - full screen
        self.root.title("MedRX Inventory System - Register")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)
        
        # Main registration container - full screen with two columns
        self.register_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.register_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Logo and title section
        self.create_header_section()
        
        # Registration form section
        self.create_register_form()
        
        # Status message label
        self.status_label = ctk.CTkLabel(
            self.register_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#F44336"
        )
        self.status_label.pack(pady=(10, 0))
    
    def create_header_section(self):
        """Create logo and title section"""
        # Logo container
        logo_frame = ctk.CTkFrame(self.register_frame, fg_color="transparent")
        logo_frame.pack(pady=(30, 20))
        
        try:
            # Load and process logo
            original_image = Image.open("assets/MedRX_logo.png")
            size = 80
            resized_image = original_image.resize((size, size))
            
            # Create rounded corners
            mask = Image.new('L', (size, size), 0)
            from PIL import ImageDraw
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), (size, size)], radius=60, fill=255)
            
            # Apply the mask
            rounded_image = Image.new('RGBA', (size, size))
            rounded_image.paste(resized_image, (0, 0))
            rounded_image.putalpha(mask)
            
            self.logo = ctk.CTkImage(rounded_image, size=(size, size))
            logo_label = ctk.CTkLabel(logo_frame, image=self.logo, text="")
            logo_label.pack()
        except Exception as e:
            # Fallback if logo not found
            log_system_event(f"Logo loading failed: {e}")
            pass
        
        # Title
        title_label = ctk.CTkLabel(
            self.register_frame,
            text="Create Account",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self.register_frame,
            text="Join MedRX Inventory System",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        subtitle_label.pack(pady=(0, 20))
    
    def create_register_form(self):
        """Create the registration form fields in two columns"""
        # Create two column container
        columns_frame = ctk.CTkFrame(self.register_frame, fg_color="transparent")
        columns_frame.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Configure grid weights
        columns_frame.grid_columnconfigure(0, weight=1)
        columns_frame.grid_columnconfigure(1, weight=1)
        
        # LEFT COLUMN - Full Name, Username, Email, Password
        left_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # Full Name field
        full_name_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        full_name_frame.pack(fill="x", pady=8)
        
        full_name_label = ctk.CTkLabel(
            full_name_frame,
            text="Full Name:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        full_name_label.pack(fill="x", pady=(0, 5))
        
        self.full_name_entry = ctk.CTkEntry(
            full_name_frame,
            placeholder_text="Enter your full name",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.full_name_entry.pack(fill="x")
        self.full_name_entry.bind("<Return>", lambda e: self.username_entry.focus())
        
        # Username field
        username_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        username_frame.pack(fill="x", pady=8)
        
        username_label = ctk.CTkLabel(
            username_frame,
            text="Username:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        username_label.pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            username_frame,
            placeholder_text="Choose a username",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(fill="x")
        self.username_entry.bind("<Return>", lambda e: self.email_entry.focus())
        
        # Email field
        email_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        email_frame.pack(fill="x", pady=8)
        
        email_label = ctk.CTkLabel(
            email_frame,
            text="Email:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        email_label.pack(fill="x", pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(
            email_frame,
            placeholder_text="Enter your email address",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.pack(fill="x")
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Password field (also in left column as requested)
        password_frame = ctk.CTkFrame(left_column, fg_color="transparent")
        password_frame.pack(fill="x", pady=8)
        
        password_label = ctk.CTkLabel(
            password_frame,
            text="Password:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Create a strong password",
            show="•",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(fill="x")
        self.password_entry.bind("<Return>", lambda e: self.confirm_password_entry.focus())
        
        # RIGHT COLUMN - Confirm Password, Requirements, Button, Back link
        right_column = ctk.CTkFrame(columns_frame, fg_color="transparent")
        right_column.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        
        # Confirm Password field
        confirm_password_frame = ctk.CTkFrame(right_column, fg_color="transparent")
        confirm_password_frame.pack(fill="x", pady=8)
        
        confirm_password_label = ctk.CTkLabel(
            confirm_password_frame,
            text="Confirm Password:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        confirm_password_label.pack(fill="x", pady=(0, 5))
        
        self.confirm_password_entry = ctk.CTkEntry(
            confirm_password_frame,
            placeholder_text="Confirm your password",
            show="•",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.confirm_password_entry.pack(fill="x")
        self.confirm_password_entry.bind("<Return>", lambda e: self.register())
        
        # Password requirements info
        requirements_frame = ctk.CTkFrame(right_column, fg_color="#F5F5F5")
        requirements_frame.pack(fill="x", pady=(20, 15))
        
        requirements_text = """Password Requirements:
• At least 8 characters long
• Contains uppercase letter
• Contains lowercase letter
• Contains at least one digit"""
        
        requirements_label = ctk.CTkLabel(
            requirements_frame,
            text=requirements_text,
            font=ctk.CTkFont(size=11),
            text_color="#666666",
            justify="left"
        )
        requirements_label.pack(pady=10, padx=10, anchor="w")
        
        # Register button
        self.register_button = ctk.CTkButton(
            right_column,
            text="Create Account",
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.register,
            hover_color="#4CAF50"
        )
        self.register_button.pack(fill="x", pady=(30, 10))
        
        # Back to login link
        back_to_login_label = ctk.CTkLabel(
            right_column,
            text="Already have an account? Back to Login",
            font=ctk.CTkFont(size=12),
            text_color="#2196F3",
            cursor="hand2"
        )
        back_to_login_label.pack(pady=10)
        back_to_login_label.bind("<Button-1>", self.back_to_login)
    
    def register(self):
        """Handle registration attempt"""
        full_name = self.full_name_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        # Validate input
        if not all([full_name, username, email, password, confirm_password]):
            self.show_error("Please fill in all fields")
            return
        
        # Validate full name
        if len(full_name) < 3:
            self.show_error("Full name must be at least 3 characters long")
            return
        
        # Validate username
        if len(username) < 3:
            self.show_error("Username must be at least 3 characters long")
            return
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            self.show_error("Username can only contain letters, numbers, and underscores")
            return
        
        # Check if username exists
        if self.check_username_exists(username):
            self.show_error("Username already exists. Please choose another one.")
            return
        
        # Validate email
        if not self.validate_email(email):
            self.show_error("Please enter a valid email address")
            return
        
        # Validate password strength
        is_strong, password_message = self.validate_password_strength(password)
        if not is_strong:
            self.show_error(password_message)
            return
        
        # Check password confirmation
        if password != confirm_password:
            self.show_error("Passwords do not match")
            return
        
        # Create user
        success, message = self.create_user_in_database(username, password, email)
        
        if success:
            log_user_action(f"User '{username}' registered successfully", "Authentication")
            self.show_success("Account created successfully!")
            
            # Call success callback after a short delay
            self.root.after(1500, self.on_register_success, username)
        else:
            self.show_error(message)
            log_user_action(f"Failed registration attempt for '{username}'", "Authentication")
    
    def back_to_login(self, event):
        """Handle back to login click"""
        log_user_action("Navigated back to login screen", "Authentication")
        self.on_back_to_login()
    
    def show_error(self, message):
        """Show error message"""
        self.status_label.configure(text=message, text_color="#F44336")
        self.root.after(3000, lambda: self.status_label.configure(text=""))
    
    def show_success(self, message):
        """Show success message"""
        self.status_label.configure(text=message, text_color="#4CAF50")
    
    def show_info(self, message):
        """Show info message"""
        self.status_label.configure(text=message, text_color="#2196F3")
        self.root.after(3000, lambda: self.status_label.configure(text=""))
    
    def focus_full_name(self):
        """Focus on full name field"""
        self.full_name_entry.focus()
    
    def clear_fields(self):
        """Clear all input fields"""
        self.full_name_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')
        self.status_label.configure(text="")