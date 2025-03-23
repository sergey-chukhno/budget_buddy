import customtkinter as ctk
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction

# Import dialogs
from app.views.dialogs.add_funds_dialog import AddFundsDialog
from app.views.dialogs.withdraw_funds_dialog import WithdrawFundsDialog
from app.views.dialogs.transfer_funds_dialog import TransferFundsDialog
from app.views.dialogs.send_funds_dialog import SendFundsDialog

class AdminAccountsView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.user = user
        
        # Set up grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Accounts Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Filters frame
        self.filters_frame = ctk.CTkFrame(self)
        self.filters_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        # Client filter
        self.client_label = ctk.CTkLabel(
            self.filters_frame,
            text="Client:",
            font=ctk.CTkFont(size=12)
        )
        self.client_label.pack(side="left", padx=(20, 5), pady=10)
        
        self.client_var = ctk.StringVar(value="All Clients")
        self.client_dropdown = ctk.CTkComboBox(
            self.filters_frame,
            width=200,
            variable=self.client_var,
            values=["All Clients"]
        )
        self.client_dropdown.pack(side="left", padx=5, pady=10)
        
        # Account type filter
        self.account_type_label = ctk.CTkLabel(
            self.filters_frame,
            text="Account Type:",
            font=ctk.CTkFont(size=12)
        )
        self.account_type_label.pack(side="left", padx=(20, 5), pady=10)
        
        self.account_type_var = ctk.StringVar(value="All Types")
        self.account_type_dropdown = ctk.CTkComboBox(
            self.filters_frame,
            width=150,
            variable=self.account_type_var,
            values=["All Types"]
        )
        self.account_type_dropdown.pack(side="left", padx=5, pady=10)
        
        # Apply filters button
        self.apply_btn = ctk.CTkButton(
            self.filters_frame,
            text="Apply Filters",
            width=120,
            command=self.apply_filters
        )
        self.apply_btn.pack(side="left", padx=20, pady=10)
        
        # Accounts list
        self.accounts_frame = ctk.CTkFrame(self)
        self.accounts_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.accounts_frame.grid_columnconfigure(0, weight=1)
        self.accounts_frame.grid_rowconfigure(0, weight=1)
        
        # Create table
        self.create_accounts_table()
        
        # Initialize data
        self.load_clients()
        self.load_account_types()
        self.load_accounts()
    
    def create_accounts_table(self):
        # Column widths
        col_widths = [80, 150, 150, 150, 150, 150]
        
        # Table header
        header_frame = ctk.CTkFrame(self.accounts_frame, fg_color=("gray90", "gray25"))
        header_frame.pack(fill="x", pady=(0, 2))
        
        # Configure header columns
        for i in range(6):
            header_frame.grid_columnconfigure(i, weight=1, minsize=col_widths[i])
        
        # Header labels
        header_labels = ["ID", "Client", "Account Name", "Type", "Balance", "Actions"]
        for i, label_text in enumerate(header_labels):
            header_label = ctk.CTkLabel(
                header_frame,
                text=label_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            header_label.grid(row=0, column=i, sticky="w", padx=10, pady=10)
        
        # Scrollable frame for the table content
        self.table_content = ctk.CTkScrollableFrame(self.accounts_frame, fg_color="transparent")
        self.table_content.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Configure content frame
        self.table_content.grid_columnconfigure(0, weight=1)
    
    def load_clients(self):
        """Load client names for the dropdown."""
        # Get clients assigned to the admin
        clients = User.get_clients_for_admin(self.user.id)
        
        # Update the dropdown values
        client_names = ["All Clients"]
        for client in clients:
            client_names.append(f"{client.first_name} {client.last_name} ({client.id})")
        
        self.client_dropdown.configure(values=client_names)
    
    def load_account_types(self):
        """Load account types for the dropdown."""
        # This would get account types from the database
        # For now, use hardcoded values
        account_types = ["All Types", "Checking", "Savings", "Investment"]
        self.account_type_dropdown.configure(values=account_types)
    
    def load_accounts(self):
        """Load accounts for the current filters."""
        # Clear existing accounts
        for widget in self.table_content.winfo_children():
            widget.destroy()
        
        # Get the selected filters
        selected_client = self.client_var.get()
        selected_type = self.account_type_var.get()
        
        # Parse client ID if a specific client is selected
        client_id = None
        if selected_client != "All Clients":
            # Extract ID from the format "First Last (ID)"
            try:
                client_id = int(selected_client.split("(")[1].split(")")[0])
            except:
                client_id = None
        
        # Get account type ID if a specific type is selected
        account_type = None
        if selected_type != "All Types":
            account_type = selected_type
        
        # Get clients assigned to the admin
        clients = User.get_clients_for_admin(self.user.id)
        
        # Store accounts of all clients
        all_accounts = []
        
        # Get accounts for each client
        for client in clients:
            # Skip if filtering by client and this isn't the selected client
            if client_id is not None and client.id != client_id:
                continue
                
            # Get this client's accounts
            accounts = Account.get_accounts_for_user(client.id)
            
            # Add client information to each account
            for account in accounts:
                account.client_name = f"{client.first_name} {client.last_name}"
                account.client_id = client.id
                all_accounts.append(account)
        
        # Filter by account type if needed
        if account_type and account_type != "All Types":
            filtered_accounts = []
            for account in all_accounts:
                if account.account_type_name == account_type:
                    filtered_accounts.append(account)
            all_accounts = filtered_accounts
            
        # Display "No accounts found" if list is empty
        if not all_accounts:
            no_accounts_label = ctk.CTkLabel(
                self.table_content,
                text="No accounts found for the selected filters",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_accounts_label.pack(pady=40)
            return
        
        # Column widths (same as header)
        col_widths = [80, 150, 150, 150, 150, 150]
        
        # Add each account
        for i, account in enumerate(all_accounts):
            # Row frame with alternating background
            row_bg = ("gray90", "gray20") if i % 2 == 0 else ("gray85", "gray17")
            row_frame = ctk.CTkFrame(self.table_content, fg_color=row_bg, corner_radius=0, height=50)
            row_frame.pack(fill="x", pady=(0, 1))
            row_frame.grid_propagate(False)
            
            # Configure columns
            for j in range(6):
                row_frame.grid_columnconfigure(j, weight=1, minsize=col_widths[j])
            
            # Account ID
            id_label = ctk.CTkLabel(
                row_frame,
                text=str(account.id),
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            id_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
            
            # Client Name
            client_name_label = ctk.CTkLabel(
                row_frame,
                text=account.client_name,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            client_name_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)
            
            # Account Name
            account_name_label = ctk.CTkLabel(
                row_frame,
                text=account.account_name,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            account_name_label.grid(row=0, column=2, sticky="w", padx=10, pady=10)
            
            # Account Type
            account_type_label = ctk.CTkLabel(
                row_frame,
                text=account.account_type_name,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            account_type_label.grid(row=0, column=3, sticky="w", padx=10, pady=10)
            
            # Balance
            balance_label = ctk.CTkLabel(
                row_frame,
                text=f"${account.balance:,.2f}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4CAF50" if account.balance >= 0 else "#F44336",
                anchor="w"
            )
            balance_label.grid(row=0, column=4, sticky="w", padx=10, pady=10)
            
            # Action buttons frame
            action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_frame.grid(row=0, column=5, sticky="ew", padx=10, pady=5)
            
            # Fund management buttons
            add_funds_btn = ctk.CTkButton(
                action_frame,
                text="Add",
                font=ctk.CTkFont(size=12),
                width=60,
                height=25,
                fg_color="#4CAF50",
                hover_color="#388E3C",
                command=lambda account_id=account.id, client_id=account.client_id: self.add_funds(account_id, client_id)
            )
            add_funds_btn.pack(side="left", padx=(0, 5))
            
            withdraw_btn = ctk.CTkButton(
                action_frame,
                text="Withdraw",
                font=ctk.CTkFont(size=12),
                width=70,
                height=25,
                fg_color="#FF9800",
                hover_color="#F57C00",
                command=lambda account_id=account.id, client_id=account.client_id: self.withdraw_funds(account_id, client_id)
            )
            withdraw_btn.pack(side="left", padx=5)
            
            transfer_btn = ctk.CTkButton(
                action_frame,
                text="Transfer",
                font=ctk.CTkFont(size=12),
                width=70,
                height=25,
                fg_color="#2196F3",
                hover_color="#1976D2",
                command=lambda account_id=account.id, client_id=account.client_id: self.transfer_funds(account_id, client_id)
            )
            transfer_btn.pack(side="left", padx=5)
            
            send_btn = ctk.CTkButton(
                action_frame,
                text="Send",
                font=ctk.CTkFont(size=12),
                width=60,
                height=25,
                fg_color="#9C27B0",
                hover_color="#7B1FA2",
                command=lambda account_id=account.id, client_id=account.client_id: self.send_funds(account_id, client_id)
            )
            send_btn.pack(side="left", padx=5)
    
    def apply_filters(self):
        """Apply the selected filters and reload accounts."""
        self.load_accounts()
    
    def view_account(self, account_id):
        """View details of a specific account."""
        print(f"Viewing account with ID: {account_id}")
    
    def toggle_freeze_account(self, account_id):
        """Freeze or unfreeze an account."""
        print(f"Toggling freeze status for account with ID: {account_id}")
        
    def add_funds(self, account_id, client_id):
        """Open dialog to add funds to client account."""
        account = Account.get_account_by_id(account_id)
        if not account:
            return
            
        # Get client information
        client = User.get_user_by_id(client_id)
        if not client:
            return
            
        # Create deposit dialog
        deposit_dialog = AddFundsDialog(self, client, callback=lambda: self.load_accounts())
        
        # Set the selected account - wait for dialog to be fully created
        # Set the selected account
        deposit_dialog.after(100, lambda: deposit_dialog.set_preselected_account(account_id))
        
        # Show the dialog and wait for it to close
        deposit_dialog.wait_window()
        
    def withdraw_funds(self, account_id, client_id):
        """Open dialog to withdraw funds from client account."""
        account = Account.get_account_by_id(account_id)
        if not account:
            return
            
        # Get client information
        client = User.get_user_by_id(client_id)
        if not client:
            return
            
        # Create withdraw dialog
        withdraw_dialog = WithdrawFundsDialog(self, client, callback=lambda: self.load_accounts())
        
        # Set the selected account
        withdraw_dialog.after(100, lambda: withdraw_dialog.set_preselected_account(account_id))
        
        # Show the dialog and wait for it to close
        withdraw_dialog.wait_window()
        
    def transfer_funds(self, account_id, client_id):
        """Open dialog to transfer funds between client accounts."""
        account = Account.get_account_by_id(account_id)
        if not account:
            return
            
        # Get all accounts for this client
        client_accounts = Account.get_accounts_for_user(client_id)
        if not client_accounts or len(client_accounts) < 2:
            # Need at least 2 accounts to transfer between them
            return
            
        # Get client information
        client = User.get_user_by_id(client_id)
        if not client:
            return
            
        # Create transfer dialog
        transfer_dialog = TransferFundsDialog(self, client, callback=lambda: self.load_accounts())
        
        # Set the selected account
        transfer_dialog.after(100, lambda: transfer_dialog.set_preselected_account(account_id))
        
        # Show the dialog and wait for it to close
        transfer_dialog.wait_window()
        
    def send_funds(self, account_id, client_id):
        """Open dialog to send funds to external recipient."""
        account = Account.get_account_by_id(account_id)
        if not account:
            return
            
        # Get client information
        client = User.get_user_by_id(client_id)
        if not client:
            return
            
        # Create external transfer dialog
        external_dialog = SendFundsDialog(self, client, callback=lambda: self.load_accounts())
        
        # Set the selected account
        external_dialog.after(100, lambda: external_dialog.set_preselected_account(account_id))
        
        # Show the dialog and wait for it to close
        external_dialog.wait_window() 