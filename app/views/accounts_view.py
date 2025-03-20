import customtkinter as ctk
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.account import Account
from app.views.dialogs.add_account_dialog import AddAccountDialog

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
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Create scrollable frame for accounts
        self.accounts_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.accounts_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.accounts_frame.grid_columnconfigure(0, weight=1)
        
        # Load and display accounts
        self.load_accounts()
    
    def load_accounts(self):
        """Load and display all accounts for the user."""
        # Clear existing account cards
        for widget in self.accounts_frame.winfo_children():
            widget.destroy()
        
        # Get accounts from the database
        accounts = Account.get_accounts_for_user(self.user.id)
        
        if not accounts:
            # No accounts found, show a message
            self.no_accounts_label = ctk.CTkLabel(
                self.accounts_frame,
                text="You don't have any accounts yet. Click 'Add Account' to create one.",
                font=ctk.CTkFont(size=14),
                wraplength=600
            )
            self.no_accounts_label.grid(row=0, column=0, padx=20, pady=100)
        else:
            # Display each account as a card
            for i, account in enumerate(accounts):
                self.create_account_card(account, i)
    
    def create_account_card(self, account, row):
        """Create a card for an account."""
        # Card frame
        card = ctk.CTkFrame(self.accounts_frame)
        card.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
        card.grid_columnconfigure(1, weight=1)
        
        # Account type label (left side)
        type_label = ctk.CTkLabel(
            card,
            text=account.account_type_name,
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray70")
        )
        type_label.grid(row=0, column=0, padx=15, pady=(15, 0), sticky="w")
        
        # Account name
        name_label = ctk.CTkLabel(
            card,
            text=account.account_name,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.grid(row=1, column=0, padx=15, pady=(0, 0), sticky="w")
        
        # Account number
        number_label = ctk.CTkLabel(
            card,
            text=account.account_number,
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray70")
        )
        number_label.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="w")
        
        # Balance (right side)
        balance_label = ctk.CTkLabel(
            card,
            text=f"${account.balance:,.2f}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        balance_label.grid(row=0, column=1, rowspan=3, padx=15, pady=15, sticky="e")
        
        # Add action buttons
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.grid(row=3, column=0, columnspan=2, padx=15, pady=(0, 15), sticky="ew")
        
        # View button
        view_btn = ctk.CTkButton(
            actions_frame, 
            text="View",
            width=70,
            command=lambda a=account: self.view_account(a)
        )
        view_btn.pack(side="left", padx=5)
        
        # Edit button
        edit_btn = ctk.CTkButton(
            actions_frame, 
            text="Edit",
            width=70,
            command=lambda a=account: self.edit_account(a)
        )
        edit_btn.pack(side="left", padx=5)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            actions_frame, 
            text="Delete",
            width=70,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=lambda a=account: self.delete_account(a)
        )
        delete_btn.pack(side="left", padx=5)
    
    def add_account(self):
        """Show dialog to add a new account."""
        AddAccountDialog(self, self.user, callback=self.load_accounts)
    
    def view_account(self, account):
        """View account details."""
        print(f"Viewing account {account.account_name}")
        # This would open a detailed view of the account with transaction history
    
    def edit_account(self, account):
        """Edit an account."""
        print(f"Editing account {account.account_name}")
        # This would open a dialog to edit the account
    
    def delete_account(self, account):
        """Delete an account."""
        # Confirm deletion
        confirm = ctk.CTkInputDialog(
            title="Confirm Deletion",
            text=f"Are you sure you want to delete the account '{account.account_name}'?\nType 'DELETE' to confirm."
        )
        result = confirm.get_input()
        
        if result == "DELETE":
            success, message = Account.delete_account(account.id)
            if success:
                self.load_accounts()
            else:
                print(f"Error deleting account: {message}")
                # Show error message dialog 