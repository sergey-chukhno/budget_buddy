import customtkinter as ctk
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.account import Account

class AccountsView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.user = user
        
        # Set up grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Accounts",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", padx=0, pady=0)
        
        # Add account button
        self.add_account_button = ctk.CTkButton(
            self.header_frame,
            text="Add Account",
            width=120,
            command=self.add_account
        )
        self.add_account_button.pack(side="right", padx=0, pady=0)
        
        # Content placeholder
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Placeholder message
        self.placeholder = ctk.CTkLabel(
            self.content_frame,
            text="In a complete implementation, this view would display all user accounts with options to view details, edit, and delete accounts.",
            wraplength=600
        )
        self.placeholder.pack(pady=100)
    
    def add_account(self):
        """Show dialog to add a new account."""
        # In a complete implementation, this would show a dialog to create a new account
        print("Add account dialog would appear here") 