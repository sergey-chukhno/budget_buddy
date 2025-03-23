import customtkinter as ctk
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.user import User

class AdminSettingsView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.user = user
        
        # Set up grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Admin Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", anchor="w")
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Create tabs
        self.create_tabs()
    
    def create_tabs(self):
        # Tab view for different settings categories
        self.tabview = ctk.CTkTabview(self.content_frame, width=250)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        self.tabview.add("Account")
        self.tabview.add("System")
        self.tabview.add("Notifications")
        self.tabview.add("Security")
        
        # Set default tab
        self.tabview.set("Account")
        
        # Fill tabs with content
        self.setup_account_tab()
        self.setup_system_tab()
        self.setup_notifications_tab()
        self.setup_security_tab()
    
    def setup_account_tab(self):
        tab = self.tabview.tab("Account")
        tab.grid_columnconfigure(0, weight=1)
        
        # Admin profile information
        profile_frame = ctk.CTkFrame(tab)
        profile_frame.pack(fill="x", padx=10, pady=(10, 20))
        profile_frame.grid_columnconfigure(1, weight=1)
        
        # Profile heading
        profile_heading = ctk.CTkLabel(
            profile_frame,
            text="Admin Profile",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        profile_heading.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 15))
        
        # Fields
        fields = [
            ("First Name", self.user.first_name),
            ("Last Name", self.user.last_name),
            ("Email", self.user.email),
            ("Role", "Admin"),
            ("ID", str(self.user.id))
        ]
        
        for i, (field_name, field_value) in enumerate(fields):
            label = ctk.CTkLabel(
                profile_frame,
                text=f"{field_name}:",
                font=ctk.CTkFont(size=14),
                anchor="e"
            )
            label.grid(row=i+1, column=0, sticky="e", padx=(10, 5), pady=5)
            
            value = ctk.CTkLabel(
                profile_frame,
                text=field_value,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            value.grid(row=i+1, column=1, sticky="w", padx=5, pady=5)
        
        # Edit profile button
        edit_btn = ctk.CTkButton(
            profile_frame,
            text="Edit Profile",
            command=self.edit_profile
        )
        edit_btn.grid(row=len(fields)+1, column=0, columnspan=2, sticky="w", padx=10, pady=(15, 10))
        
        # Change password section
        password_frame = ctk.CTkFrame(tab)
        password_frame.pack(fill="x", padx=10, pady=10)
        
        # Password heading
        password_heading = ctk.CTkLabel(
            password_frame,
            text="Change Password",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        password_heading.pack(anchor="w", padx=10, pady=(10, 15))
        
        # Current password
        current_pw_label = ctk.CTkLabel(
            password_frame,
            text="Current Password:",
            font=ctk.CTkFont(size=14)
        )
        current_pw_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.current_pw_entry = ctk.CTkEntry(
            password_frame,
            width=300,
            show="•"
        )
        self.current_pw_entry.pack(anchor="w", padx=10, pady=(0, 10))
        
        # New password
        new_pw_label = ctk.CTkLabel(
            password_frame,
            text="New Password:",
            font=ctk.CTkFont(size=14)
        )
        new_pw_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.new_pw_entry = ctk.CTkEntry(
            password_frame,
            width=300,
            show="•"
        )
        self.new_pw_entry.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Confirm new password
        confirm_pw_label = ctk.CTkLabel(
            password_frame,
            text="Confirm New Password:",
            font=ctk.CTkFont(size=14)
        )
        confirm_pw_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        self.confirm_pw_entry = ctk.CTkEntry(
            password_frame,
            width=300,
            show="•"
        )
        self.confirm_pw_entry.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Change password button
        change_pw_btn = ctk.CTkButton(
            password_frame,
            text="Change Password",
            command=self.change_password
        )
        change_pw_btn.pack(anchor="w", padx=10, pady=(5, 15))
    
    def setup_system_tab(self):
        tab = self.tabview.tab("System")
        
        # General settings frame
        general_frame = ctk.CTkFrame(tab)
        general_frame.pack(fill="x", padx=10, pady=(10, 20))
        
        # Section heading
        general_heading = ctk.CTkLabel(
            general_frame,
            text="System Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        general_heading.pack(anchor="w", padx=10, pady=(10, 15))
        
        # Theme selection
        theme_frame = ctk.CTkFrame(general_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=10, pady=5)
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="App Theme:",
            font=ctk.CTkFont(size=14)
        )
        theme_label.pack(side="left", padx=(0, 10))
        
        self.theme_var = ctk.StringVar(value="System")
        theme_combobox = ctk.CTkComboBox(
            theme_frame,
            values=["System", "Light", "Dark"],
            variable=self.theme_var,
            width=150,
            command=self.change_theme
        )
        theme_combobox.pack(side="left")
        
        # Backup & Export
        backup_frame = ctk.CTkFrame(tab)
        backup_frame.pack(fill="x", padx=10, pady=10)
        
        # Section heading
        backup_heading = ctk.CTkLabel(
            backup_frame,
            text="Backup & Export",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        backup_heading.pack(anchor="w", padx=10, pady=(10, 15))
        
        # Backup button
        backup_btn = ctk.CTkButton(
            backup_frame,
            text="Backup System Data",
            width=200,
            command=self.backup_data
        )
        backup_btn.pack(anchor="w", padx=10, pady=5)
        
        # Export clients data
        export_clients_btn = ctk.CTkButton(
            backup_frame,
            text="Export Clients Data",
            width=200,
            command=self.export_clients_data
        )
        export_clients_btn.pack(anchor="w", padx=10, pady=5)
        
        # Export transactions data
        export_transactions_btn = ctk.CTkButton(
            backup_frame,
            text="Export Transactions Data",
            width=200,
            command=self.export_transactions_data
        )
        export_transactions_btn.pack(anchor="w", padx=10, pady=5)
        
        # System maintenance
        maintenance_frame = ctk.CTkFrame(tab)
        maintenance_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        # Section heading
        maintenance_heading = ctk.CTkLabel(
            maintenance_frame,
            text="System Maintenance",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        maintenance_heading.pack(anchor="w", padx=10, pady=(10, 15))
        
        # Maintenance buttons
        clear_cache_btn = ctk.CTkButton(
            maintenance_frame,
            text="Clear System Cache",
            width=200,
            fg_color="#FF9800",
            hover_color="#F57C00",
            command=self.clear_cache
        )
        clear_cache_btn.pack(anchor="w", padx=10, pady=5)
        
        db_optimize_btn = ctk.CTkButton(
            maintenance_frame,
            text="Optimize Database",
            width=200,
            fg_color="#2196F3",
            hover_color="#1976D2",
            command=self.optimize_database
        )
        db_optimize_btn.pack(anchor="w", padx=10, pady=5)
    
    def setup_notifications_tab(self):
        tab = self.tabview.tab("Notifications")
        
        # Admin notifications
        notifications_frame = ctk.CTkFrame(tab)
        notifications_frame.pack(fill="x", padx=10, pady=(10, 20))
        
        # Section heading
        notifications_heading = ctk.CTkLabel(
            notifications_frame,
            text="Notification Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        notifications_heading.pack(anchor="w", padx=10, pady=(10, 15))
        
        # Notification options
        options = [
            ("New Client Registrations", True),
            ("Large Transactions (>$10,000)", True),
            ("Suspicious Activity Alerts", True),
            ("System Updates", False),
            ("Client Account Changes", False)
        ]
        
        for i, (option_text, default_state) in enumerate(options):
            option_var = ctk.BooleanVar(value=default_state)
            option_check = ctk.CTkCheckBox(
                notifications_frame,
                text=option_text,
                variable=option_var,
                command=lambda opt=option_text: self.toggle_notification(opt)
            )
            option_check.pack(anchor="w", padx=10, pady=5)
        
        # Email notifications
        email_frame = ctk.CTkFrame(tab)
        email_frame.pack(fill="x", padx=10, pady=10)
        
        # Section heading
        email_heading = ctk.CTkLabel(
            email_frame,
            text="Email Notifications",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        email_heading.pack(anchor="w", padx=10, pady=(10, 15))
        
        # Email settings
        email_var = ctk.BooleanVar(value=True)
        email_check = ctk.CTkCheckBox(
            email_frame,
            text="Send Notifications to Email",
            variable=email_var,
            command=self.toggle_email_notifications
        )
        email_check.pack(anchor="w", padx=10, pady=5)
        
        # Email address
        email_label = ctk.CTkLabel(
            email_frame,
            text="Notification Email:",
            font=ctk.CTkFont(size=14)
        )
        email_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.email_entry = ctk.CTkEntry(
            email_frame,
            width=300,
            placeholder_text=self.user.email
        )
        self.email_entry.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Save email button
        save_email_btn = ctk.CTkButton(
            email_frame,
            text="Update Email",
            command=self.update_notification_email
        )
        save_email_btn.pack(anchor="w", padx=10, pady=(5, 15))
    
    def setup_security_tab(self):
        tab = self.tabview.tab("Security")
        
        # Security settings
        security_frame = ctk.CTkFrame(tab)
        security_frame.pack(fill="x", padx=10, pady=(10, 20))
        
        # Section heading
        security_heading = ctk.CTkLabel(
            security_frame,
            text="Security Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        security_heading.pack(anchor="w", padx=10, pady=(10, 15))
        
        # Two-factor authentication
        twofa_var = ctk.BooleanVar(value=False)
        twofa_check = ctk.CTkCheckBox(
            security_frame,
            text="Enable Two-Factor Authentication",
            variable=twofa_var,
            command=self.toggle_twofa
        )
        twofa_check.pack(anchor="w", padx=10, pady=5)
        
        # Setup 2FA button
        setup_twofa_btn = ctk.CTkButton(
            security_frame,
            text="Setup Two-Factor Authentication",
            width=250,
            state="disabled",  # Enable when 2FA is toggled on
            command=self.setup_twofa
        )
        setup_twofa_btn.pack(anchor="w", padx=10, pady=(5, 15))
        
        # Session settings
        session_frame = ctk.CTkFrame(tab)
        session_frame.pack(fill="x", padx=10, pady=10)
        
        # Section heading
        session_heading = ctk.CTkLabel(
            session_frame,
            text="Session Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        session_heading.pack(anchor="w", padx=10, pady=(10, 15))
        
        # Auto logout after inactivity
        logout_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
        logout_frame.pack(fill="x", padx=10, pady=5)
        
        logout_label = ctk.CTkLabel(
            logout_frame,
            text="Auto Logout After:",
            font=ctk.CTkFont(size=14)
        )
        logout_label.pack(side="left", padx=(0, 10))
        
        self.logout_var = ctk.StringVar(value="30 minutes")
        logout_combobox = ctk.CTkComboBox(
            logout_frame,
            values=["10 minutes", "30 minutes", "1 hour", "4 hours", "Never"],
            variable=self.logout_var,
            width=150,
            command=self.set_logout_time
        )
        logout_combobox.pack(side="left")
        
        # Active sessions management
        sessions_btn = ctk.CTkButton(
            session_frame,
            text="Manage Active Sessions",
            width=200,
            command=self.manage_sessions
        )
        sessions_btn.pack(anchor="w", padx=10, pady=(15, 10))
        
        # Audit log
        audit_frame = ctk.CTkFrame(tab)
        audit_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        # Section heading
        audit_heading = ctk.CTkLabel(
            audit_frame,
            text="Security Audit",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        audit_heading.pack(anchor="w", padx=10, pady=(10, 15))
        
        # View audit log button
        audit_btn = ctk.CTkButton(
            audit_frame,
            text="View Security Audit Log",
            width=200,
            command=self.view_audit_log
        )
        audit_btn.pack(anchor="w", padx=10, pady=(5, 15))
    
    # Event handlers
    def edit_profile(self):
        print("Editing admin profile...")
    
    def change_password(self):
        current_pw = self.current_pw_entry.get()
        new_pw = self.new_pw_entry.get()
        confirm_pw = self.confirm_pw_entry.get()
        
        if not current_pw or not new_pw or not confirm_pw:
            print("All password fields are required")
            return
        
        if new_pw != confirm_pw:
            print("New passwords do not match")
            return
        
        # Here we would verify the current password and update
        print("Changing password...")
    
    def change_theme(self, theme):
        print(f"Changing theme to: {theme}")
        # Here we would update the app theme
    
    def backup_data(self):
        print("Backing up system data...")
    
    def export_clients_data(self):
        print("Exporting clients data...")
    
    def export_transactions_data(self):
        print("Exporting transactions data...")
    
    def clear_cache(self):
        print("Clearing system cache...")
    
    def optimize_database(self):
        print("Optimizing database...")
    
    def toggle_notification(self, option):
        print(f"Toggling notification for: {option}")
    
    def toggle_email_notifications(self):
        print("Toggling email notifications")
    
    def update_notification_email(self):
        email = self.email_entry.get()
        if not email:
            email = self.user.email
        
        print(f"Updating notification email to: {email}")
    
    def toggle_twofa(self):
        print("Toggling two-factor authentication")
    
    def setup_twofa(self):
        print("Setting up two-factor authentication...")
    
    def set_logout_time(self, time):
        print(f"Setting auto logout time to: {time}")
    
    def manage_sessions(self):
        print("Managing active sessions...")
    
    def view_audit_log(self):
        print("Viewing security audit log...") 