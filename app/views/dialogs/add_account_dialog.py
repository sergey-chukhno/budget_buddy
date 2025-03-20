import customtkinter as ctk
import sys
import os
import random
import string
from decimal import Decimal

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import models
from app.models.account_type import AccountType
from app.models.account import Account

class AddAccountDialog(ctk.CTkToplevel):
    def __init__(self, parent, user, callback=None):
        super().__init__(parent)
        
        self.parent = parent
        self.user = user
        self.callback = callback
        
        # Set up the dialog window
        self.title("Add New Account")
        self.geometry("400x400")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Set up grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Load account types
        self.account_types = AccountType.get_all_account_types()
        
        # Create the form
        self.create_form()
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make dialog modal and focus it
        self.focus_set()
        
        # Handle window close button
        self.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def create_form(self):
        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Add New Account",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="w")
        
        # Account Type
        type_label = ctk.CTkLabel(self, text="Account Type:", anchor="w")
        type_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")
        
        # Create account type options
        self.type_var = ctk.StringVar(value="Select account type")
        self.type_options = ["Select account type"] + [t.type_name for t in self.account_types]
        self.type_dropdown = ctk.CTkOptionMenu(
            self,
            variable=self.type_var,
            values=self.type_options,
            width=200
        )
        self.type_dropdown.grid(row=1, column=1, padx=20, pady=(0, 10), sticky="e")
        
        # Account Name
        name_label = ctk.CTkLabel(self, text="Account Name:", anchor="w")
        name_label.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="w")
        
        self.name_entry = ctk.CTkEntry(self, width=200)
        self.name_entry.grid(row=2, column=1, padx=20, pady=(10, 10), sticky="e")
        
        # Initial Balance
        balance_label = ctk.CTkLabel(self, text="Initial Balance ($):", anchor="w")
        balance_label.grid(row=3, column=0, padx=20, pady=(10, 10), sticky="w")
        
        self.balance_entry = ctk.CTkEntry(self, width=200)
        self.balance_entry.grid(row=3, column=1, padx=20, pady=(10, 10), sticky="e")
        self.balance_entry.insert(0, "0.00")
        
        # Account Number (auto-generated)
        number_label = ctk.CTkLabel(self, text="Account Number:", anchor="w")
        number_label.grid(row=4, column=0, padx=20, pady=(10, 10), sticky="w")
        
        self.account_number = self.generate_account_number()
        self.number_entry = ctk.CTkEntry(self, width=200)
        self.number_entry.grid(row=4, column=1, padx=20, pady=(10, 10), sticky="e")
        self.number_entry.insert(0, self.account_number)
        self.number_entry.configure(state="disabled")
        
        # Generate new number button
        self.generate_btn = ctk.CTkButton(
            self,
            text="Generate New",
            width=100,
            command=self.regenerate_account_number
        )
        self.generate_btn.grid(row=5, column=1, padx=20, pady=(0, 20), sticky="e")
        
        # Buttons
        self.cancel_btn = ctk.CTkButton(
            self,
            text="Cancel",
            width=100,
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.cancel
        )
        self.cancel_btn.grid(row=6, column=0, padx=20, pady=(30, 20), sticky="e")
        
        self.add_btn = ctk.CTkButton(
            self,
            text="Add Account",
            width=100,
            command=self.add_account
        )
        self.add_btn.grid(row=6, column=1, padx=20, pady=(30, 20), sticky="w")
    
    def generate_account_number(self):
        """Generate a random account number in the format FR + 10 digits."""
        digits = ''.join(random.choices(string.digits, k=10))
        return f"FR{digits}"
    
    def regenerate_account_number(self):
        """Generate a new account number and update the field."""
        self.account_number = self.generate_account_number()
        self.number_entry.configure(state="normal")
        self.number_entry.delete(0, "end")
        self.number_entry.insert(0, self.account_number)
        self.number_entry.configure(state="disabled")
    
    def validate_inputs(self):
        """Validate user inputs before creating account."""
        # Check if account type is selected
        if self.type_var.get() == "Select account type":
            return False, "Please select an account type."
        
        # Check if account name is provided
        if not self.name_entry.get().strip():
            return False, "Please enter an account name."
        
        # Check if initial balance is valid
        try:
            balance = Decimal(self.balance_entry.get())
            if balance < 0:
                return False, "Initial balance cannot be negative."
        except:
            return False, "Please enter a valid initial balance."
        
        return True, ""
    
    def add_account(self):
        """Add the account to the database."""
        # Validate inputs
        valid, message = self.validate_inputs()
        if not valid:
            # Show error message
            self.show_message_dialog("Error", message)
            return
        
        # Get selected account type id
        selected_type = self.type_var.get()
        account_type_id = None
        for at in self.account_types:
            if at.type_name == selected_type:
                account_type_id = at.id
                break
        
        if not account_type_id:
            # This shouldn't happen if validation works correctly
            self.show_message_dialog("Error", "Could not find selected account type.")
            return
        
        # Create the account
        try:
            initial_balance = Decimal(self.balance_entry.get())
            
            account, error_message = Account.create_account(
                user_id=self.user.id,
                account_type_id=account_type_id,
                account_name=self.name_entry.get().strip(),
                account_number=self.account_number,
                initial_balance=initial_balance
            )
            
            if account:
                # Show success message
                self.show_message_dialog("Success", "Account created successfully!", is_success=True)
                # Call the callback and close the dialog
                if self.callback:
                    self.callback()
                self.after(2000, self.destroy)  # Close after showing success message
            else:
                # Show error message
                self.show_message_dialog("Error", error_message or "Failed to create account.")
        except Exception as e:
            error_msg = str(e)
            print(f"Error creating account: {error_msg}")
            self.show_message_dialog("Error", f"Failed to create account: {error_msg}")
    
    def cancel(self):
        """Close the dialog without saving."""
        self.destroy()
    
    def show_message_dialog(self, title, message, is_success=False):
        """Show a message dialog with the given title and message."""
        message_dialog = ctk.CTkToplevel(self)
        message_dialog.title(title)
        message_dialog.geometry("300x180")
        message_dialog.resizable(False, False)
        message_dialog.transient(self)
        message_dialog.grab_set()
        
        # Make dialog modal
        message_dialog.focus_set()
        
        # Center the dialog
        message_dialog.update_idletasks()
        screen_width = message_dialog.winfo_screenwidth()
        screen_height = message_dialog.winfo_screenheight()
        x = (screen_width // 2) - (300 // 2)
        y = (screen_height // 2) - (180 // 2)
        message_dialog.geometry(f'300x180+{x}+{y}')
        
        # Add icon based on success/error
        if is_success:
            icon_text = "✓"
            icon_color = "green"
        else:
            icon_text = "✗"
            icon_color = "red"
        
        icon_label = ctk.CTkLabel(
            message_dialog,
            text=icon_text,
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=icon_color
        )
        icon_label.pack(pady=(20, 10))
        
        # Message
        msg_label = ctk.CTkLabel(
            message_dialog,
            text=message,
            wraplength=250
        )
        msg_label.pack(pady=(0, 20))
        
        # OK button
        ok_btn = ctk.CTkButton(
            message_dialog,
            text="OK",
            width=100,
            command=message_dialog.destroy
        )
        ok_btn.pack(pady=(0, 20))
        
        # Auto-close on success after delay
        if is_success:
            message_dialog.after(2000, message_dialog.destroy) 