import sys
import os
import customtkinter as ctk
from PIL import Image, ImageTk

class LoginView(ctk.CTkFrame):
    def __init__(self, master, login_callback, register_callback):
        super().__init__(master)
        self.master = master
        self.login_callback = login_callback
        self.register_callback = register_callback
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Load background image
        self.bg_image = ctk.CTkImage(
            light_image=Image.open("resources/images/background_login.png"),
            dark_image=Image.open("resources/images/background_login.png"),
            size=(self.master.winfo_width(), self.master.winfo_height())
        )
        
        # Create background image label
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0, sticky="nsew")
        
        # Bind resize event to update background image size
        self.master.bind("<Configure>", self.update_background_size)
        
        # Create a main transparent frame for the login form
        self.login_form_frame = ctk.CTkFrame(self, fg_color="transparent", corner_radius=15)
        self.login_form_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.3, relheight=0.6)
        self.login_form_frame.grid_columnconfigure(0, weight=1)
        
        # Title text
        self.logo_label = ctk.CTkLabel(
            self.login_form_frame, 
            text="Billionnaires Budget Buddy", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        )
        self.logo_label.pack(pady=(30, 15))
        
        # Login subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.login_form_frame, 
            text="Please login to your account", 
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        self.subtitle_label.pack(pady=(0, 30))
        
        # Email label
        self.email_label = ctk.CTkLabel(
            self.login_form_frame, 
            text="Email:", 
            text_color="white"
        )
        self.email_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        # Email container with rounded corners
        self.email_container = ctk.CTkFrame(
            self.login_form_frame,
            corner_radius=8,
            fg_color=("#E0E0E0", "#3c3c3c"),  # Light and dark mode colors
            width=250  # Set specific width for container
        )
        self.email_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # Email entry inside container
        self.email_entry = ctk.CTkEntry(
            self.email_container,
            placeholder_text="Enter your email",
            border_width=0,
            fg_color="transparent",
            width=230  # Set specific width for entry
        )
        self.email_entry.pack(fill="x", padx=10, pady=8)
        
        # Password label
        self.password_label = ctk.CTkLabel(
            self.login_form_frame, 
            text="Password:", 
            text_color="white"
        )
        self.password_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        # Password container with rounded corners
        self.password_container = ctk.CTkFrame(
            self.login_form_frame,
            corner_radius=8,
            fg_color=("#E0E0E0", "#3c3c3c"),  # Light and dark mode colors
            width=250  # Set specific width for container
        )
        self.password_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # Password entry inside container
        self.password_entry = ctk.CTkEntry(
            self.password_container,
            placeholder_text="Enter your password",
            show="*",
            border_width=0,
            fg_color="transparent",
            width=230  # Set specific width for entry
        )
        self.password_entry.pack(fill="x", padx=10, pady=8)
        
        # Error message label with rounded container
        self.error_label = ctk.CTkLabel(
            self.login_form_frame, 
            text="", 
            text_color="red",
            fg_color=("#D9D9D9", "#2a2a2a"),
            corner_radius=5
        )
        self.error_label.pack(fill="x", padx=20, pady=(0, 15))
        
        # Login button
        self.login_button = ctk.CTkButton(
            self.login_form_frame, 
            text="Login", 
            command=self.login,
            fg_color="#3a7ebf",
            hover_color="#2b5f8f",
            corner_radius=8,
            width=250  # Set specific width for button
        )
        self.login_button.pack(fill="x", padx=20, pady=(0, 15))
        
        # Register option frame
        self.register_frame = ctk.CTkFrame(self.login_form_frame, fg_color="transparent")
        self.register_frame.pack(pady=15)
        
        # Register label
        self.register_label = ctk.CTkLabel(
            self.register_frame, 
            text="Don't have an account?", 
            text_color="white"
        )
        self.register_label.pack(side="left", padx=(0, 10))
        
        # Register button
        self.register_button = ctk.CTkButton(
            self.register_frame, 
            text="Register", 
            command=self.register,
            fg_color="transparent",
            text_color=["#1f538d", "#3a7ebf"],
            hover_color=["#e0e0e0", "#2d2d2d"],
            border_width=0
        )
        self.register_button.pack(side="left")
        
        # Bind enter key to login
        self.email_entry.bind("<Return>", lambda event: self.login())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Set focus to email field
        self.email_entry.focus_set()
    
    def update_background_size(self, event=None):
        """Update the background image size when window is resized."""
        # Only update if event is from master window
        if event and event.widget == self.master:
            new_width = event.width
            new_height = event.height
            self.bg_image.configure(size=(new_width, new_height))
    
    def login(self):
        # Get email and password
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        # Validate fields
        if not email or not password:
            self.error_label.configure(text="Please enter both email and password")
            return
        
        # Call the login callback
        success, message = self.login_callback(email, password)
        
        if not success:
            self.error_label.configure(text=message)
    
    def register(self):
        # Call the register callback
        self.register_callback() 