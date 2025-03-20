import customtkinter as ctk
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.user import User

class SettingsView(ctk.CTkFrame):
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
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", padx=0, pady=0)
        
        self.save_btn = ctk.CTkButton(
            self.header_frame,
            text="Save Changes",
            command=self.save_settings
        )
        self.save_btn.pack(side="right", padx=0, pady=0)
        
        # Settings content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Create a tabview for different settings categories
        self.tabview = ctk.CTkTabview(self.content_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Profile")
        self.tabview.add("Account")
        self.tabview.add("Appearance")
        self.tabview.add("Notifications")
        self.tabview.add("Security")
        
        # Profile tab placeholder
        self.profile_placeholder = ctk.CTkLabel(
            self.tabview.tab("Profile"),
            text="Profile settings would include:\n\n"
                 "• Name and contact information\n"
                 "• Profile picture\n"
                 "• Personal details\n"
                 "• Language preferences",
            wraplength=500
        )
        self.profile_placeholder.pack(pady=50)
        
        # Account tab placeholder
        self.account_placeholder = ctk.CTkLabel(
            self.tabview.tab("Account"),
            text="Account settings would include:\n\n"
                 "• Account type management\n"
                 "• Default currency\n"
                 "• Linked accounts\n"
                 "• Export account data",
            wraplength=500
        )
        self.account_placeholder.pack(pady=50)
        
        # Appearance tab placeholder
        self.appearance_placeholder = ctk.CTkLabel(
            self.tabview.tab("Appearance"),
            text="Appearance settings would include:\n\n"
                 "• Theme selection (Light/Dark)\n"
                 "• Color scheme\n"
                 "• Font size\n"
                 "• Dashboard layout options",
            wraplength=500
        )
        self.appearance_placeholder.pack(pady=50)
        
        # Notifications tab placeholder
        self.notifications_placeholder = ctk.CTkLabel(
            self.tabview.tab("Notifications"),
            text="Notification settings would include:\n\n"
                 "• Transaction alerts\n"
                 "• Balance notifications\n"
                 "• Bill reminders\n"
                 "• Security alerts\n"
                 "• Email notification preferences",
            wraplength=500
        )
        self.notifications_placeholder.pack(pady=50)
        
        # Security tab placeholder
        self.security_placeholder = ctk.CTkLabel(
            self.tabview.tab("Security"),
            text="Security settings would include:\n\n"
                 "• Password change\n"
                 "• Two-factor authentication\n"
                 "• Login history\n"
                 "• Session management\n"
                 "• Privacy settings",
            wraplength=500
        )
        self.security_placeholder.pack(pady=50)
    
    def save_settings(self):
        """Save user settings."""
        print("Settings would be saved here")
        # In a complete implementation, this would validate and save all settings 