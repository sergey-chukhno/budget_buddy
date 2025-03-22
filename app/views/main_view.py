import customtkinter as ctk
from PIL import Image, ImageTk
import os
import sys
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import components
from app.views.dashboard_view import DashboardView
from app.views.accounts_view import AccountsView
from app.views.transactions_view import TransactionsView
from app.views.analytics_view import AnalyticsView
from app.views.dialogs.add_funds_dialog import AddFundsDialog
from app.views.dialogs.withdraw_funds_dialog import WithdrawFundsDialog
from app.views.dialogs.transfer_funds_dialog import TransferFundsDialog
from app.views.dialogs.send_funds_dialog import SendFundsDialog

class MainView(ctk.CTkFrame):
    def __init__(self, master, user, logout_callback):
        super().__init__(master)
        self.master = master
        self.user = user
        self.logout_callback = logout_callback
        
        # Configure the grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create the sidebar
        self.create_sidebar()
        
        # Create the content frame
        self.content_frame = ctk.CTkFrame(self, fg_color=("gray95", "gray10"))
        self.content_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Create the action bar at the bottom
        self.create_action_bar()
        
        # Show the dashboard view by default
        self.current_view = None
        self.show_dashboard()
        
    def create_sidebar(self):
        # Create the sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)
        
        # Load and display logo image
        self.logo_image = ctk.CTkImage(
            light_image=Image.open("resources/images/logo.png"),
            dark_image=Image.open("resources/images/logo.png"),
            size=(150, 60)  # Adjust size as needed
        )
        
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="",
            image=self.logo_image
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        
        # User info
        self.user_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.user_frame.grid(row=1, column=0, padx=20, pady=(5, 20), sticky="ew")
        
        user_name = f"{self.user.first_name} {self.user.last_name}"
        user_id = f"ID: {self.user.id}"
        user_role = "Admin" if self.user.is_admin() else "Client"
        
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
        
        # Navigation
        self.nav_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="NAVIGATION",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("gray40", "gray60")
        )
        self.nav_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")
        
        # Dashboard button
        self.dashboard_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Dashboard",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.show_dashboard
        )
        self.dashboard_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        
        # Accounts button
        self.accounts_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Accounts",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.show_accounts
        )
        self.accounts_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        
        # Transactions button
        self.transactions_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Transactions",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.show_transactions
        )
        self.transactions_button.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        
        # Analytics button
        self.analytics_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Analytics",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.show_analytics
        )
        self.analytics_button.grid(row=6, column=0, padx=10, pady=5, sticky="ew")
        
        # Logout button
        self.logout_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Logout",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.logout
        )
        self.logout_button.grid(row=8, column=0, padx=10, pady=(5, 20), sticky="ew")
        
        # Active button styling variables
        self.active_button_fg = "#3a7ebf"
        self.active_button_text = "#ffffff"
        self.active_button = None
        
    def create_action_bar(self):
        # Create the action bar frame
        self.action_bar = ctk.CTkFrame(self, height=60, corner_radius=0)
        self.action_bar.grid(row=1, column=1, sticky="sew")
        self.action_bar.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Add Funds button
        self.add_funds_button = ctk.CTkButton(
            self.action_bar,
            text="Add Funds",
            fg_color="#4CAF50",
            hover_color="#388E3C",
            command=self.show_add_funds_dialog
        )
        self.add_funds_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Withdraw Funds button
        self.withdraw_funds_button = ctk.CTkButton(
            self.action_bar,
            text="Withdraw Funds",
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=self.show_withdraw_funds_dialog
        )
        self.withdraw_funds_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Transfer Funds button
        self.transfer_funds_button = ctk.CTkButton(
            self.action_bar,
            text="Transfer Funds",
            fg_color="#2196F3",
            hover_color="#1976D2",
            command=self.show_transfer_funds_dialog
        )
        self.transfer_funds_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Send Funds button
        self.send_funds_button = ctk.CTkButton(
            self.action_bar,
            text="Send Funds",
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            command=self.show_send_funds_dialog
        )
        self.send_funds_button.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
    
    def show_dashboard(self):
        self.update_active_button(self.dashboard_button)
        self.clear_content_frame()
        self.current_view = DashboardView(self.content_frame, self.user)
        self.current_view.pack(fill="both", expand=True)
    
    def show_accounts(self):
        self.update_active_button(self.accounts_button)
        self.clear_content_frame()
        self.current_view = AccountsView(self.content_frame, self.user)
        self.current_view.pack(fill="both", expand=True)
    
    def show_transactions(self):
        self.update_active_button(self.transactions_button)
        self.clear_content_frame()
        self.current_view = TransactionsView(self.content_frame, self.user)
        self.current_view.pack(fill="both", expand=True)
    
    def show_analytics(self):
        self.update_active_button(self.analytics_button)
        self.clear_content_frame()
        self.current_view = AnalyticsView(self.content_frame, self.user)
        self.current_view.pack(fill="both", expand=True)
    
    def update_active_button(self, button):
        # Reset the previous active button
        if self.active_button:
            self.active_button.configure(
                fg_color="transparent",
                text_color=("gray10", "gray90")
            )
        
        # Set the new active button
        button.configure(
            fg_color=self.active_button_fg,
            text_color=self.active_button_text
        )
        self.active_button = button
    
    def clear_content_frame(self):
        # Destroy all widgets in the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def refresh_current_view(self):
        # Refresh the current view based on which one is active
        if self.active_button == self.dashboard_button:
            self.show_dashboard()
        elif self.active_button == self.accounts_button:
            self.show_accounts()
        elif self.active_button == self.transactions_button:
            self.show_transactions()
        elif self.active_button == self.analytics_button:
            self.show_analytics()
    
    def show_add_funds_dialog(self):
        dialog = AddFundsDialog(self, self.user)
        dialog.wait_window()
        self.refresh_current_view()
    
    def show_withdraw_funds_dialog(self):
        dialog = WithdrawFundsDialog(self, self.user)
        dialog.wait_window()
        self.refresh_current_view()
    
    def show_transfer_funds_dialog(self):
        dialog = TransferFundsDialog(self, self.user, callback=self.refresh_current_view)
        dialog.wait_window()
    
    def show_send_funds_dialog(self):
        from app.views.dialogs.send_funds_dialog import SendFundsDialog
        dialog = SendFundsDialog(self, self.user, callback=self.refresh_current_view)
        dialog.wait_window()
    
    def logout(self):
        self.logout_callback() 