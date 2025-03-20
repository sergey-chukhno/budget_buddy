import customtkinter as ctk
from decimal import Decimal
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import models
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.category import Category

class AddFundsDialog(ctk.CTkToplevel):
    def __init__(self, parent, user, callback=None):
        super().__init__(parent)
        
        self.parent = parent
        self.user = user
        self.callback = callback
        
        # Set up the dialog window
        self.title("Add Funds")
        self.geometry("400x600")  # Increased height to show all content
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create the dialog content
        self.create_widgets()
        
        # Make dialog modal and focus it
        self.focus_set()
        
        # Handle window close button
        self.protocol("WM_DELETE_WINDOW", self.close)
    
    def create_widgets(self):
        """Create the dialog widgets."""
        # Main container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="Add Funds to Account",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Account selection
        account_frame = ctk.CTkFrame(container, fg_color="transparent")
        account_frame.pack(fill="x", pady=(0, 10))
        
        account_label = ctk.CTkLabel(
            account_frame,
            text="Select Account:",
            font=ctk.CTkFont(size=14)
        )
        account_label.pack(anchor="w")
        
        # Get user's accounts
        self.accounts = Account.get_accounts_for_user(self.user.id)
        self.account_var = ctk.StringVar()
        
        self.account_menu = ctk.CTkOptionMenu(
            account_frame,
            values=[f"{acc.account_name} (${acc.balance:,.2f})" for acc in self.accounts],
            variable=self.account_var,
            width=300
        )
        self.account_menu.pack(pady=(5, 0))
        
        # Amount input
        amount_frame = ctk.CTkFrame(container, fg_color="transparent")
        amount_frame.pack(fill="x", pady=(0, 10))
        
        amount_label = ctk.CTkLabel(
            amount_frame,
            text="Amount:",
            font=ctk.CTkFont(size=14)
        )
        amount_label.pack(anchor="w")
        
        self.amount_entry = ctk.CTkEntry(
            amount_frame,
            placeholder_text="Enter amount",
            width=300
        )
        self.amount_entry.pack(pady=(5, 0))
        
        # Category selection
        category_frame = ctk.CTkFrame(container, fg_color="transparent")
        category_frame.pack(fill="x", pady=(0, 10))
        
        category_label = ctk.CTkLabel(
            category_frame,
            text="Select Category:",
            font=ctk.CTkFont(size=14)
        )
        category_label.pack(anchor="w")
        
        # Get income categories
        self.categories = Category.get_categories_by_type(self.user.id, "income")
        self.category_var = ctk.StringVar()
        
        self.category_menu = ctk.CTkOptionMenu(
            category_frame,
            values=[cat.category_name for cat in self.categories],
            variable=self.category_var,
            width=300
        )
        self.category_menu.pack(pady=(5, 0))
        
        # Description input
        description_frame = ctk.CTkFrame(container, fg_color="transparent")
        description_frame.pack(fill="x", pady=(0, 10))
        
        description_label = ctk.CTkLabel(
            description_frame,
            text="Description (optional):",
            font=ctk.CTkFont(size=14)
        )
        description_label.pack(anchor="w")
        
        self.description_entry = ctk.CTkEntry(
            description_frame,
            placeholder_text="Enter description",
            width=300
        )
        self.description_entry.pack(pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(20, 0))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=100,
            command=self.close
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Add button
        add_btn = ctk.CTkButton(
            buttons_frame,
            text="Add",
            width=100,
            command=self.add_funds
        )
        add_btn.pack(side="right", padx=10)
    
    def add_funds(self):
        """Add funds to the selected account."""
        try:
            # Get selected account
            account_index = self.account_menu.current()
            if account_index < 0:
                self.show_error("Please select an account")
                return
            
            account = self.accounts[account_index]
            
            # Get amount
            try:
                amount = Decimal(self.amount_entry.get())
                if amount <= 0:
                    self.show_error("Amount must be greater than 0")
                    return
            except (ValueError, TypeError):
                self.show_error("Please enter a valid amount")
                return
            
            # Get selected category
            selected_category_index = self.category_menu.current()
            if selected_category_index < 0:
                self.show_error("Please select a category")
                return
            
            category = self.categories[selected_category_index]
            
            # Get description
            description = self.description_entry.get().strip()
            
            # Create transaction and update account balance
            success, message = Transaction.create_transaction(
                user_id=self.user.id,
                account_id=account.id,
                category_id=category.id,
                amount=amount,
                transaction_type="deposit",
                description=description
            )
            
            if success:
                # Show success message
                self.show_success("Funds added successfully!")
                # Call the callback to refresh the accounts list
                if self.callback:
                    self.callback()
                # Close the dialog after a delay
                self.after(2000, self.close)
            else:
                self.show_error(message)
                
        except Exception as e:
            self.show_error(f"An error occurred: {str(e)}")
    
    def show_error(self, message):
        """Show an error message."""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x150")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()
        
        # Center the dialog
        error_dialog.update_idletasks()
        width = error_dialog.winfo_width()
        height = error_dialog.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        error_dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Error icon
        icon_label = ctk.CTkLabel(
            error_dialog,
            text="✗",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="red"
        )
        icon_label.pack(pady=(20, 10))
        
        # Error message
        msg_label = ctk.CTkLabel(
            error_dialog,
            text=message,
            wraplength=250
        )
        msg_label.pack(pady=(0, 20))
        
        # OK button
        ok_btn = ctk.CTkButton(
            error_dialog,
            text="OK",
            width=100,
            command=error_dialog.destroy
        )
        ok_btn.pack(pady=(0, 20))
    
    def show_success(self, message):
        """Show a success message."""
        success_dialog = ctk.CTkToplevel(self)
        success_dialog.title("Success")
        success_dialog.geometry("300x150")
        success_dialog.resizable(False, False)
        success_dialog.transient(self)
        success_dialog.grab_set()
        
        # Center the dialog
        success_dialog.update_idletasks()
        width = success_dialog.winfo_width()
        height = success_dialog.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        success_dialog.geometry(f'{width}x{height}+{x}+{y}')
        
        # Success icon
        icon_label = ctk.CTkLabel(
            success_dialog,
            text="✓",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="green"
        )
        icon_label.pack(pady=(20, 10))
        
        # Success message
        msg_label = ctk.CTkLabel(
            success_dialog,
            text=message,
            wraplength=250
        )
        msg_label.pack(pady=(0, 20))
        
        # OK button
        ok_btn = ctk.CTkButton(
            success_dialog,
            text="OK",
            width=100,
            command=success_dialog.destroy
        )
        ok_btn.pack(pady=(0, 20))
    
    def close(self):
        """Close the dialog."""
        self.destroy() 