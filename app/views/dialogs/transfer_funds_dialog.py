import customtkinter as ctk
import sys
import os
from decimal import Decimal, InvalidOperation

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import models
from app.models.account import Account

class TransferFundsDialog(ctk.CTkToplevel):
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        
        # Configure the dialog
        self.title("Transfer Funds")
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
            text="Transfer Funds",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=(0, 20))
        
        # Placeholder message 
        # In a complete implementation, this would be replaced with form fields
        self.placeholder = ctk.CTkLabel(
            self.main_frame,
            text="This dialog would contain form fields for transferring funds between accounts.\n\n"
                 "It would include source account selection, destination account selection, amount entry, and description.",
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