import customtkinter as ctk
import sys
import os
from PIL import Image

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import admin views
from app.views.admin_dashboard_view import AdminDashboardView
from app.views.admin_clients_view import AdminClientsView
from app.views.admin_accounts_view import AdminAccountsView
from app.views.admin_transactions_view import AdminTransactionsView
from app.views.admin_settings_view import AdminSettingsView

class AdminView(ctk.CTkFrame):
    def __init__(self, master, user, show_dashboard=True):
        super().__init__(master)
        self.master = master
        self.user = user
        
        # Configure the grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create the sidebar
        self.sidebar_frame = self.create_sidebar()
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Initialize views dictionary
        self.views = {}
        
        # Create the admin views
        self.create_views()
        
        # Show the dashboard by default
        if show_dashboard:
            self.show_view("dashboard")
    
    def create_sidebar(self):
        # Create sidebar frame
        sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar_frame.grid_rowconfigure(8, weight=1)  # Push logout button to the bottom
        
        # Logo
        image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "resources", "images", "logo.png")
        
        try:
            # Load and prepare the logo image
            logo_img = Image.open(image_path)
            
            # Make the logo circular by creating a circular mask
            # Resize to a square first
            size = min(logo_img.width, logo_img.height)
            logo_img = logo_img.resize((size, size))
            
            # Create a circular mask
            mask = Image.new('L', (size, size), 0)
            from PIL import ImageDraw
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)
            
            # Create a new image with transparent background
            circular_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            circular_img.paste(logo_img, (0, 0), mask)
            
            # Create CTkImage
            logo = ctk.CTkImage(light_image=circular_img, dark_image=circular_img, size=(120, 120))
            
            logo_label = ctk.CTkLabel(sidebar_frame, image=logo, text="")
            logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        except Exception as e:
            print(f"Error loading logo: {e}")
            # Fallback if logo image is not found
            logo_label = ctk.CTkLabel(sidebar_frame, text="Admin Panel", font=ctk.CTkFont(size=20, weight="bold"))
            logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # User info frame
        user_frame = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
        user_frame.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        # User name
        user_name_label = ctk.CTkLabel(
            user_frame, 
            text=f"{self.user.first_name} {self.user.last_name}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        user_name_label.pack(anchor="w")
        
        # User ID
        user_id_label = ctk.CTkLabel(
            user_frame, 
            text=f"ID: {self.user.id}",
            font=ctk.CTkFont(size=12)
        )
        user_id_label.pack(anchor="w")
        
        # Role label
        role_label = ctk.CTkLabel(
            user_frame,
            text="Administrator",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#FF9800"
        )
        role_label.pack(anchor="w")
        
        # Navigation title
        nav_label = ctk.CTkLabel(sidebar_frame, text="NAVIGATION", font=ctk.CTkFont(size=12, weight="bold"))
        nav_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="w")
        
        # Navigation buttons - arranged together
        self.dashboard_button = ctk.CTkButton(
            sidebar_frame, 
            text="Dashboard",
            fg_color="transparent", 
            font=ctk.CTkFont(size=13),
            anchor="w",
            command=lambda: self.show_view("dashboard")
        )
        self.dashboard_button.grid(row=3, column=0, padx=(15, 10), pady=(5, 0), sticky="ew")
        
        self.clients_button = ctk.CTkButton(
            sidebar_frame, 
            text="Clients",
            fg_color="transparent", 
            font=ctk.CTkFont(size=13),
            anchor="w",
            command=lambda: self.show_view("clients")
        )
        self.clients_button.grid(row=4, column=0, padx=(15, 10), pady=(5, 0), sticky="ew")
        
        self.accounts_button = ctk.CTkButton(
            sidebar_frame, 
            text="Accounts",
            fg_color="transparent", 
            font=ctk.CTkFont(size=13),
            anchor="w",
            command=lambda: self.show_view("accounts")
        )
        self.accounts_button.grid(row=5, column=0, padx=(15, 10), pady=(5, 0), sticky="ew")
        
        # Moved up to be with other navigation buttons
        self.transactions_button = ctk.CTkButton(
            sidebar_frame, 
            text="Transactions",
            fg_color="transparent", 
            font=ctk.CTkFont(size=13),
            anchor="w",
            command=lambda: self.show_view("transactions")
        )
        self.transactions_button.grid(row=6, column=0, padx=(15, 10), pady=(5, 0), sticky="ew")
        
        # Moved up to be with other navigation buttons
        self.settings_button = ctk.CTkButton(
            sidebar_frame, 
            text="Settings",
            fg_color="transparent", 
            font=ctk.CTkFont(size=13),
            anchor="w",
            command=lambda: self.show_view("settings")
        )
        self.settings_button.grid(row=7, column=0, padx=(15, 10), pady=(5, 0), sticky="ew")
        
        # Logout button (at the bottom)
        self.logout_button = ctk.CTkButton(
            sidebar_frame, 
            text="Logout",
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=self.logout
        )
        self.logout_button.grid(row=9, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        return sidebar_frame
    
    def create_views(self):
        # Create all the admin views
        self.views["dashboard"] = AdminDashboardView(self, self.user)
        self.views["clients"] = AdminClientsView(self, self.user)
        self.views["accounts"] = AdminAccountsView(self, self.user)
        self.views["transactions"] = AdminTransactionsView(self, self.user)
        self.views["settings"] = AdminSettingsView(self, self.user)
        
        # Grid but do not show the views yet
        for view in self.views.values():
            view.grid(row=0, column=1, sticky="nsew")
            view.grid_remove()
    
    def show_view(self, view_name):
        # Reset button colors
        for button in [self.dashboard_button, self.clients_button, self.accounts_button, 
                      self.transactions_button, self.settings_button]:
            button.configure(fg_color="transparent")
        
        # Highlight the selected button
        if view_name == "dashboard":
            self.dashboard_button.configure(fg_color=("gray75", "gray28"))
        elif view_name == "clients":
            self.clients_button.configure(fg_color=("gray75", "gray28"))
        elif view_name == "accounts":
            self.accounts_button.configure(fg_color=("gray75", "gray28"))
        elif view_name == "transactions":
            self.transactions_button.configure(fg_color=("gray75", "gray28"))
        elif view_name == "settings":
            self.settings_button.configure(fg_color=("gray75", "gray28"))
        
        # Hide all views
        for view in self.views.values():
            view.grid_remove()
        
        # Show the selected view
        if view_name in self.views:
            self.views[view_name].grid()
            self.current_view = view_name
    
    def refresh_current_view(self):
        """Refresh the current view if needed"""
        # This method can be called to refresh data in the current view
        if hasattr(self, "current_view") and self.current_view in self.views:
            if hasattr(self.views[self.current_view], "refresh"):
                self.views[self.current_view].refresh()
    
    def logout(self):
        """Logout the user"""
        if hasattr(self.master, "handle_logout"):
            self.master.handle_logout() 