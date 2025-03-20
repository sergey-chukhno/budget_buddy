import customtkinter as ctk
import sys
import os
from decimal import Decimal, InvalidOperation

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import models
from app.models.account import Account
from app.models.category import Category

class WithdrawFundsDialog(ctk.CTkToplevel):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        
        # Configure the dialog
        self.title("Withdraw Funds")
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
            text="Withdraw Funds",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # Placeholder message 
        # In a complete implementation, this would be replaced with form fields similar to AddFundsDialog
        self.placeholder = ctk.CTkLabel(
            self.main_frame,
            text="This dialog would contain form fields for withdrawing funds from an account.\n\n"
                 "It would include account selection, amount entry, category selection, and description.",
            wraplength=400
        )
        self.placeholder.pack(pady=50)
        
        # Close button
        self.close_button = ctk.CTkButton(
            self.main_frame,
            text="Close",
            command=self.destroy
        )
        self.close_button.pack(pady=20) 