import customtkinter as ctk
import sys
import os
from PIL import Image, ImageDraw

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import views
from app.views.login_view import LoginView
from app.views.register_view import RegisterView
from app.views.dashboard_view import DashboardView
from app.views.accounts_view import AccountsView
from app.views.transactions_view import TransactionsView
from app.views.analytics_view import AnalyticsView
from app.views.settings_view import SettingsView
from app.views.admin_view import AdminView

# Import models
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.category import Category

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set appearance mode (optional)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure window
        self.title("Billionnaires Budget Buddy")
        self.geometry("1200x800")
        self.minsize(800, 600)

        # Set up grid layout for the window
        self.grid_columnconfigure(1, weight=1)  # Content column takes extra space
        self.grid_rowconfigure(0, weight=1)     # Make the content expand

        # Initialize class variables
        self.current_user = None
        self.current_view = None
        self.sidebar = None
        
        # Dictionary to map view names to view classes
        self.views = {
            "dashboard": DashboardView,
            "accounts": AccountsView,
            "transactions": TransactionsView,
            "analytics": AnalyticsView,
            "settings": SettingsView
        }

        # Start with login view
        self.show_login()

    def show_login(self):
        """Show the login view."""
        self.clear_current_view()
        self.current_view = LoginView(self, login_callback=self.handle_login, register_callback=self.show_register)
        self.current_view.grid(row=0, column=0, sticky="nsew", columnspan=2)

    def show_register(self):
        """Show the registration view."""
        self.clear_current_view()
        self.current_view = RegisterView(self, back_callback=self.show_login, register_callback=self.handle_registration)
        self.current_view.grid(row=0, column=0, sticky="nsew", columnspan=2)

    def handle_login(self, email, password):
        """Handle login attempt."""
        # Use the User model to authenticate against the database
        success, result = User.authenticate(email, password)
        
        if success:
            # Store the user object
            self.current_user = result
            
            # Check if the user is an admin
            if self.current_user.is_admin():
                # Show the admin interface
                self.show_admin_interface()
            else:
                # Show the client interface
                self.create_sidebar()
                self.show_view("dashboard")
            
            return True, "Login successful"
        else:
            # Return the error message from authentication
            return False, result

    def handle_registration(self, email, password, first_name, last_name, phone, address):
        """Handle registration of a new user."""
        # Use the User model to create a new user in the database
        success, result = User.create_user(email, password, first_name, last_name, phone, address)
        
        if success:
            # Store the user object
            self.current_user = result
            
            # Create sidebar and show dashboard (clients only)
            self.create_sidebar()
            self.show_view("dashboard")
            
            return True, "Registration successful"
        else:
            # Return the error message from user creation
            return False, result
            
    def show_admin_interface(self):
        """Show the admin interface."""
        self.clear_current_view()
        
        # Create the admin view
        self.current_view = AdminView(self, self.current_user)
        self.current_view.grid(row=0, column=0, sticky="nsew", columnspan=2)

    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        if self.sidebar:
            self.sidebar.destroy()

        # Create sidebar frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)  # Push logout to bottom
        
        # Load and display logo image
        original_logo = Image.open("resources/images/logo.png")
        
        # Create a circular mask
        width, height = original_logo.size
        size = min(width, height)
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0, width, height), fill=255)
        
        # Apply circular mask to logo
        circular_logo = original_logo.copy()
        circular_logo.putalpha(mask)
        
        self.logo_image = ctk.CTkImage(
            light_image=circular_logo,
            dark_image=circular_logo,
            size=(180, 180)  # Make it square for circular appearance
        )
        
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="",
            image=self.logo_image,
            corner_radius=90  # Half the width/height for circular appearance
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        # User info frame
        self.user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.user_frame.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # Display user information
        if self.current_user:
            user_name = f"{self.current_user.first_name} {self.current_user.last_name}"
            user_id = f"ID: {self.current_user.id}"
            user_role = "Admin" if self.current_user.is_admin() else "Client"
            
            self.user_name_label = ctk.CTkLabel(
                self.user_frame,
                text=user_name,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            self.user_name_label.grid(row=0, column=0, sticky="w")
            
            self.user_id_label = ctk.CTkLabel(
                self.user_frame,
                text=user_id,
                text_color=("gray50", "gray70"),
                font=ctk.CTkFont(size=12)
            )
            self.user_id_label.grid(row=1, column=0, sticky="w")
            
            self.user_role_label = ctk.CTkLabel(
                self.user_frame,
                text=user_role,
                text_color=("gray50", "gray70"),
                font=ctk.CTkFont(size=12)
            )
            self.user_role_label.grid(row=2, column=0, sticky="w")

        # Navigation buttons
        self.dashboard_btn = self.create_nav_button("Dashboard", 2, "dashboard")
        self.accounts_btn = self.create_nav_button("Accounts", 3, "accounts")
        self.transactions_btn = self.create_nav_button("Transactions", 4, "transactions")
        self.analytics_btn = self.create_nav_button("Analytics", 5, "analytics")
        self.settings_btn = self.create_nav_button("Settings", 6, "settings")
        
        # Logout button
        self.logout_btn = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.handle_logout
        )
        self.logout_btn.grid(row=8, column=0, padx=20, pady=20, sticky="ew")

    def create_nav_button(self, text, row, view_name):
        """Create a navigation button for the sidebar."""
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            fg_color="transparent",
            text_color=("gray10", "#DCE4EE"),
            anchor="w",
            command=lambda: self.show_view(view_name)
        )
        button.grid(row=row, column=0, padx=20, pady=10, sticky="ew")
        return button

    def show_view(self, view_name):
        """Show the specified view and update active button."""
        self.clear_current_view()
        
        # Create and display the requested view
        if view_name in self.views:
            view_class = self.views[view_name]
            self.current_view = view_class(self, self.current_user)
            self.current_view.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
            
            # Update active button
            self.update_active_button(view_name)

    def update_active_button(self, active_view):
        """Update the active button in the sidebar."""
        # Reset all buttons
        all_buttons = {
            "dashboard": self.dashboard_btn,
            "accounts": self.accounts_btn,
            "transactions": self.transactions_btn,
            "analytics": self.analytics_btn,
            "settings": self.settings_btn
        }
        
        # Reset all buttons
        for button in all_buttons.values():
            button.configure(
                fg_color="transparent",
                text_color=("gray10", "#DCE4EE")
            )
        
        # Set active button
        if active_view in all_buttons:
            all_buttons[active_view].configure(
                fg_color=("gray70", "gray25"),
                text_color=("gray10", "#DCE4EE")
            )

    def clear_current_view(self):
        """Clear the current view."""
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

    def handle_logout(self):
        """Handle user logout."""
        # Clear user data
        self.current_user = None
        
        # Remove sidebar
        if self.sidebar:
            self.sidebar.destroy()
            self.sidebar = None
        
        # Show login screen
        self.show_login()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop() 