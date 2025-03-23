import customtkinter as ctk
import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction

class AdminDashboardView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.user = user
        
        # Set up grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Admin Dashboard",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(anchor="w")
        
        # Content
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Create statistics cards
        self.create_statistics_cards()
        
        # Create recent clients and transactions sections
        self.create_recent_clients()
        self.create_recent_transactions()
        
        # Refresh data
        self.refresh_dashboard()
    
    def create_statistics_cards(self):
        # Statistics frame
        stats_frame = ctk.CTkFrame(self.content_frame)
        stats_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total Clients Card
        clients_card = ctk.CTkFrame(stats_frame, corner_radius=10)
        clients_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        clients_title = ctk.CTkLabel(
            clients_card,
            text="Total Clients",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        clients_title.pack(padx=20, pady=(20, 5))
        
        self.clients_count = ctk.CTkLabel(
            clients_card,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2196F3"
        )
        self.clients_count.pack(padx=20, pady=(5, 20))
        
        # Total Accounts Card
        accounts_card = ctk.CTkFrame(stats_frame, corner_radius=10)
        accounts_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        accounts_title = ctk.CTkLabel(
            accounts_card,
            text="Total Accounts",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        accounts_title.pack(padx=20, pady=(20, 5))
        
        self.accounts_count = ctk.CTkLabel(
            accounts_card,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4CAF50"
        )
        self.accounts_count.pack(padx=20, pady=(5, 20))
        
        # Total Transactions Card
        transactions_card = ctk.CTkFrame(stats_frame, corner_radius=10)
        transactions_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        transactions_title = ctk.CTkLabel(
            transactions_card,
            text="Total Transactions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        transactions_title.pack(padx=20, pady=(20, 5))
        
        self.transactions_count = ctk.CTkLabel(
            transactions_card,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF9800"
        )
        self.transactions_count.pack(padx=20, pady=(5, 20))
    
    def create_recent_clients(self):
        # Recent clients frame
        self.clients_frame = ctk.CTkFrame(self.content_frame)
        self.clients_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Title
        clients_title = ctk.CTkLabel(
            self.clients_frame,
            text="Recent Clients",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        clients_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Clients list container
        self.clients_list_frame = ctk.CTkScrollableFrame(self.clients_frame, height=250)
        self.clients_list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def create_recent_transactions(self):
        # Recent transactions frame
        self.transactions_frame = ctk.CTkFrame(self.content_frame)
        self.transactions_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Title
        transactions_title = ctk.CTkLabel(
            self.transactions_frame,
            text="Recent Transactions",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        transactions_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Transactions list container
        self.transactions_list_frame = ctk.CTkScrollableFrame(self.transactions_frame, height=250)
        self.transactions_list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def update_statistics(self):
        """Update the statistics cards."""
        # Get clients assigned to the admin
        clients = User.get_clients_for_admin(self.user.id)
        
        # Count accounts and transactions
        accounts_count = 0
        transactions_count = 0
        
        # For each client, get their accounts and count them
        for client in clients:
            # Get accounts for this client
            client_accounts = Account.get_accounts_for_user(client.id)
            accounts_count += len(client_accounts)
            
            # For each account, get transactions and count them
            for account in client_accounts:
                transactions = Transaction.get_transactions_for_account(account.id)
                transactions_count += len(transactions)
        
        # Update UI
        self.clients_count.configure(text=str(len(clients)))
        self.accounts_count.configure(text=str(accounts_count))
        self.transactions_count.configure(text=str(transactions_count))
    
    def update_recent_clients(self):
        """Update the recent clients list."""
        # Clear existing clients
        for widget in self.clients_list_frame.winfo_children():
            widget.destroy()
        
        # Get assigned clients
        clients = User.get_clients_for_admin(self.user.id)
        
        if not clients:
            no_clients_label = ctk.CTkLabel(
                self.clients_list_frame,
                text="No clients found",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_clients_label.pack(pady=20)
            return
        
        # Add each client
        for i, client in enumerate(clients):
            # Get account count for this client
            client_accounts = Account.get_accounts_for_user(client.id)
            
            # Create row with alternating background color
            row_bg = ("gray90", "gray20") if i % 2 == 0 else ("gray85", "gray17")
            client_frame = ctk.CTkFrame(self.clients_list_frame, fg_color=row_bg, corner_radius=0, height=40)
            client_frame.pack(fill="x", pady=(0, 1))
            client_frame.grid_propagate(False)
            
            # Configure grid
            client_frame.grid_columnconfigure(0, weight=1)
            client_frame.grid_columnconfigure(1, weight=1)
            client_frame.grid_columnconfigure(2, weight=1)
            client_frame.grid_columnconfigure(3, weight=1)
            
            # Client name
            name_label = ctk.CTkLabel(
                client_frame,
                text=f"{client.first_name} {client.last_name}",
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            name_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
            
            # Client email
            email_label = ctk.CTkLabel(
                client_frame,
                text=client.email,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            email_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)
            
            # Account count
            accounts_label = ctk.CTkLabel(
                client_frame,
                text=f"Accounts: {len(client_accounts)}",
                font=ctk.CTkFont(size=12),
                text_color="#4CAF50",
                anchor="w"
            )
            accounts_label.grid(row=0, column=2, sticky="w", padx=10, pady=10)
            
            # View details button
            view_btn = ctk.CTkButton(
                client_frame,
                text="View Details",
                font=ctk.CTkFont(size=12),
                width=100,
                height=25,
                corner_radius=5,
                command=lambda client_id=client.id: self.view_client_details(client_id)
            )
            view_btn.grid(row=0, column=3, sticky="e", padx=10, pady=10)
    
    def view_client_details(self, client_id):
        """View details of a specific client."""
        # This would navigate to the client details view
        if hasattr(self.master, "show_view"):
            self.master.show_view("clients")
    
    def update_recent_transactions(self):
        """Update the recent transactions list."""
        # Clear existing transactions
        for widget in self.transactions_list_frame.winfo_children():
            widget.destroy()
        
        # Get clients assigned to the admin
        clients = User.get_clients_for_admin(self.user.id)
        
        # Collect all recent transactions
        all_transactions = []
        
        # For each client, get their accounts and transactions
        for client in clients:
            # Get accounts for this client
            client_accounts = Account.get_accounts_for_user(client.id)
            
            # For each account, get transactions
            for account in client_accounts:
                # Get transactions for this account
                transactions = Transaction.get_transactions_for_account(account.id, limit=5)
                
                # Add client and account info to each transaction
                for transaction in transactions:
                    # Create a dictionary with transaction data
                    transaction_data = {
                        'transaction': transaction,
                        'client_name': f"{client.first_name} {client.last_name}",
                        'account_name': account.account_name
                    }
                    all_transactions.append(transaction_data)
        
        # Sort transactions by date (newest first) and limit to 10
        all_transactions.sort(key=lambda x: x['transaction'].transaction_date if x['transaction'].transaction_date else datetime.now(), reverse=True)
        recent_transactions = all_transactions[:10]
        
        if not recent_transactions:
            no_transactions_label = ctk.CTkLabel(
                self.transactions_list_frame,
                text="No transactions found",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_transactions_label.pack(pady=20)
            return
        
        # Add each transaction
        for i, transaction_data in enumerate(recent_transactions):
            transaction = transaction_data['transaction']
            client_name = transaction_data['client_name']
            account_name = transaction_data['account_name']
            
            # Create row with alternating background color
            row_bg = ("gray90", "gray20") if i % 2 == 0 else ("gray85", "gray17")
            transaction_frame = ctk.CTkFrame(self.transactions_list_frame, fg_color=row_bg, corner_radius=0, height=50)
            transaction_frame.pack(fill="x", pady=(0, 1))
            transaction_frame.grid_propagate(False)
            
            # Configure grid
            transaction_frame.grid_columnconfigure(0, weight=1)
            transaction_frame.grid_columnconfigure(1, weight=1)
            transaction_frame.grid_columnconfigure(2, weight=1)
            transaction_frame.grid_columnconfigure(3, weight=1)
            
            # Format date
            date_str = transaction.transaction_date.strftime("%Y-%m-%d") if transaction.transaction_date else "N/A"
            
            # Transaction date
            date_label = ctk.CTkLabel(
                transaction_frame,
                text=date_str,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            date_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
            
            # Client name
            client_label = ctk.CTkLabel(
                transaction_frame,
                text=client_name,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            client_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)
            
            # Account
            account_label = ctk.CTkLabel(
                transaction_frame,
                text=account_name,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            account_label.grid(row=0, column=2, sticky="w", padx=10, pady=10)
            
            # Amount
            amount_color = "#4CAF50" if transaction.amount >= 0 else "#F44336"
            amount_label = ctk.CTkLabel(
                transaction_frame,
                text=f"${transaction.amount:,.2f}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=amount_color,
                anchor="w"
            )
            amount_label.grid(row=0, column=3, sticky="w", padx=10, pady=10)
    
    def refresh_dashboard(self):
        """Refresh all dashboard components."""
        self.update_statistics()
        self.update_recent_clients()
        self.update_recent_transactions() 