import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")
import numpy as np
from datetime import datetime, timedelta
import sys
import os
from decimal import Decimal

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.category import Category
from app.views.dialogs.add_funds_dialog import AddFundsDialog
from app.views.dialogs.send_funds_dialog import SendFundsDialog
from app.views.dialogs.withdraw_funds_dialog import WithdrawFundsDialog
from app.views.dialogs.transfer_funds_dialog import TransferFundsDialog

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.user = user
        
        # Set up grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Welcome header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        
        self.welcome_label = ctk.CTkLabel(
            self.header_frame,
            text=f"Welcome to Billionnaires Budget Buddy",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.welcome_label.pack(side="left", padx=0, pady=0)
        
        # Quick actions frame
        self.actions_frame = ctk.CTkFrame(self)
        self.actions_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.add_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Add Funds",
            command=self.add_funds
        )
        self.add_btn.pack(side="left", padx=10, pady=10)
        
        self.withdraw_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Withdraw Funds",
            command=self.withdraw_funds
        )
        self.withdraw_btn.pack(side="left", padx=10, pady=10)
        
        self.transfer_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Transfer Funds",
            command=self.transfer_funds
        )
        self.transfer_btn.pack(side="left", padx=10, pady=10)
        
        self.send_btn = ctk.CTkButton(
            self.actions_frame, 
            text="Send Funds",
            command=self.send_funds
        )
        self.send_btn.pack(side="left", padx=10, pady=10)
        
        # Dashboard content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=2)
        self.content_frame.grid_columnconfigure(1, weight=3)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=4)
        
        # Create summary cards and transaction list
        self.create_summary_cards()
        self.create_recent_transactions()
        
        # Load data
        self.refresh_dashboard()
    
    def create_summary_cards(self):
        """Create summary cards for total balance and account count."""
        summary_frame = ctk.CTkFrame(self.content_frame)
        summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        summary_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Total Balance Card
        balance_card = ctk.CTkFrame(summary_frame, corner_radius=10)
        balance_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        balance_title = ctk.CTkLabel(
            balance_card,
            text="Total Balance",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        balance_title.pack(padx=20, pady=(20, 5))
        
        self.balance_value = ctk.CTkLabel(
            balance_card,
            text="$0.00",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#4CAF50"
        )
        self.balance_value.pack(padx=20, pady=(5, 20))
        
        # Account Count Card
        account_card = ctk.CTkFrame(summary_frame, corner_radius=10)
        account_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        account_title = ctk.CTkLabel(
            account_card,
            text="Total Accounts",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        account_title.pack(padx=20, pady=(20, 5))
        
        self.account_count = ctk.CTkLabel(
            account_card,
            text="0",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2196F3"
        )
        self.account_count.pack(padx=20, pady=(5, 20))
    
    def create_recent_transactions(self):
        """Create recent transactions section."""
        # Transactions frame
        self.transactions_frame = ctk.CTkFrame(self.content_frame)
        self.transactions_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        
        # Transactions title
        transactions_title = ctk.CTkLabel(
            self.transactions_frame,
            text="Recent Transactions",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        transactions_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Transactions list container with scrollbar
        self.transactions_list_frame = ctk.CTkScrollableFrame(self.transactions_frame, height=300)
        self.transactions_list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def add_funds(self):
        """Open add funds dialog."""
        dialog = AddFundsDialog(self, self.user, callback=self.refresh_dashboard)
        dialog.wait_window()
    
    def withdraw_funds(self):
        """Open withdraw funds dialog."""
        dialog = WithdrawFundsDialog(self, self.user, callback=self.refresh_dashboard)
        dialog.wait_window()
    
    def transfer_funds(self):
        """Open transfer funds dialog."""
        dialog = TransferFundsDialog(self, self.user, callback=self.refresh_dashboard)
        dialog.wait_window()
    
    def send_funds(self):
        """Open send funds dialog."""
        dialog = SendFundsDialog(self, self.user, callback=self.refresh_dashboard)
        dialog.wait_window()
    
    def update_total_balance(self):
        """Update the total balance display."""
        total_balance = 0
        accounts = Account.get_accounts_for_user(self.user.id)
        for account in accounts:
            total_balance += account.balance
        
        self.balance_value.configure(text=f"${total_balance:,.2f}")
    
    def update_account_count(self):
        """Update the account count display."""
        accounts = Account.get_accounts_for_user(self.user.id)
        self.account_count.configure(text=str(len(accounts)))
    
    def update_recent_transactions(self):
        """Update the recent transactions list."""
        # Clear existing transactions
        for widget in self.transactions_list_frame.winfo_children():
            widget.destroy()
        
        # Get recent transactions (last 5)
        transactions = Transaction.get_transactions_for_user(
            self.user.id,
            limit=5,
            include_details=True
        )
        
        if not transactions:
            no_transactions_label = ctk.CTkLabel(
                self.transactions_list_frame,
                text="No transactions found",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_transactions_label.pack(pady=20)
            return
        
        # Define column widths
        col_widths = [150, 150, 120, 120, 180]
        
        # Create header
        header_frame = ctk.CTkFrame(self.transactions_list_frame, fg_color=("gray90", "gray25"))
        header_frame.pack(fill="x", pady=(0, 5))
        
        # Configure header columns with fixed widths
        for i in range(5):
            header_frame.grid_columnconfigure(i, weight=1, minsize=col_widths[i])
        
        # Header labels
        header_labels = ["Date", "Account", "Category", "Amount", "Type"]
        for i, label_text in enumerate(header_labels):
            header_label = ctk.CTkLabel(
                header_frame,
                text=label_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
                width=col_widths[i]
            )
            header_label.grid(row=0, column=i, sticky="w", padx=5, pady=5)
        
        # Add each transaction
        for i, transaction in enumerate(transactions):
            # Create row with alternating background color
            row_bg = ("gray90", "gray20") if i % 2 == 0 else ("gray85", "gray17")
            transaction_frame = ctk.CTkFrame(self.transactions_list_frame, fg_color=row_bg, corner_radius=0, height=40)
            transaction_frame.pack(fill="x", pady=(0, 1))
            transaction_frame.grid_propagate(False)  # Fix the height
            
            # Configure row columns with fixed widths
            for j in range(5):
                transaction_frame.grid_columnconfigure(j, weight=1, minsize=col_widths[j])
            
            # Format date
            date_str = transaction.transaction_date.strftime("%Y-%m-%d %H:%M")
            
            # Format amount text and color
            amount = float(transaction.amount)
            if transaction.transaction_type in ["withdrawal", "external_transfer", "transfer"]:
                # For outgoing transactions, show negative amount
                if transaction.account_id:  # If this is the source account
                    amount_text = f"-${amount:,.2f}"
                    amount_color = "#F44336"  # Red
                else:
                    amount_text = f"${amount:,.2f}"
                    amount_color = "#4CAF50"  # Green
            else:
                amount_text = f"${amount:,.2f}"
                amount_color = "#4CAF50"  # Green
            
            # Transaction type display
            transaction_type_map = {
                "deposit": "Deposit",
                "withdrawal": "Withdrawal", 
                "transfer": "Transfer",
                "external_transfer": "External Transfer"
            }
            
            type_text = transaction_type_map.get(transaction.transaction_type, transaction.transaction_type)
            
            # Get type color based on transaction type
            def get_type_color(transaction_type):
                if transaction_type == "deposit":
                    return "#4CAF50"  # Green
                elif transaction_type == "withdrawal":
                    return "#F44336"  # Red
                elif transaction_type == "transfer":
                    return "#2196F3"  # Blue
                elif transaction_type == "external_transfer":
                    return "#FF9800"  # Orange
                else:
                    return "#9E9E9E"  # Gray
            
            # Data cells
            date_label = ctk.CTkLabel(
                transaction_frame,
                text=date_str,
                font=ctk.CTkFont(size=12),
                anchor="w",
                width=col_widths[0]
            )
            date_label.grid(row=0, column=0, sticky="w", padx=5, pady=8)
            
            account_label = ctk.CTkLabel(
                transaction_frame,
                text=transaction.account_name or "Unknown",
                font=ctk.CTkFont(size=12),
                anchor="w",
                width=col_widths[1]
            )
            account_label.grid(row=0, column=1, sticky="w", padx=5, pady=8)
            
            category_label = ctk.CTkLabel(
                transaction_frame,
                text=transaction.category_name or "N/A",
                font=ctk.CTkFont(size=12),
                anchor="w",
                width=col_widths[2]
            )
            category_label.grid(row=0, column=2, sticky="w", padx=5, pady=8)
            
            amount_label = ctk.CTkLabel(
                transaction_frame,
                text=amount_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=amount_color,
                anchor="e",
                width=col_widths[3]
            )
            amount_label.grid(row=0, column=3, sticky="e", padx=5, pady=8)
            
            # Type with styled background
            type_frame = ctk.CTkFrame(
                transaction_frame, 
                fg_color=get_type_color(transaction.transaction_type), 
                corner_radius=8
            )
            type_frame.grid(row=0, column=4, padx=5, pady=4, sticky="w")
            
            type_label = ctk.CTkLabel(
                type_frame,
                text=type_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="white",
                corner_radius=8
            )
            type_label.grid(row=0, column=0, padx=8, pady=2)
    
    def refresh_dashboard(self):
        """Refresh all dashboard components."""
        self.update_total_balance()
        self.update_account_count()
        self.update_recent_transactions()
    
    def create_account_card(self, account):
        """Create a card for an account."""
        card = ctk.CTkFrame(self.accounts_scrollable, corner_radius=10)
        card.pack(fill="x", padx=0, pady=5)
        
        # Account name
        name_label = ctk.CTkLabel(
            card,
            text=account.account_name,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.pack(side="top", anchor="nw", padx=10, pady=(10, 5))
        
        # Account type
        type_label = ctk.CTkLabel(
            card,
            text=account.account_type_name,
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        type_label.pack(side="top", anchor="nw", padx=10, pady=0)
        
        # Balance
        balance_text = f"${account.balance:,.2f}"
        balance_label = ctk.CTkLabel(
            card,
            text=balance_text,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        balance_label.pack(side="top", anchor="nw", padx=10, pady=(10, 10))
    
    def create_balance_history_chart(self):
        """Create a chart showing balance history."""
        # Set up the frame for the chart
        self.chart_frame = ctk.CTkFrame(self.history_frame, fg_color="transparent")
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Get balance history for the user's accounts for the past 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Sample data for the chart (would normally come from the database)
        # In a real implementation, you would aggregate balance history across all accounts
        # Here we'll create some sample data
        if self.accounts:
            account = self.accounts[0]  # Just use the first account for demonstration
            balance_history = Account.get_balance_history(account.id, start_date, end_date)
            
            # Extract dates and balances
            dates = [item['date'] for item in balance_history]
            balances = [float(item['balance']) for item in balance_history]
        else:
            # If no accounts, show empty chart
            dates = []
            balances = []
        
        if not dates:
            # Create sample data if no data available
            days = 30
            dates = [(end_date - timedelta(days=i)).date() for i in range(days, 0, -1)]
            balances = [self.total_balance] * len(dates)  # Flat line
        
        # Create a figure and axis
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        
        # Plot the data
        ax.plot(dates, balances, linewidth=2, color='#3a7ebf')
        ax.fill_between(dates, 0, balances, alpha=0.3, color='#3a7ebf')
        
        # Format the axis
        ax.tick_params(axis='x', colors='gray')
        ax.tick_params(axis='y', colors='gray')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('gray')
        ax.spines['left'].set_color('gray')
        
        # Format date labels
        date_format = '%m/%d'
        plt.xticks(rotation=45, ha='right')
        
        # Add $ signs to y-axis labels
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: f'${x:,.0f}')
        )
        
        # Adjust figure layout
        plt.tight_layout()
        
        # Embed the chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def create_transactions_table(self):
        """Create a table of recent transactions."""
        # Create scrollable frame for transactions
        self.transactions_scrollable = ctk.CTkScrollableFrame(
            self.transactions_frame, 
            fg_color="transparent",
            height=200
        )
        self.transactions_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Headers
        headers_frame = ctk.CTkFrame(self.transactions_scrollable, fg_color="transparent")
        headers_frame.pack(fill="x", padx=0, pady=(0, 5))
        headers_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Create headers
        headers = ["Date", "Description", "Category", "Amount"]
        for i, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                headers_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=("gray40", "gray60")
            )
            header_label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Get recent transactions
        transactions = Transaction.get_transactions_for_user(
            self.user.id, 
            limit=10, 
            include_details=True
        )
        
        # Add transactions to the table
        for i, transaction in enumerate(transactions):
            row_frame = ctk.CTkFrame(self.transactions_scrollable, fg_color="transparent")
            row_frame.pack(fill="x", padx=0, pady=2)
            row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
            
            # Date
            date_str = transaction.transaction_date.strftime("%m/%d/%Y")
            date_label = ctk.CTkLabel(
                row_frame,
                text=date_str,
                font=ctk.CTkFont(size=12)
            )
            date_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            # Description
            description = transaction.description or ""
            if transaction.transaction_type == "transfer":
                if transaction.recipient_account_id:
                    description = f"Transfer to {transaction.recipient_account_name}"
                else:
                    description = f"Transfer from {transaction.account_name}"
            elif transaction.transaction_type == "external_transfer":
                description = f"External transfer to {transaction.external_recipient}"
                
            description_label = ctk.CTkLabel(
                row_frame,
                text=description,
                font=ctk.CTkFont(size=12)
            )
            description_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")
            
            # Category
            category_text = transaction.category_name or "-"
            category_label = ctk.CTkLabel(
                row_frame,
                text=category_text,
                font=ctk.CTkFont(size=12)
            )
            category_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
            
            # Amount with appropriate color
            amount_text = f"${transaction.amount:,.2f}"
            amount_color = "#4CAF50"  # Green for deposits
            
            if transaction.transaction_type in ["withdrawal", "external_transfer"]:
                amount_text = f"-${transaction.amount:,.2f}"
                amount_color = "#F44336"  # Red for withdrawals
            elif transaction.transaction_type == "transfer":
                if transaction.account_id == int(transaction.account_id):
                    # Outgoing transfer
                    amount_text = f"-${transaction.amount:,.2f}"
                    amount_color = "#F44336"
                else:
                    # Incoming transfer
                    amount_color = "#4CAF50"
            
            amount_label = ctk.CTkLabel(
                row_frame,
                text=amount_text,
                text_color=amount_color,
                font=ctk.CTkFont(size=12)
            )
            amount_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")
            
            # Add a separator line
            separator = ctk.CTkFrame(self.transactions_scrollable, height=1, fg_color=("gray90", "gray20"))
            separator.pack(fill="x", padx=5, pady=0) 