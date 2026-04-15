import customtkinter as ctk
from PIL import ImageTk, Image, ImageDraw
import hashlib
from src.utils.logger import log_user_action, log_system_event
from src.ui.register import Register

class Login:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.attempts = 0
        self.max_attempts = 3
        
        # Default admin credentials (in production, these should be stored securely)
        self.admin_username = "admin"
        self.admin_password = self.hash_password("admin123")
        
        self.create_login_ui()
        log_system_event("Login screen initialized")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_credentials(self, username, password):
        """Verify user credentials"""
        hashed_password = self.hash_password(password)
        
        # Check admin credentials (in production, check against database)
        if username == self.admin_username and hashed_password == self.admin_password:
            return True
        
        # Add more user checks here in production
        return False
    
    def create_login_ui(self):
        """Create the login interface"""
        # Clear the root window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set window properties for login - full screen
        self.root.title("MedRX Inventory System - Login")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)
        
        # Main login container - fixed dimensions to prevent stretching
        self.login_frame = ctk.CTkFrame(self.root, corner_radius=15, width=450, height=650)
        self.login_frame.pack(expand=True)
        self.login_frame.pack_propagate(False)  # Prevent frame from resizing to children
        
        # Logo and title section
        self.create_header_section()
        
        # Login form section
        self.create_login_form()
        
        # Status message label
        self.status_label = ctk.CTkLabel(
            self.login_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#F44336"
        )
        self.status_label.pack(pady=(10, 0))
    
    def create_header_section(self):
        """Create logo and title section"""
        # Logo container
        logo_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        logo_frame.pack(pady=(30, 20))
        
        try:
            # Load and process logo
            original_image = Image.open("assets/MedRX_logo.png")
            size = 100
            resized_image = original_image.resize((size, size))
            
            # Create rounded corners
            mask = Image.new('L', (size, size), 0)
            from PIL import ImageDraw
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([(0, 0), (size, size)], radius=80, fill=255)
            
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
            self.login_frame,
            text="MedRX Inventory System",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            self.login_frame,
            text="Please login to continue",
            font=ctk.CTkFont(size=14),
            text_color="#666666"
        )
        subtitle_label.pack(pady=(0, 30))
    
    def create_login_form(self):
        """Create the login form fields"""
        # Username field
        username_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        username_frame.pack(fill="x", padx=40, pady=10)
        
        username_label = ctk.CTkLabel(
            username_frame,
            text="Username:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        username_label.pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            username_frame,
            placeholder_text="Enter your username",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(fill="x")
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Password field
        password_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        password_frame.pack(fill="x", padx=40, pady=10)
        
        password_label = ctk.CTkLabel(
            password_frame,
            text="Password:",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        password_label.pack(fill="x", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            password_frame,
            placeholder_text="Enter your password",
            show="•",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(fill="x")
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Remember me checkbox
        self.remember_me_var = ctk.BooleanVar()
        remember_me_checkbox = ctk.CTkCheckBox(
            self.login_frame,
            text="Remember me",
            variable=self.remember_me_var,
            font=ctk.CTkFont(size=12)
        )
        remember_me_checkbox.pack(pady=(20, 10))
        
        # Login button
        self.login_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.login,
            hover_color="#1E88E5"
        )
        self.login_button.pack(fill="x", padx=40, pady=(10, 20))
        
        # Forgot password link
        forgot_password_label = ctk.CTkLabel(
            self.login_frame,
            text="Forgot Password?",
            font=ctk.CTkFont(size=12),
            text_color="#2196F3",
            cursor="hand2"
        )
        forgot_password_label.pack(pady=5)
        forgot_password_label.bind("<Button-1>", self.forgot_password)
        
        # Register link
        register_label = ctk.CTkLabel(
            self.login_frame,
            text="Register",
            font=ctk.CTkFont(size=12),
            text_color="#4CAF50",
            cursor="hand2"
        )
        register_label.pack(pady=5)
        register_label.bind("<Button-1>", self.go_to_register)
        
        # Default credentials info
        info_frame = ctk.CTkFrame(self.login_frame, fg_color="#F5F5F5")
        info_frame.pack(fill="x", padx=40, pady=(30, 0))
        
        info_label = ctk.CTkLabel(
            info_frame,
            text="Default: admin / admin123",
            font=ctk.CTkFont(size=11),
            text_color="#666666"
        )
        info_label.pack(pady=10)
    
    def login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validate input
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
        
        # Verify credentials
        if self.verify_credentials(username, password):
            log_user_action(f"User '{username}' logged in successfully", "Authentication")
            self.show_success("Login successful!")
            
            # Call success callback
            self.root.after(500, self.on_login_success, username)
        else:
            self.attempts += 1
            remaining_attempts = self.max_attempts - self.attempts
            
            if remaining_attempts > 0:
                self.show_error(f"Invalid credentials. {remaining_attempts} attempts remaining.")
                log_user_action(f"Failed login attempt for '{username}'", "Authentication")
                
                # Clear password field
                self.password_entry.delete(0, 'end')
                self.password_entry.focus()
            else:
                self.show_error("Too many failed attempts. Application will close.")
                log_system_event("Maximum login attempts reached")
                self.root.after(2000, self.root.quit)
    
    def forgot_password(self, event):
        """Handle forgot password click"""
        self.show_info("Contact your system administrator to reset your password.")
        log_user_action("Password reset requested", "Authentication")
    
    def go_to_register(self, event):
        """Handle register click"""
        log_user_action("Navigated to registration screen", "Authentication")
        # Create registration screen with callbacks
        register_screen = Register(
            self.root, 
            on_register_success=self.on_register_success,
            on_back_to_login=self.back_to_login
        )
    
    def on_register_success(self, username):
        """Called when registration is successful"""
        log_user_action(f"User '{username}' successfully registered", "Authentication")
        # Show success message and go back to login
        self.show_success("Registration successful! You can now login.")
        # Recreate login screen after a short delay
        self.root.after(2000, self.create_login_ui)
    
    def back_to_login(self):
        """Go back to login screen"""
        log_user_action("Returned to login screen from registration", "Authentication")
        self.create_login_ui()
    
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
    
    def focus_username(self):
        """Focus on username field"""
        self.username_entry.focus()
    
    def clear_fields(self):
        """Clear all input fields"""
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.remember_me_var.set(False)
        self.status_label.configure(text="")