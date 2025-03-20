import customtkinter as ctk
import sys
import os
from decimal import Decimal, InvalidOperation

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import models
from app.models.account import Account
from app.models.transaction import Transaction

class TransferFundsDialog(ctk.CTkToplevel):
    def __init__(self, parent, user, callback=None):
        super().__init__(parent)
        
        self.parent = parent
        self.user = user
        self.callback = callback
        
        # Set up the dialog window
        self.title("Transfer Funds")
        self.geometry("400x500")
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
        
        # Create the widgets
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
            text="Transfer Funds Between Accounts",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Get user's accounts
        self.accounts = Account.get_accounts_for_user(self.user.id)
        
        # Check if user has at least two accounts
        if len(self.accounts) < 2:
            insufficient_accounts_label = ctk.CTkLabel(
                container,
                text="You need at least two accounts to make a transfer.\nPlease create another account first.",
                text_color="red",
                wraplength=300
            )
            insufficient_accounts_label.pack(pady=20)
            
            close_btn = ctk.CTkButton(
                container,
                text="Close",
                command=self.close
            )
            close_btn.pack(pady=20)
            return
        
        # From Account selection
        from_account_frame = ctk.CTkFrame(container, fg_color="transparent")
        from_account_frame.pack(fill="x", pady=(0, 10))
        
        from_account_label = ctk.CTkLabel(
            from_account_frame,
            text="From Account:",
            font=ctk.CTkFont(size=14)
        )
        from_account_label.pack(anchor="w")
        
        self.from_account_var = ctk.StringVar()
        from_account_options = [f"{acc.account_name} (${acc.balance:.2f})" for acc in self.accounts]
        self.from_account_var.set(from_account_options[0])
        
        self.from_account_menu = ctk.CTkOptionMenu(
            from_account_frame,
            values=from_account_options,
            variable=self.from_account_var,
            width=300,
            command=self.update_to_account_options
        )
        self.from_account_menu.pack(pady=(5, 0))
        
        # To Account selection
        to_account_frame = ctk.CTkFrame(container, fg_color="transparent")
        to_account_frame.pack(fill="x", pady=(0, 10))
        
        to_account_label = ctk.CTkLabel(
            to_account_frame,
            text="To Account:",
            font=ctk.CTkFont(size=14)
        )
        to_account_label.pack(anchor="w")
        
        self.to_account_var = ctk.StringVar()
        # Initialize to_account_options without the first account (which is selected as from_account)
        to_account_options = [f"{acc.account_name} (${acc.balance:.2f})" for acc in self.accounts if acc.account_name != self.accounts[0].account_name]
        
        if to_account_options:
            self.to_account_var.set(to_account_options[0])
        
        self.to_account_menu = ctk.CTkOptionMenu(
            to_account_frame,
            values=to_account_options,
            variable=self.to_account_var,
            width=300
        )
        self.to_account_menu.pack(pady=(5, 0))
        
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
        
        # Transfer button
        transfer_btn = ctk.CTkButton(
            buttons_frame,
            text="Transfer",
            width=100,
            command=self.transfer_funds
        )
        transfer_btn.pack(side="right", padx=10)
    
    def update_to_account_options(self, from_account_text):
        """Update the to account options based on the selected from account."""
        # Get the selected from account name
        from_account_name = from_account_text.split(" (")[0]
        
        # Create new to account options, excluding the selected from account
        to_account_options = [f"{acc.account_name} (${acc.balance:.2f})" for acc in self.accounts 
                             if acc.account_name != from_account_name]
        
        # Update the to account menu
        self.to_account_menu.configure(values=to_account_options)
        
        # Set the default value if there are options
        if to_account_options:
            self.to_account_var.set(to_account_options[0])
    
    def transfer_funds(self):
        """Transfer funds between accounts."""
        try:
            # Get from account
            from_account_text = self.from_account_var.get()
            from_account_name = from_account_text.split(" (")[0]
            from_account = next((acc for acc in self.accounts if acc.account_name == from_account_name), None)
            
            if not from_account:
                self.show_error("Source account not found")
                return
            
            # Get to account
            to_account_text = self.to_account_var.get()
            to_account_name = to_account_text.split(" (")[0]
            to_account = next((acc for acc in self.accounts if acc.account_name == to_account_name), None)
            
            if not to_account:
                self.show_error("Destination account not found")
                return
                
            # Get amount
            try:
                amount = Decimal(self.amount_entry.get())
                if amount <= 0:
                    self.show_error("Amount must be greater than 0")
                    return
                
                # Check if the source account has enough funds
                if amount > from_account.balance:
                    self.show_error("Insufficient funds in the source account")
                    return
                
            except (ValueError, InvalidOperation):
                self.show_error("Please enter a valid amount")
                return
            
            # Get description
            description = self.description_entry.get().strip() or f"Transfer from {from_account_name} to {to_account_name}"
            
            # Perform the transfer transaction
            success, message = Transaction.create_transaction(
                user_id=self.user.id,
                account_id=from_account.id,
                category_id=None,  # No category needed for transfers
                amount=amount,
                transaction_type="transfer",
                description=description,
                recipient_account_id=to_account.id
            )
            
            if success:
                self.show_success("Funds transferred successfully!")
                
                # If callback is provided, call it to refresh the view
                if self.callback:
                    self.callback()
                
                # Close dialog after delay
                self.after(2000, self.close)
            else:
                self.show_error(f"Transfer failed: {message}")
                
        except Exception as e:
            self.show_error(f"An error occurred: {str(e)}")
    
    def show_error(self, message):
        """Show an error message dialog."""
        error_dialog = ctk.CTkToplevel(self)
        error_dialog.title("Error")
        error_dialog.geometry("300x150")
        error_dialog.resizable(False, False)
        error_dialog.transient(self)
        error_dialog.grab_set()
        
        # Center dialog
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
        """Show a success message dialog."""
        success_dialog = ctk.CTkToplevel(self)
        success_dialog.title("Success")
        success_dialog.geometry("300x150")
        success_dialog.resizable(False, False)
        success_dialog.transient(self)
        success_dialog.grab_set()
        
        # Center dialog
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