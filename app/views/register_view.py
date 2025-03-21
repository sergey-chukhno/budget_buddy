import customtkinter as ctk
from PIL import Image, ImageTk
import os
import re

class RegisterView(ctk.CTkFrame):
    def __init__(self, master, register_callback, back_callback):
        super().__init__(master)
        self.master = master
        self.register_callback = register_callback
        self.back_callback = back_callback
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create a main frame for the register form
        self.register_frame = ctk.CTkFrame(self, corner_radius=15)
        self.register_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.register_frame.grid_columnconfigure(0, weight=1)
        self.register_frame.grid_rowconfigure(3, weight=1)
        
        # Load background image
        bg_image = ctk.CTkImage(
        Image.open("fin_tracker_sql/assets/background_register.png"),
        size=(1980,1980))

        self.bg_label = ctk.CTkLabel(self.register_frame, image=bg_image, text="")
        self.bg_label.place(relwidth=1,relheight=1)
        # Logo and title
        self.logo_label = ctk.CTkLabel(
            self.register_frame, 
            text="Billionnaires Budget Buddy", 
            font=ctk.CTkFont(size=24, weight="bold")
        )

        # Logo and title
        logo = Image.open("fin_tracker_sql/assets/new_logo.png")
        image_ctk = ctk.CTkImage(light_image=logo, dark_image=logo, size=(200, 200))
        self.logo_label = ctk.CTkLabel(
            self.register_frame,
            image=image_ctk, 
            text="", 
            )
        self.logo_label.grid(row=0, column=0, padx=30, pady=(30, 15))


        self.logo_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        
        # Register subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.register_frame, 
            text="Create a new account", 
            font=ctk.CTkFont(size=16)
        )
        self.subtitle_label.grid(row=1, column=0, padx=30, pady=(0, 15))
        
        # Register form
        self.register_form_frame = ctk.CTkFrame(self.register_frame, fg_color="white")
        self.register_form_frame.grid(row=2, column=0, padx=30, pady=15, sticky="ew")
        self.register_form_frame.grid_columnconfigure((0, 1), weight=1)
        
        


        # Email field
        self.email_label = ctk.CTkLabel(self.register_form_frame, text="Email:",text_color="#3a7ebf")
        self.email_label.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w", columnspan=2)
        self.email_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Enter your email",text_color="#3a7ebf")
        self.email_entry.grid(row=1, column=0, padx=10, pady=(0, 15), sticky="ew", columnspan=2)
        
        # Password field
        self.password_label = ctk.CTkLabel(self.register_form_frame, text="Password:",text_color="#3a7ebf")
        self.password_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
        self.password_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Enter your password", show="*")
        self.password_entry.grid(row=3, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # Confirm password field
        self.confirm_password_label = ctk.CTkLabel(self.register_form_frame, text="Confirm Password:",text_color="#3a7ebf")
        self.confirm_password_label.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="w")
        self.confirm_password_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Confirm your password", show="*")
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=(0, 15), sticky="ew")
        
        # First name field
        self.first_name_label = ctk.CTkLabel(self.register_form_frame, text="First Name:",text_color="#3a7ebf")
        self.first_name_label.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")
        self.first_name_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Enter your first name")
        self.first_name_entry.grid(row=5, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # Last name field
        self.last_name_label = ctk.CTkLabel(self.register_form_frame, text="Last Name:",text_color="#3a7ebf")
        self.last_name_label.grid(row=4, column=1, padx=10, pady=(0, 5), sticky="w")
        self.last_name_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Enter your last name")
        self.last_name_entry.grid(row=5, column=1, padx=10, pady=(0, 15), sticky="ew")
        
        # Phone field
        self.phone_label = ctk.CTkLabel(self.register_form_frame, text="Phone:",text_color="#3a7ebf")
        self.phone_label.grid(row=6, column=0, padx=10, pady=(0, 5), sticky="w")
        self.phone_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Enter your phone number")
        self.phone_entry.grid(row=7, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # Address field
        self.address_label = ctk.CTkLabel(self.register_form_frame, text="Address:",text_color="#3a7ebf")
        self.address_label.grid(row=6, column=1, padx=10, pady=(0, 5), sticky="w")
        self.address_entry = ctk.CTkEntry(self.register_form_frame, placeholder_text="Enter your address")
        self.address_entry.grid(row=7, column=1, padx=10, pady=(0, 15), sticky="ew")
        
        # Error message label
        self.error_label = ctk.CTkLabel(self.register_form_frame, text="", text_color="red")
        self.error_label.grid(row=8, column=0, padx=10, pady=(0, 15), sticky="ew", columnspan=2)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.register_form_frame, fg_color="transparent")
        self.buttons_frame.grid(row=9, column=0, padx=10, pady=(0, 15), sticky="ew", columnspan=2)
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Register button
        self.register_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Register", 
            command=self.register,
            fg_color="#3a7ebf",
            hover_color="#2b5f8f"
        )
        self.register_button.grid(row=0, column=1, padx=10, pady=0, sticky="e")
        
        # Back button
        self.back_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Back to Login", 
            command=self.back,
            fg_color="transparent",
            text_color=["#1f538d", "#3a7ebf"],
            hover_color=["#E3E3E3", "#2D2D2D"],
            border_width=0
        )
        self.back_button.grid(row=0, column=0, padx=10, pady=0, sticky="w")
    
    def validate_email(self, email):
        """Validate email format."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
    
    def register(self):
        # Get all field values
        email = self.email_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        phone = self.phone_entry.get()
        address = self.address_entry.get()
        
        # Validate required fields
        if not email or not password or not confirm_password or not first_name or not last_name:
            self.error_label.configure(text="Please fill in all required fields")
            return
        
        # Validate email format
        if not self.validate_email(email):
            self.error_label.configure(text="Please enter a valid email address")
            return
        
        # Validate password match
        if password != confirm_password:
            self.error_label.configure(text="Passwords do not match")
            return
        
        # Validate password length
        if len(password) < 6:
            self.error_label.configure(text="Password must be at least 6 characters long")
            return
        
        # Call the register callback
        success, message = self.register_callback(email, password, first_name, last_name, phone, address)
        
        if not success:
            self.error_label.configure(text=message)
    
    def back(self):
        # Call the back callback
        self.back_callback() 