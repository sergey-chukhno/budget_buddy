import customtkinter as ctk
import sys
import os
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction

class AdminTransactionsView(ctk.CTkFrame):
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
            text="Transactions Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Filters frame
        self.filters_frame = ctk.CTkFrame(self)
        self.filters_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.filters_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        
        # Client filter
        self.client_label = ctk.CTkLabel(
            self.filters_frame,
            text="Client:",
            font=ctk.CTkFont(size=12)
        )
        self.client_label.grid(row=0, column=0, sticky="e", padx=(20, 5), pady=10)
        
        self.client_var = ctk.StringVar(value="All Clients")
        self.client_dropdown = ctk.CTkComboBox(
            self.filters_frame,
            width=150,
            variable=self.client_var,
            values=["All Clients"]
        )
        self.client_dropdown.grid(row=0, column=1, sticky="w", padx=5, pady=10)
        self.client_dropdown.bind("<<ComboboxSelected>>", self.on_client_select)
        
        # Account filter
        self.account_label = ctk.CTkLabel(
            self.filters_frame,
            text="Account:",
            font=ctk.CTkFont(size=12)
        )
        self.account_label.grid(row=0, column=2, sticky="e", padx=(20, 5), pady=10)
        
        self.account_var = ctk.StringVar(value="All Accounts")
        self.account_dropdown = ctk.CTkComboBox(
            self.filters_frame,
            width=150,
            variable=self.account_var,
            values=["All Accounts"]
        )
        self.account_dropdown.grid(row=0, column=3, sticky="w", padx=5, pady=10)
        
        # Transaction type filter
        self.type_label = ctk.CTkLabel(
            self.filters_frame,
            text="Type:",
            font=ctk.CTkFont(size=12)
        )
        self.type_label.grid(row=0, column=4, sticky="e", padx=(20, 5), pady=10)
        
        self.type_var = ctk.StringVar(value="All Types")
        self.type_dropdown = ctk.CTkComboBox(
            self.filters_frame,
            width=120,
            variable=self.type_var,
            values=["All Types", "Income", "Expense", "Transfer"]
        )
        self.type_dropdown.grid(row=0, column=5, sticky="w", padx=5, pady=10)
        
        # Date range filter
        self.date_range_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        self.date_range_frame.grid(row=1, column=0, columnspan=6, sticky="ew", padx=20, pady=(0, 10))
        
        self.date_from_label = ctk.CTkLabel(
            self.date_range_frame,
            text="From:",
            font=ctk.CTkFont(size=12)
        )
        self.date_from_label.pack(side="left", padx=(0, 5))
        
        self.date_from_entry = ctk.CTkEntry(
            self.date_range_frame,
            width=100,
            placeholder_text="YYYY-MM-DD"
        )
        self.date_from_entry.pack(side="left", padx=(0, 15))
        
        self.date_to_label = ctk.CTkLabel(
            self.date_range_frame,
            text="To:",
            font=ctk.CTkFont(size=12)
        )
        self.date_to_label.pack(side="left", padx=(0, 5))
        
        self.date_to_entry = ctk.CTkEntry(
            self.date_range_frame,
            width=100,
            placeholder_text="YYYY-MM-DD"
        )
        self.date_to_entry.pack(side="left", padx=(0, 15))
        
        # Apply filters button
        self.apply_btn = ctk.CTkButton(
            self.date_range_frame,
            text="Apply Filters",
            width=120,
            command=self.apply_filters
        )
        self.apply_btn.pack(side="left", padx=10)
        
        # Reset filters button
        self.reset_btn = ctk.CTkButton(
            self.date_range_frame,
            text="Reset",
            width=80,
            fg_color="#F44336",
            hover_color="#D32F2F",
            command=self.reset_filters
        )
        self.reset_btn.pack(side="left", padx=10)
        
        # Transactions list
        self.transactions_frame = ctk.CTkFrame(self)
        self.transactions_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.transactions_frame.grid_columnconfigure(0, weight=1)
        self.transactions_frame.grid_rowconfigure(0, weight=1)
        
        # Create table
        self.create_transactions_table()
        
        # Initialize data
        self.load_clients()
        self.load_transactions()
    
    def create_transactions_table(self):
        # Column widths
        self.col_widths = [80, 120, 120, 130, 120, 110, 110, 120]
        
        # Table header
        header_frame = ctk.CTkFrame(self.transactions_frame, fg_color=("gray90", "gray25"))
        header_frame.pack(fill="x", pady=(0, 2))
        
        # Configure header columns
        for i in range(len(self.col_widths)):
            header_frame.grid_columnconfigure(i, weight=1, minsize=self.col_widths[i])
        
        # Header labels
        header_labels = ["ID", "Date", "Client", "Account", "Category", "Amount", "Type", "Actions"]
        for i, label_text in enumerate(header_labels):
            header_label = ctk.CTkLabel(
                header_frame,
                text=label_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            header_label.grid(row=0, column=i, sticky="w", padx=10, pady=10)
        
        # Scrollable frame for the table content
        self.table_content = ctk.CTkScrollableFrame(self.transactions_frame, fg_color="transparent")
        self.table_content.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Configure content frame
        for i in range(len(self.col_widths)):
            self.table_content.grid_columnconfigure(i, weight=1, minsize=self.col_widths[i])
    
    def load_clients(self):
        """Load client names for the dropdown."""
        # Get clients assigned to the admin
        clients = User.get_clients_for_admin(self.user.id)
        
        # Update the dropdown values
        client_names = ["All Clients"]
        for client in clients:
            client_names.append(f"{client.first_name} {client.last_name} ({client.id})")
        
        self.client_dropdown.configure(values=client_names)
    
    def load_accounts_for_client(self, client_id):
        """Load accounts for the selected client."""
        # Get accounts for the client
        accounts = Account.get_accounts_for_user(client_id)
        
        # Update the dropdown values
        account_names = ["All Accounts"]
        for account in accounts:
            account_names.append(f"{account.name} ({account.id})")
        
        self.account_dropdown.configure(values=account_names)
    
    def on_client_select(self, event=None):
        """Handle client selection change."""
        selected_client = self.client_var.get()
        
        if selected_client != "All Clients":
            # Extract ID from the format "First Last (ID)"
            try:
                client_id = int(selected_client.split("(")[1].split(")")[0])
                self.load_accounts_for_client(client_id)
            except:
                self.account_dropdown.configure(values=["All Accounts"])
        else:
            self.account_dropdown.configure(values=["All Accounts"])
        
        self.account_var.set("All Accounts")
    
    def load_transactions(self):
        """Load transactions for the current filters."""
        # Clear existing transactions
        for widget in self.table_content.winfo_children():
            widget.destroy()
        
        # Get the selected filters
        selected_client = self.client_var.get()
        selected_account = self.account_var.get()
        selected_type = self.type_var.get()
        date_from = self.date_from_entry.get()
        date_to = self.date_to_entry.get()
        
        # Parse client ID if a specific client is selected
        client_id = None
        if selected_client != "All Clients":
            try:
                client_id = int(selected_client.split("(")[1].split(")")[0])
            except:
                client_id = None
        
        # Parse account ID if a specific account is selected
        account_id = None
        if selected_account != "All Accounts":
            try:
                account_id = int(selected_account.split("(")[1].split(")")[0])
            except:
                account_id = None
        
        # Parse transaction type
        transaction_type = None
        if selected_type != "All Types":
            transaction_type = selected_type.lower()
        
        # Parse date range
        from_date = None
        to_date = None
        
        if date_from:
            try:
                from_date = datetime.strptime(date_from, "%Y-%m-%d")
            except:
                pass
        
        if date_to:
            try:
                to_date = datetime.strptime(date_to, "%Y-%m-%d")
            except:
                pass
        
        # Get clients assigned to the admin
        clients = User.get_clients_for_admin(self.user.id)
        
        # Collect all transactions based on filters
        all_transactions = []
        client_details = {}  # Map client ID to client name
        
        # For each client, get their accounts and transactions
        for client in clients:
            # Skip if filtering by client and this isn't the selected client
            if client_id is not None and client.id != client_id:
                continue
            
            # Store client name for later use
            client_details[client.id] = f"{client.first_name} {client.last_name}"
            
            # Get accounts for this client
            client_accounts = Account.get_accounts_for_user(client.id)
            
            # For each account, get transactions
            for account in client_accounts:
                # Skip if filtering by account and this isn't the selected account
                if account_id is not None and account.id != account_id:
                    continue
                
                # Get transactions for this account with filters
                transactions = Transaction.get_transactions_for_account(
                    account.id, 
                    limit=100,
                    start_date=from_date,
                    end_date=to_date,
                    transaction_type=transaction_type,
                    include_details=True
                )
                
                # Add client and account info to each transaction
                for transaction in transactions:
                    transaction.client_id = client.id
                    transaction.client_name = client_details[client.id]
                    all_transactions.append(transaction)
        
        # Sort transactions by date (newest first)
        all_transactions.sort(key=lambda x: x.transaction_date if x.transaction_date else datetime.now(), reverse=True)
        
        if not all_transactions:
            no_transactions_label = ctk.CTkLabel(
                self.table_content,
                text="No transactions found for the selected filters",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_transactions_label.pack(pady=40)
            return
        
        # Add each transaction
        for i, transaction in enumerate(all_transactions):
            # Row frame with alternating background
            row_bg = ("gray90", "gray20") if i % 2 == 0 else ("gray85", "gray17")
            row_frame = ctk.CTkFrame(self.table_content, fg_color=row_bg, corner_radius=0, height=50)
            row_frame.pack(fill="x", pady=(0, 1))
            row_frame.grid_propagate(False)
            
            # Configure columns
            for j in range(len(self.col_widths)):
                row_frame.grid_columnconfigure(j, weight=1, minsize=self.col_widths[j])
            
            # Transaction ID
            id_label = ctk.CTkLabel(
                row_frame,
                text=str(transaction.id),
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            id_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
            
            # Date
            date_str = transaction.transaction_date.strftime("%Y-%m-%d") if transaction.transaction_date else "N/A"
            date_label = ctk.CTkLabel(
                row_frame,
                text=date_str,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            date_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)
            
            # Client Name
            client_name_label = ctk.CTkLabel(
                row_frame,
                text=transaction.client_name,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            client_name_label.grid(row=0, column=2, sticky="w", padx=10, pady=10)
            
            # Account Name
            account_name_label = ctk.CTkLabel(
                row_frame,
                text=transaction.account_name,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            account_name_label.grid(row=0, column=3, sticky="w", padx=10, pady=10)
            
            # Category
            category_label = ctk.CTkLabel(
                row_frame,
                text=transaction.category_name if hasattr(transaction, 'category_name') else "",
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            category_label.grid(row=0, column=4, sticky="w", padx=10, pady=10)
            
            # Amount
            amount_color = "#4CAF50" if transaction.amount >= 0 else "#F44336"
            amount_text = f"${abs(transaction.amount):,.2f}"
            amount_label = ctk.CTkLabel(
                row_frame,
                text=amount_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=amount_color,
                anchor="w"
            )
            amount_label.grid(row=0, column=5, sticky="w", padx=10, pady=10)
            
            # Type
            type_bg = {"deposit": "#4CAF50", "withdrawal": "#F44336", "transfer": "#2196F3"}
            type_frame = ctk.CTkFrame(row_frame, fg_color=type_bg.get(transaction.transaction_type, "gray"))
            type_frame.grid(row=0, column=6, sticky="w", padx=10, pady=5)
            
            type_label = ctk.CTkLabel(
                type_frame,
                text=transaction.transaction_type.capitalize(),
                font=ctk.CTkFont(size=12),
                text_color="white",
                anchor="center"
            )
            type_label.pack(padx=8, pady=2)
            
            # Action buttons frame
            action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_frame.grid(row=0, column=7, sticky="ew", padx=10, pady=5)
            
            # View button
            view_btn = ctk.CTkButton(
                action_frame,
                text="View",
                font=ctk.CTkFont(size=12),
                width=60,
                height=25,
                fg_color="#2196F3",
                hover_color="#1976D2",
                command=lambda transaction_id=transaction.id: self.view_transaction(transaction_id)
            )
            view_btn.pack(side="left", padx=(0, 5))
            
            # Flag button
            flag_btn = ctk.CTkButton(
                action_frame,
                text="Flag",
                font=ctk.CTkFont(size=12),
                width=60,
                height=25,
                fg_color="#FF9800",
                hover_color="#F57C00",
                command=lambda transaction_id=transaction.id: self.flag_transaction(transaction_id)
            )
            flag_btn.pack(side="left", padx=5)
    
    def apply_filters(self):
        """Apply the selected filters and reload transactions."""
        self.load_transactions()
    
    def reset_filters(self):
        """Reset all filters to default values."""
        self.client_var.set("All Clients")
        self.account_var.set("All Accounts")
        self.type_var.set("All Types")
        self.date_from_entry.delete(0, "end")
        self.date_to_entry.delete(0, "end")
        self.load_transactions()
    
    def view_transaction(self, transaction_id):
        """View details of a specific transaction."""
        print(f"Viewing transaction with ID: {transaction_id}")
    
    def flag_transaction(self, transaction_id):
        """Flag a transaction for review."""
        print(f"Flagging transaction with ID: {transaction_id}") 