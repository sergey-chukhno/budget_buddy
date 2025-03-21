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
        
        # Add new tabs
        self.tabview.add("Account")
        self.tabview.add("Security")
        self.tabview.add("Preferences")
        
        # Account tab content
        self.setup_account_tab()
        
        # Security tab content
        self.setup_security_tab()
        
        # Preferences tab content
        self.setup_preferences_tab()
    
    def setup_account_tab(self):
        """Set up the Account tab with user profile and account settings."""
        account_frame = ctk.CTkFrame(self.tabview.tab("Account"), fg_color="transparent")
        account_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        account_title = ctk.CTkLabel(
            account_frame,
            text="Account Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        account_title.pack(anchor="w", pady=(0, 20))
        
        # User information section
        user_info_frame = ctk.CTkFrame(account_frame)
        user_info_frame.pack(fill="x", padx=10, pady=10)
        
        # Extract first and last name from user.name
        name_parts = self.user.name.split(" ", 1) if self.user.name else ["", ""]
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""
        
        # First name field
        first_name_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        first_name_frame.pack(fill="x", pady=10)
        
        first_name_label = ctk.CTkLabel(first_name_frame, text="First Name:", width=120, anchor="w")
        first_name_label.pack(side="left", padx=(10, 0))
        
        self.first_name_entry = ctk.CTkEntry(first_name_frame, placeholder_text="Enter your first name")
        self.first_name_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.first_name_entry.insert(0, first_name)
        
        # Last name field
        last_name_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        last_name_frame.pack(fill="x", pady=10)
        
        last_name_label = ctk.CTkLabel(last_name_frame, text="Last Name:", width=120, anchor="w")
        last_name_label.pack(side="left", padx=(10, 0))
        
        self.last_name_entry = ctk.CTkEntry(last_name_frame, placeholder_text="Enter your last name")
        self.last_name_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.last_name_entry.insert(0, last_name)
        
        # Email field
        email_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        email_frame.pack(fill="x", pady=10)
        
        email_label = ctk.CTkLabel(email_frame, text="Email:", width=120, anchor="w")
        email_label.pack(side="left", padx=(10, 0))
        
        self.email_entry = ctk.CTkEntry(email_frame, placeholder_text="Enter your email")
        self.email_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.email_entry.insert(0, self.user.email)
        
        # Divider
        divider = ctk.CTkFrame(account_frame, height=2, fg_color="gray30")
        divider.pack(fill="x", padx=10, pady=20)
        
        # Account preferences section
        preferences_title = ctk.CTkLabel(
            account_frame,
            text="Account Preferences",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        preferences_title.pack(anchor="w", pady=(0, 20))
        
        # Currency preference
        currency_frame = ctk.CTkFrame(account_frame, fg_color="transparent")
        currency_frame.pack(fill="x", pady=10)
        
        currency_label = ctk.CTkLabel(currency_frame, text="Default Currency:", width=120, anchor="w")
        currency_label.pack(side="left", padx=(10, 0))
        
        currencies = ["USD ($)", "EUR (€)", "GBP (£)", "JPY (¥)", "CAD (C$)"]
        self.currency_var = ctk.StringVar(value=currencies[0])
        
        currency_dropdown = ctk.CTkOptionMenu(
            currency_frame,
            variable=self.currency_var,
            values=currencies,
            width=120
        )
        currency_dropdown.pack(side="left", padx=10)
        
        # Timezone preference
        timezone_frame = ctk.CTkFrame(account_frame, fg_color="transparent")
        timezone_frame.pack(fill="x", pady=10)
        
        timezone_label = ctk.CTkLabel(timezone_frame, text="Timezone:", width=120, anchor="w")
        timezone_label.pack(side="left", padx=(10, 0))
        
        timezones = [
            "UTC (GMT+0)", 
            "America/New_York (GMT-5/4)", 
            "America/Chicago (GMT-6/5)", 
            "America/Denver (GMT-7/6)", 
            "America/Los_Angeles (GMT-8/7)",
            "Europe/London (GMT+0/1)",
            "Europe/Paris (GMT+1/2)",
            "Asia/Tokyo (GMT+9)",
            "Australia/Sydney (GMT+10/11)"
        ]
        self.timezone_var = ctk.StringVar(value=timezones[0])
        
        timezone_dropdown = ctk.CTkOptionMenu(
            timezone_frame,
            variable=self.timezone_var,
            values=timezones,
            width=200
        )
        timezone_dropdown.pack(side="left", padx=10)
        
        # Divider
        divider2 = ctk.CTkFrame(account_frame, height=2, fg_color="gray30")
        divider2.pack(fill="x", padx=10, pady=20)
        
        # Login information section
        login_info_title = ctk.CTkLabel(
            account_frame,
            text="Login Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        login_info_title.pack(anchor="w", pady=(0, 20))
        
        # Login info frame
        login_info_frame = ctk.CTkFrame(account_frame)
        login_info_frame.pack(fill="x", padx=10, pady=10)
        
        # Last login time
        last_login_frame = ctk.CTkFrame(login_info_frame, fg_color="transparent")
        last_login_frame.pack(fill="x", pady=5)
        
        last_login_label = ctk.CTkLabel(
            last_login_frame, 
            text="Last Login:", 
            width=120, 
            anchor="w",
            font=ctk.CTkFont(weight="bold")
        )
        last_login_label.pack(side="left", padx=(10, 0))
        
        # In a real implementation, this would be dynamically retrieved from the database
        last_login_time = "2025-03-21 07:08:35"
        
        last_login_value = ctk.CTkLabel(
            last_login_frame,
            text=last_login_time,
            anchor="w"
        )
        last_login_value.pack(side="left", padx=10)
        
        # Current session start
        session_frame = ctk.CTkFrame(login_info_frame, fg_color="transparent")
        session_frame.pack(fill="x", pady=5)
        
        session_label = ctk.CTkLabel(
            session_frame, 
            text="Current Session:", 
            width=120, 
            anchor="w",
            font=ctk.CTkFont(weight="bold")
        )
        session_label.pack(side="left", padx=(10, 0))
        
        # In a real implementation, this would be the current session start time
        session_start = "2025-03-21 07:09:35"
        
        session_value = ctk.CTkLabel(
            session_frame,
            text=session_start,
            anchor="w"
        )
        session_value.pack(side="left", padx=10)
        
        # Device information
        device_frame = ctk.CTkFrame(login_info_frame, fg_color="transparent")
        device_frame.pack(fill="x", pady=5)
        
        device_label = ctk.CTkLabel(
            device_frame, 
            text="Device:", 
            width=120, 
            anchor="w",
            font=ctk.CTkFont(weight="bold")
        )
        device_label.pack(side="left", padx=(10, 0))
        
        # In a real implementation, this would be detected from the user's system
        device_info = "MacOS 24.3.0"
        
        device_value = ctk.CTkLabel(
            device_frame,
            text=device_info,
            anchor="w"
        )
        device_value.pack(side="left", padx=10)
    
    def setup_security_tab(self):
        """Set up the Security tab with password and security settings."""
        security_frame = ctk.CTkFrame(self.tabview.tab("Security"), fg_color="transparent")
        security_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        security_title = ctk.CTkLabel(
            security_frame,
            text="Security Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        security_title.pack(anchor="w", pady=(0, 20))
        
        # Password change section
        password_frame = ctk.CTkFrame(security_frame)
        password_frame.pack(fill="x", padx=10, pady=10)
        
        password_title = ctk.CTkLabel(
            password_frame,
            text="Change Password",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        password_title.pack(anchor="w", padx=10, pady=10)
        
        # Current password
        current_pw_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
        current_pw_frame.pack(fill="x", pady=5)
        
        current_pw_label = ctk.CTkLabel(current_pw_frame, text="Current Password:", width=150, anchor="w")
        current_pw_label.pack(side="left", padx=(10, 0))
        
        self.current_pw_entry = ctk.CTkEntry(current_pw_frame, placeholder_text="Enter current password", show="*")
        self.current_pw_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        # New password
        new_pw_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
        new_pw_frame.pack(fill="x", pady=5)
        
        new_pw_label = ctk.CTkLabel(new_pw_frame, text="New Password:", width=150, anchor="w")
        new_pw_label.pack(side="left", padx=(10, 0))
        
        self.new_pw_entry = ctk.CTkEntry(new_pw_frame, placeholder_text="Enter new password", show="*")
        self.new_pw_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        # Confirm new password
        confirm_pw_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
        confirm_pw_frame.pack(fill="x", pady=5)
        
        confirm_pw_label = ctk.CTkLabel(confirm_pw_frame, text="Confirm New Password:", width=150, anchor="w")
        confirm_pw_label.pack(side="left", padx=(10, 0))
        
        self.confirm_pw_entry = ctk.CTkEntry(confirm_pw_frame, placeholder_text="Confirm new password", show="*")
        self.confirm_pw_entry.pack(side="left", fill="x", expand=True, padx=10)
        
        # Change password button
        change_pw_button = ctk.CTkButton(
            password_frame,
            text="Change Password",
            command=self.change_password
        )
        change_pw_button.pack(anchor="w", padx=10, pady=10)
        
        # Divider
        divider = ctk.CTkFrame(security_frame, height=2, fg_color="gray30")
        divider.pack(fill="x", padx=10, pady=20)
        
        # Session settings
        session_frame = ctk.CTkFrame(security_frame)
        session_frame.pack(fill="x", padx=10, pady=10)
        
        session_title = ctk.CTkLabel(
            session_frame,
            text="Session Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        session_title.pack(anchor="w", padx=10, pady=10)
        
        # Auto logout option
        auto_logout_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
        auto_logout_frame.pack(fill="x", pady=5)
        
        auto_logout_label = ctk.CTkLabel(auto_logout_frame, text="Auto Logout After:", width=150, anchor="w")
        auto_logout_label.pack(side="left", padx=(10, 0))
        
        logout_options = ["Never", "15 minutes", "30 minutes", "1 hour", "3 hours"]
        self.logout_var = ctk.StringVar(value=logout_options[1])
        
        logout_dropdown = ctk.CTkOptionMenu(
            auto_logout_frame,
            variable=self.logout_var,
            values=logout_options,
            width=120
        )
        logout_dropdown.pack(side="left", padx=10)
    
    def setup_preferences_tab(self):
        """Set up the Preferences tab with appearance and notification settings."""
        preferences_frame = ctk.CTkFrame(self.tabview.tab("Preferences"), fg_color="transparent")
        preferences_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        preferences_title = ctk.CTkLabel(
            preferences_frame,
            text="Application Preferences",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        preferences_title.pack(anchor="w", pady=(0, 20))
        
        # Appearance settings
        appearance_frame = ctk.CTkFrame(preferences_frame)
        appearance_frame.pack(fill="x", padx=10, pady=10)
        
        appearance_title = ctk.CTkLabel(
            appearance_frame,
            text="Appearance",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        appearance_title.pack(anchor="w", padx=10, pady=10)
        
        # Theme selection
        theme_frame = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        theme_frame.pack(fill="x", pady=5)
        
        theme_label = ctk.CTkLabel(theme_frame, text="Theme:", width=100, anchor="w")
        theme_label.pack(side="left", padx=(10, 0))
        
        themes = ["System", "Dark", "Light"]
        self.theme_var = ctk.StringVar(value=themes[1])  # Default to Dark
        
        for i, theme in enumerate(themes):
            theme_radio = ctk.CTkRadioButton(
                theme_frame,
                text=theme,
                variable=self.theme_var,
                value=theme
            )
            theme_radio.pack(side="left", padx=10)
        
        # Font size
        font_frame = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        font_frame.pack(fill="x", pady=5)
        
        font_label = ctk.CTkLabel(font_frame, text="Font Size:", width=100, anchor="w")
        font_label.pack(side="left", padx=(10, 0))
        
        font_sizes = ["Small", "Medium", "Large"]
        self.font_var = ctk.StringVar(value=font_sizes[1])  # Default to Medium
        
        font_dropdown = ctk.CTkOptionMenu(
            font_frame,
            variable=self.font_var,
            values=font_sizes,
            width=120
        )
        font_dropdown.pack(side="left", padx=10)
        
        # Divider
        divider = ctk.CTkFrame(preferences_frame, height=2, fg_color="gray30")
        divider.pack(fill="x", padx=10, pady=20)
        
        # Notification settings
        notification_frame = ctk.CTkFrame(preferences_frame)
        notification_frame.pack(fill="x", padx=10, pady=10)
        
        notification_title = ctk.CTkLabel(
            notification_frame,
            text="Notifications",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        notification_title.pack(anchor="w", padx=10, pady=10)
        
        # Transaction alerts
        self.transaction_alerts_var = ctk.BooleanVar(value=True)
        transaction_alerts = ctk.CTkCheckBox(
            notification_frame,
            text="Transaction Alerts",
            variable=self.transaction_alerts_var
        )
        transaction_alerts.pack(anchor="w", padx=20, pady=5)
        
        # Balance notifications
        self.balance_notifications_var = ctk.BooleanVar(value=True)
        balance_notifications = ctk.CTkCheckBox(
            notification_frame,
            text="Balance Notifications",
            variable=self.balance_notifications_var
        )
        balance_notifications.pack(anchor="w", padx=20, pady=5)
        
        # Security alerts
        self.security_alerts_var = ctk.BooleanVar(value=True)
        security_alerts = ctk.CTkCheckBox(
            notification_frame,
            text="Security Alerts",
            variable=self.security_alerts_var
        )
        security_alerts.pack(anchor="w", padx=20, pady=5)
    
    def save_settings(self):
        """Save user settings."""
        # Get the values from the input fields
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        
        # Validation
        if not first_name:
            self.show_message("First name cannot be empty", "error")
            return
            
        if not last_name:
            self.show_message("Last name cannot be empty", "error")
            return
            
        if not email:
            self.show_message("Email cannot be empty", "error")
            return
            
        if "@" not in email or "." not in email:
            self.show_message("Please enter a valid email address", "error")
            return
        
        # Update user info in database
        success = self.update_user_info(first_name, last_name, email)
        
        if success:
            self.show_message("Settings saved successfully", "success")
        
    def update_user_info(self, first_name, last_name, email):
        """Update user information in the database."""
        # Check if email has changed
        email_changed = email != self.user.email
        
        # Create a connection to execute SQL
        connection = User.get_connection()
        if not connection:
            self.show_message("Database connection error", "error")
            return False

        try:
            cursor = connection.cursor()
            
            # Check if email already exists for another user
            if email_changed:
                cursor.execute("SELECT id FROM users WHERE email = %s AND id != %s", (email, self.user.id))
                if cursor.fetchone():
                    self.show_message("Email already used by another account", "error")
                    return False
            
            # Update user information
            query = """
            UPDATE users 
            SET first_name = %s, last_name = %s, email = %s
            WHERE id = %s
            """
            cursor.execute(query, (first_name, last_name, email, self.user.id))
            connection.commit()
            
            # Update the user object
            self.user.name = f"{first_name} {last_name}"
            self.user.email = email
            
            # If email changed, update login credentials in the application
            if email_changed:
                # In a real implementation, this might involve updating session info
                # or requiring a re-login
                print(f"[INFO] User email changed from {self.user.email} to {email}")
            
            return True
            
        except Exception as e:
            self.show_message(f"Error updating user information: {str(e)}", "error")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def change_password(self):
        """Change user password."""
        current_password = self.current_pw_entry.get()
        new_password = self.new_pw_entry.get()
        confirm_password = self.confirm_pw_entry.get()
        
        if not current_password or not new_password or not confirm_password:
            self.show_message("Please fill in all password fields", "error")
            return
            
        if new_password != confirm_password:
            self.show_message("New passwords do not match", "error")
            return
            
        # In a real implementation, this would verify the current password
        # and update with the new password in the database
        
        # Clear the fields
        self.current_pw_entry.delete(0, "end")
        self.new_pw_entry.delete(0, "end")
        self.confirm_pw_entry.delete(0, "end")
        
        self.show_message("Password changed successfully", "success")
    
    def show_message(self, message, message_type="info"):
        """Show a message to the user."""
        # In a complete implementation, this would show a proper message dialog
        # For now, we just print to console with the message type
        print(f"[{message_type.upper()}] {message}") 