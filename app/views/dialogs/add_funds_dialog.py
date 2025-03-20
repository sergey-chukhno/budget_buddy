import customtkinter as ctk
import sys
import os
from decimal import Decimal

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import models
from app.models.account import Account
from app.models.category import Category

class AddFundsDialog(ctk.CTkToplevel):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        
        # Configure the dialog
        self.title("Add Funds")
        self.geometry("500x550")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(master)
        self.grab_set()
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Dialog title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Add Funds",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # Account selection section
        self.account_frame = ctk.CTkFrame(self.main_frame)
        self.account_frame.pack(fill="x", padx=10, pady=10)
        
        self.account_label = ctk.CTkLabel(
            self.account_frame,
            text="Account",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.account_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Get user accounts
        self.accounts = Account.get_accounts_for_user(self.user.id)
        
        if not self.accounts:
            self.account_options = ["No accounts available"]
            self.selected_account = None
        else:
            self.account_options = [f"{account.account_name} (${account.balance:,.2f})" for account in self.accounts]
            self.selected_account = self.accounts[0] if self.accounts else None
        
        self.account_dropdown = ctk.CTkOptionMenu(
            self.account_frame,
            values=self.account_options,
            command=self.on_account_selected,
            width=300
        )
        self.account_dropdown.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Amount section
        self.amount_frame = ctk.CTkFrame(self.main_frame)
        self.amount_frame.pack(fill="x", padx=10, pady=10)
        
        self.amount_label = ctk.CTkLabel(
            self.amount_frame,
            text="Amount",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.amount_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.amount_entry = ctk.CTkEntry(
            self.amount_frame,
            placeholder_text="Enter amount",
            width=300
        )
        self.amount_entry.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Category section
        self.category_frame = ctk.CTkFrame(self.main_frame)
        self.category_frame.pack(fill="x", padx=10, pady=10)
        
        self.category_label = ctk.CTkLabel(
            self.category_frame,
            text="Category",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.category_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Get income categories
        self.categories = Category.get_all_categories(is_expense=False)
        
        if not self.categories:
            self.category_options = ["No categories available"]
            self.selected_category = None
        else:
            self.category_options = [category.category_name for category in self.categories]
            self.selected_category = self.categories[0] if self.categories else None
        
        self.category_dropdown = ctk.CTkOptionMenu(
            self.category_frame,
            values=self.category_options,
            command=self.on_category_selected,
            width=300
        )
        self.category_dropdown.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Description section
        self.description_frame = ctk.CTkFrame(self.main_frame)
        self.description_frame.pack(fill="x", padx=10, pady=10)
        
        self.description_label = ctk.CTkLabel(
            self.description_frame,
            text="Description",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.description_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.description_entry = ctk.CTkEntry(
            self.description_frame,
            placeholder_text="Enter description (optional)",
            width=300
        )
        self.description_entry.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Error message label
        self.error_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            text_color="red",
            font=ctk.CTkFont(size=12)
        )
        self.error_label.pack(pady=(5, 10))
        
        # Buttons
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        self.cancel_button = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90")
        )
        self.cancel_button.pack(side="left", padx=10)
        
        self.add_button = ctk.CTkButton(
            self.buttons_frame,
            text="Add Funds",
            command=self.add_funds,
            fg_color="#4CAF50",
            hover_color="#388E3C"
        )
        self.add_button.pack(side="right", padx=10)
    
    def on_account_selected(self, selection):
        """Handle account selection."""
        if not self.accounts:
            return
            
        for account in self.accounts:
            if f"{account.account_name} (${account.balance:,.2f})" == selection:
                self.selected_account = account
                break
    
    def on_category_selected(self, selection):
        """Handle category selection."""
        if not self.categories:
            return
            
        for category in self.categories:
            if category.category_name == selection:
                self.selected_category = category
                break
    
    def validate_amount(self, amount_str):
        """Validate the amount input."""
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                return False, "Amount must be positive"
            return True, amount
        except (ValueError, InvalidOperation):
            return False, "Please enter a valid amount"
    
    def add_funds(self):
        """Process adding funds to the account."""
        # Check if account is selected
        if not self.selected_account:
            self.error_label.configure(text="Please select an account")
            return
            
        # Check if category is selected
        if not self.selected_category:
            self.error_label.configure(text="Please select a category")
            return
            
        # Validate amount
        amount_str = self.amount_entry.get()
        valid, result = self.validate_amount(amount_str)
        if not valid:
            self.error_label.configure(text=result)
            return
            
        amount = result
        
        # Get description
        description = self.description_entry.get() or "Deposit"
        
        # Add funds to the account
        success, message = self.selected_account.add_funds(
            float(amount),
            self.selected_category.id,
            description,
            self.user.id
        )
        
        if success:
            self.destroy()  # Close the dialog on success
        else:
            self.error_label.configure(text=message) 