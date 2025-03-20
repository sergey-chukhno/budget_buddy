import customtkinter as ctk
from datetime import datetime

class ViewAccountDialog(ctk.CTkToplevel):
    def __init__(self, parent, account):
        super().__init__(parent)
        
        self.parent = parent
        self.account = account
        
        # Set up the dialog window
        self.title("Account Details")
        self.geometry("500x400")
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
        
        # Account Type
        type_frame = ctk.CTkFrame(container, fg_color="transparent")
        type_frame.pack(fill="x", pady=(0, 10))
        
        type_label = ctk.CTkLabel(
            type_frame,
            text="Account Type:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        type_label.pack(side="left")
        
        type_value = ctk.CTkLabel(
            type_frame,
            text=self.account.account_type_name,
            font=ctk.CTkFont(size=14)
        )
        type_value.pack(side="left", padx=10)
        
        # Account Name
        name_frame = ctk.CTkFrame(container, fg_color="transparent")
        name_frame.pack(fill="x", pady=(0, 10))
        
        name_label = ctk.CTkLabel(
            name_frame,
            text="Account Name:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack(side="left")
        
        name_value = ctk.CTkLabel(
            name_frame,
            text=self.account.account_name,
            font=ctk.CTkFont(size=14)
        )
        name_value.pack(side="left", padx=10)
        
        # Account Number
        number_frame = ctk.CTkFrame(container, fg_color="transparent")
        number_frame.pack(fill="x", pady=(0, 10))
        
        number_label = ctk.CTkLabel(
            number_frame,
            text="Account Number:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        number_label.pack(side="left")
        
        number_value = ctk.CTkLabel(
            number_frame,
            text=self.account.account_number,
            font=ctk.CTkFont(size=14)
        )
        number_value.pack(side="left", padx=10)
        
        # Balance
        balance_frame = ctk.CTkFrame(container, fg_color="transparent")
        balance_frame.pack(fill="x", pady=(0, 10))
        
        balance_label = ctk.CTkLabel(
            balance_frame,
            text="Current Balance:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        balance_label.pack(side="left")
        
        balance_value = ctk.CTkLabel(
            balance_frame,
            text=f"${self.account.balance:,.2f}",
            font=ctk.CTkFont(size=14)
        )
        balance_value.pack(side="left", padx=10)
        
        # Status
        status_frame = ctk.CTkFrame(container, fg_color="transparent")
        status_frame.pack(fill="x", pady=(0, 10))
        
        status_label = ctk.CTkLabel(
            status_frame,
            text="Status:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        status_label.pack(side="left")
        
        status_value = ctk.CTkLabel(
            status_frame,
            text="Active" if self.account.is_active else "Inactive",
            font=ctk.CTkFont(size=14)
        )
        status_value.pack(side="left", padx=10)
        
        # Created At
        created_frame = ctk.CTkFrame(container, fg_color="transparent")
        created_frame.pack(fill="x", pady=(0, 10))
        
        created_label = ctk.CTkLabel(
            created_frame,
            text="Created At:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        created_label.pack(side="left")
        
        created_value = ctk.CTkLabel(
            created_frame,
            text=self.account.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.account.created_at else "N/A",
            font=ctk.CTkFont(size=14)
        )
        created_value.pack(side="left", padx=10)
        
        # Close button
        close_btn = ctk.CTkButton(
            container,
            text="Close",
            width=100,
            command=self.close
        )
        close_btn.pack(pady=(20, 0))
    
    def close(self):
        """Close the dialog."""
        self.destroy() 