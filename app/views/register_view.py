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
        
        # Load background image
        self.bg_image = ctk.CTkImage(
            light_image=Image.open("resources/images/background_register.png"),
            dark_image=Image.open("resources/images/background_register.png"),
            size=(self.master.winfo_width(), self.master.winfo_height())
        )
        
        # Create background image label
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0, sticky="nsew")
        
        # Bind resize event to update background image size
        self.master.bind("<Configure>", self.update_background_size)
        
        # Create a main transparent frame for the register form
        self.register_form_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=15)
        self.register_form_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.6, relheight=0.65)
        self.register_form_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Title text
        self.logo_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="Billionnaires Budget Buddy", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(30, 15))
        
        # Register subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="Create a new account", 
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        self.subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Email label
        self.email_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="Email:", 
            text_color="white"
        )
        self.email_label.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w", columnspan=2)
        
        # Email container
        self.email_container = ctk.CTkFrame(
            self.register_form_frame,
            corner_radius=8,
            fg_color=("#E0E0E0", "#3c3c3c")  # Light and dark mode colors
        )
        self.email_container.grid(row=1, column=0, padx=10, pady=(0, 15), sticky="ew", columnspan=2)
        
        # Email entry
        self.email_entry = ctk.CTkEntry(
            self.email_container,
            placeholder_text="Enter your email",
            border_width=0,
            fg_color="transparent"
        )
        self.email_entry.pack(fill="x", padx=10, pady=8)
        
        # Password label
        self.password_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="Password:", 
            text_color="white"
        )
        self.password_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
        
        # Password container
        self.password_container = ctk.CTkFrame(
            self.register_form_frame,
            corner_radius=8,
            fg_color=("#E0E0E0", "#3c3c3c")  # Light and dark mode colors
        )
        self.password_container.grid(row=3, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.password_container,
            placeholder_text="Enter your password",
            show="*",
            border_width=0,
            fg_color="transparent"
        )
        self.password_entry.pack(fill="x", padx=10, pady=8)
        
        # Confirm password label
        self.confirm_password_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="Confirm Password:", 
            text_color="white"
        )
        self.confirm_password_label.grid(row=2, column=1, padx=10, pady=(0, 5), sticky="w")
        
        # Confirm password container
        self.confirm_password_container = ctk.CTkFrame(
            self.register_form_frame,
            corner_radius=8,
            fg_color=("#E0E0E0", "#3c3c3c")  # Light and dark mode colors
        )
        self.confirm_password_container.grid(row=3, column=1, padx=10, pady=(0, 15), sticky="ew")
        
        # Confirm password entry
        self.confirm_password_entry = ctk.CTkEntry(
            self.confirm_password_container,
            placeholder_text="Confirm your password",
            show="*",
            border_width=0,
            fg_color="transparent"
        )
        self.confirm_password_entry.pack(fill="x", padx=10, pady=8)
        
        # First name label
        self.first_name_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="First Name:", 
            text_color="white"
        )
        self.first_name_label.grid(row=4, column=0, padx=10, pady=(0, 5), sticky="w")
        
        # First name container
        self.first_name_container = ctk.CTkFrame(
            self.register_form_frame,
            corner_radius=8,
            fg_color=("#E0E0E0", "#3c3c3c")  # Light and dark mode colors
        )
        self.first_name_container.grid(row=5, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # First name entry
        self.first_name_entry = ctk.CTkEntry(
            self.first_name_container,
            placeholder_text="Enter your first name",
            border_width=0,
            fg_color="transparent"
        )
        self.first_name_entry.pack(fill="x", padx=10, pady=8)
        
        # Last name label
        self.last_name_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="Last Name:", 
            text_color="white"
        )
        self.last_name_label.grid(row=4, column=1, padx=10, pady=(0, 5), sticky="w")
        
        # Last name container
        self.last_name_container = ctk.CTkFrame(
            self.register_form_frame,
            corner_radius=8,
            fg_color=("#E0E0E0", "#3c3c3c")  # Light and dark mode colors
        )
        self.last_name_container.grid(row=5, column=1, padx=10, pady=(0, 15), sticky="ew")
        
        # Last name entry
        self.last_name_entry = ctk.CTkEntry(
            self.last_name_container,
            placeholder_text="Enter your last name",
            border_width=0,
            fg_color="transparent"
        )
        self.last_name_entry.pack(fill="x", padx=10, pady=8)
        
        # Phone label
        self.phone_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="Phone:", 
            text_color="white"
        )
        self.phone_label.grid(row=6, column=0, padx=10, pady=(0, 5), sticky="w")
        
        # Phone container
        self.phone_container = ctk.CTkFrame(
            self.register_form_frame,
            corner_radius=8,
            fg_color=("#E0E0E0", "#3c3c3c")  # Light and dark mode colors
        )
        self.phone_container.grid(row=7, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # Phone entry
        self.phone_entry = ctk.CTkEntry(
            self.phone_container,
            placeholder_text="Enter your phone number",
            border_width=0,
            fg_color="transparent"
        )
        self.phone_entry.pack(fill="x", padx=10, pady=8)
        
        # Address label
        self.address_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="Address:", 
            text_color="white"
        )
        self.address_label.grid(row=6, column=1, padx=10, pady=(0, 5), sticky="w")
        
        # Address container
        self.address_container = ctk.CTkFrame(
            self.register_form_frame,
            corner_radius=8,
            fg_color=("#E0E0E0", "#3c3c3c")  # Light and dark mode colors
        )
        self.address_container.grid(row=7, column=1, padx=10, pady=(0, 15), sticky="ew")
        
        # Address entry
        self.address_entry = ctk.CTkEntry(
            self.address_container,
            placeholder_text="Enter your address",
            border_width=0,
            fg_color="transparent"
        )
        self.address_entry.pack(fill="x", padx=10, pady=8)
        
        # Error message label
        self.error_label = ctk.CTkLabel(
            self.register_form_frame, 
            text="", 
            text_color="red",
            fg_color=("#D9D9D9", "#2a2a2a"),
            corner_radius=5
        )
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
            hover_color="#2b5f8f",
            corner_radius=8
        )
        self.register_button.grid(row=0, column=1, padx=10, pady=0, sticky="e")
        
        # Back button
        self.back_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Back to Login", 
            command=self.back,
            fg_color="transparent",
            text_color=["#1f538d", "#3a7ebf"],
            hover_color=["#e0e0e0", "#2d2d2d"],
            border_width=0
        )
        self.back_button.grid(row=0, column=0, padx=10, pady=0, sticky="w")
    
    def update_background_size(self, event=None):
        """Update the background image size when window is resized."""
        # Only update if event is from master window
        if event and event.widget == self.master:
            new_width = event.width
            new_height = event.height
            self.bg_image.configure(size=(new_width, new_height))
    
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