import customtkinter as ctk
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import views
from app.views.login_view import LoginView
from app.views.register_view import RegisterView
from app.views.dashboard_view import DashboardView
from app.views.accounts_view import AccountsView
from app.views.transactions_view import TransactionsView
from app.views.categories_view import CategoriesView
from app.views.analytics_view import AnalyticsView
from app.views.settings_view import SettingsView

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
            "categories": CategoriesView,
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
        # Here we would normally authenticate against a database
        # For now, just create a test user
        self.current_user = User(1, "John Doe", email, "password_hash")
        
        # Now show the main application with sidebar
        self.create_sidebar()
        self.show_view("dashboard")
        
        return True, "Login successful"

    def handle_registration(self, email, password, first_name, last_name, phone, address):
        """Handle registration of a new user."""
        # Here we would normally save to a database
        # For now, just create the user and log them in
        self.current_user = User(1, first_name + " " + last_name, email, "password_hash")
        
        # Create sidebar and show dashboard
        self.create_sidebar()
        self.show_view("dashboard")
        
        return True, "Registration successful"

    def create_sidebar(self):
        """Create the sidebar with navigation buttons."""
        if self.sidebar:
            self.sidebar.destroy()

        # Create sidebar frame
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)  # Push logout to bottom
        
        # App logo/title
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="Budget Buddy",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Navigation buttons
        self.dashboard_btn = self.create_nav_button("Dashboard", 1, "dashboard")
        self.accounts_btn = self.create_nav_button("Accounts", 2, "accounts")
        self.transactions_btn = self.create_nav_button("Transactions", 3, "transactions")
        self.categories_btn = self.create_nav_button("Categories", 4, "categories")
        self.analytics_btn = self.create_nav_button("Analytics", 5, "analytics")
        
        # Settings button
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
            "categories": self.categories_btn,
            "analytics": self.analytics_btn,
            "settings": self.settings_btn
        }
        
        # Set inactive style
        for name, button in all_buttons.items():
            button.configure(fg_color="transparent")
            
        # Set active style for current view
        if active_view in all_buttons:
            all_buttons[active_view].configure(fg_color=("gray75", "gray28"))

    def clear_current_view(self):
        """Clear the current view if it exists."""
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