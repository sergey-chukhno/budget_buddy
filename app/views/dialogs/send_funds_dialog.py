import customtkinter as ctk
import sys
import os
from decimal import Decimal, InvalidOperation

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import models
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.category import Category

class SendFundsDialog(ctk.CTkToplevel):
    def __init__(self, parent, user, callback=None):
        super().__init__(parent)
        
        self.parent = parent
        self.user = user
        self.callback = callback
        
        # Set up the dialog window
        self.title("Send Funds")
        self.geometry("450x620")  # Make it a bit wider and taller
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
        # Simple grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Send Funds to External Account",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(20, 30), padx=20, sticky="ew")
        
        # Account selection
        account_label = ctk.CTkLabel(
            self,
            text="Select Account:",
            font=ctk.CTkFont(size=14)
        )
        account_label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="w")
        
        # Get user's accounts
        self.accounts = Account.get_accounts_for_user(self.user.id)
        self.account_options = [f"{acc.account_name} (${acc.balance:,.2f})" for acc in self.accounts]
        
        # Account dropdown
        self.account_var = ctk.StringVar()
        if self.account_options:
            self.account_var.set(self.account_options[0])
        
        self.account_menu = ctk.CTkComboBox(
            self,
            values=self.account_options,
            variable=self.account_var,
            width=400,
            state="readonly"
        )
        self.account_menu.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        # Recipient
        recipient_label = ctk.CTkLabel(
            self,
            text="Recipient Information:",
            font=ctk.CTkFont(size=14)
        )
        recipient_label.grid(row=3, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.recipient_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter recipient name or account number",
            width=400
        )
        self.recipient_entry.grid(row=4, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        # Amount
        amount_label = ctk.CTkLabel(
            self,
            text="Amount:",
            font=ctk.CTkFont(size=14)
        )
        amount_label.grid(row=5, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.amount_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter amount",
            width=400
        )
        self.amount_entry.grid(row=6, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        # Category
        category_label = ctk.CTkLabel(
            self,
            text="Select Category:",
            font=ctk.CTkFont(size=14)
        )
        category_label.grid(row=7, column=0, padx=20, pady=(0, 5), sticky="w")
        
        # Get expense categories
        self.categories = Category.get_all_categories(is_expense=True)
        self.category_options = [cat.category_name for cat in self.categories]
        
        # Category dropdown
        self.category_var = ctk.StringVar()
        if self.category_options:
            self.category_var.set(self.category_options[0])
        else:
            self.category_options = ["Other Expense"]
            self.category_var.set(self.category_options[0])
        
        self.category_menu = ctk.CTkComboBox(
            self,
            values=self.category_options,
            variable=self.category_var,
            width=400,
            state="readonly"
        )
        self.category_menu.grid(row=8, column=0, padx=20, pady=(0, 15), sticky="ew")
        
        # Description
        description_label = ctk.CTkLabel(
            self,
            text="Description (optional):",
            font=ctk.CTkFont(size=14)
        )
        description_label.grid(row=9, column=0, padx=20, pady=(0, 5), sticky="w")
        
        self.description_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter description",
            width=400
        )
        self.description_entry.grid(row=10, column=0, padx=20, pady=(0, 30), sticky="ew")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=11, column=0, padx=20, pady=(0, 20), sticky="ew")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=180,
            command=self.close
        )
        cancel_btn.grid(row=0, column=0, padx=10, pady=0, sticky="w")
        
        # Send button
        send_btn = ctk.CTkButton(
            buttons_frame,
            text="Send",
            width=180,
            command=self.send_funds
        )
        send_btn.grid(row=0, column=1, padx=10, pady=0, sticky="e")
    
    def send_funds(self):
        """Send funds to the external recipient."""
        try:
            # Get selected account
            selected_account = self.account_var.get()
            if not selected_account:
                self.show_error("Please select an account")
                return
            
            # Find the account from the selection
            account = None
            for acc in self.accounts:
                if selected_account.startswith(acc.account_name):
                    account = acc
                    break
            
            if not account:
                self.show_error("Invalid account selection")
                return
            
            # Get recipient information
            recipient = self.recipient_entry.get().strip()
            if not recipient:
                self.show_error("Please enter recipient information")
                return
            
            # Get amount
            try:
                amount = Decimal(self.amount_entry.get())
                if amount <= 0:
                    self.show_error("Amount must be greater than 0")
                    return
                if amount > account.balance:
                    self.show_error("Insufficient funds")
                    return
            except (InvalidOperation, ValueError, TypeError):
                self.show_error("Please enter a valid amount")
                return
            
            # Get selected category
            selected_category = self.category_var.get()
            if not selected_category:
                self.show_error("Please select a category")
                return
            
            # Find the category from the selection
            category = None
            for cat in self.categories:
                if cat.category_name == selected_category:
                    category = cat
                    break
            
            if not category:
                self.show_error("Invalid category selection")
                return
            
            # Get description
            description = self.description_entry.get().strip()
            
            # Create transaction and update account balance
            success, message = Transaction.create_transaction(
                user_id=self.user.id,
                account_id=account.id,
                category_id=category.id,
                amount=amount,
                transaction_type="send",
                description=description,
                external_recipient=recipient
            )
            
            if success:
                # Show success message
                self.show_success("Funds sent successfully!")
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