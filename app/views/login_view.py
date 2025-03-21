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
        
        # Create a main frame for the login form
        self.login_frame = ctk.CTkFrame(self, corner_radius=15)
        self.login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(4, weight=1)
        
        # Logo and title
        logo = Image.open("fin_tracker_sql/assets/new_logo.png")
        image_ctk = ctk.CTkImage(light_image=logo, dark_image=logo, size=(200, 200))
        self.logo_label = ctk.CTkLabel(
            self.login_frame,
            image=image_ctk, 
            text="", 
            )
        self.logo_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        
        # Login subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.login_frame, 
            text="Please login to your account", 
            font=ctk.CTkFont(size=16)
        )
        self.subtitle_label.grid(row=1, column=0, padx=30, pady=(0, 15))
        
        # Login form
        self.login_form_frame = ctk.CTkFrame(self.login_frame, fg_color="lightgrey")
        self.login_form_frame.grid(row=2, column=0, padx=30, pady=15)
        self.login_form_frame.grid_columnconfigure(0, weight=1)
        
        # Email field
        self.email_label = ctk.CTkLabel(self.login_form_frame, text="Email:",text_color="#3a7ebf")
        self.email_label.grid(row=0, column=0, padx=10, pady=(0, 5), sticky="w")
        self.email_entry = ctk.CTkEntry(self.login_form_frame, placeholder_text="Enter your email", width=300)
        self.email_entry.grid(row=1, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # Password field
        self.password_label = ctk.CTkLabel(self.login_form_frame, text="Password:",text_color="#3a7ebf")
        self.password_label.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")
        self.password_entry = ctk.CTkEntry(self.login_form_frame, placeholder_text="Enter your password", show="*", width=300)
        self.password_entry.grid(row=3, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # Error message label
        self.error_label = ctk.CTkLabel(self.login_form_frame, text="", text_color="#3a7ebf")
        self.error_label.grid(row=4, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # Login button
        self.login_button = ctk.CTkButton(
            self.login_form_frame, 
            text="Login", 
            command=self.login,
            fg_color="#3a7ebf",
            hover_color="#2b5f8f"
        )
        self.login_button.grid(row=5, column=0, padx=10, pady=(0, 15), sticky="ew")
        
        # Register option
        self.register_frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.register_frame.grid(row=3, column=0, padx=30, pady=15)
        
        self.register_label = ctk.CTkLabel(self.register_frame, text="Don't have an account?",text_color="red")
        self.register_label.grid(row=0, column=0, padx=(0, 10))
        
        self.register_button = ctk.CTkButton(
            self.register_frame, 
            text="Register", 
            command=self.register,
            fg_color="transparent",
            text_color=["#1f538d", "#3a7ebf"],
            hover_color=["#E3E3E3", "#2D2D2D"],
            border_width=0
        )
        self.register_button.grid(row=0, column=1)
        
        # Bind enter key to login
        self.email_entry.bind("<Return>", lambda event: self.login())
        self.password_entry.bind("<Return>", lambda event: self.login())
        
        # Set focus to email field
        self.email_entry.focus_set()
    
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