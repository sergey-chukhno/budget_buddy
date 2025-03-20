import customtkinter as ctk
import sys
import os
from datetime import datetime, timedelta
import tkinter as tk

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.transaction import Transaction
from app.models.category import Category
from app.models.account import Account

class TransactionsView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.user = user
        
        # Set up grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Initialize variables
        self.current_page = 1
        self.page_size = 20
        self.total_records = 0
        self.sort_column = "transaction_date"
        self.sort_direction = "DESC"
        
        # Filter variables
        self.start_date_var = tk.StringVar()
        self.end_date_var = tk.StringVar()
        self.account_var = tk.StringVar(value="All Accounts")
        self.category_var = tk.StringVar(value="All Categories")
        self.transaction_type_var = tk.StringVar(value="All Types")
        self.search_var = tk.StringVar()
        self.min_amount_var = tk.StringVar()
        self.max_amount_var = tk.StringVar()
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Transactions",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", padx=0, pady=0)
        
        # Export button
        self.export_button = ctk.CTkButton(
            self.header_frame,
            text="Export Report",
            width=120,
            command=self.export_report
        )
        self.export_button.pack(side="right", padx=0, pady=0)
        
        # Create filters frame
        self.create_filters_frame()
        
        # Create the transactions table
        self.create_transactions_table()
        
        # Load initial data
        self.refresh_transactions()
    
    def export_report(self):
        """Generate and export a transactions report."""
        # In a complete implementation, this would generate a PDF or CSV report
        print("Export report functionality would be implemented here")

    def refresh_transactions(self):
        """Refresh the transactions table with current filters."""
        # Clear existing rows
        for widget in self.table_content.winfo_children():
            widget.destroy()
        
        print("Refreshing transactions...")
        
        # Prepare filter parameters
        start_date = self.start_date_var.get() if self.start_date_var.get() else None
        end_date = self.end_date_var.get() if self.end_date_var.get() else None
        
        # Get account ID if a specific account is selected
        account_id = None
        if self.account_var.get() != "All Accounts":
            accounts = Account.get_accounts_for_user(self.user.id)
            for account in accounts:
                if account.account_name == self.account_var.get():
                    account_id = account.id
                    break
        
        # Get category ID if a specific category is selected
        category_id = None
        if self.category_var.get() != "All Categories":
            all_categories = Category.get_categories_by_type(self.user.id, "income") + Category.get_categories_by_type(self.user.id, "expense")
            for category in all_categories:
                if category.category_name == self.category_var.get():
                    category_id = category.id
                    break
        
        # Get transaction type
        transaction_type = None
        if self.transaction_type_var.get() != "All Types":
            type_map = {
                "Deposit": "deposit",
                "Withdrawal": "withdrawal",
                "Transfer": "transfer",
                "External Transfer": "external_transfer"
            }
            transaction_type = type_map.get(self.transaction_type_var.get())
        
        # Amount range
        min_amount = self.min_amount_var.get() if self.min_amount_var.get() else None
        max_amount = self.max_amount_var.get() if self.max_amount_var.get() else None
        
        try:
            if min_amount:
                min_amount = float(min_amount)
            if max_amount:
                max_amount = float(max_amount)
        except ValueError:
            # Handle invalid input for amount filters
            min_amount = None
            max_amount = None
        
        # Search term
        search_term = self.search_var.get() if self.search_var.get() else None
        
        # Calculate offset for pagination
        offset = (self.current_page - 1) * self.page_size
        
        # Get transactions with filters
        print(f"User ID: {self.user.id}")
        print(f"Fetching transactions with: limit={self.page_size}, offset={offset}, order_by={self.sort_column}, order_dir={self.sort_direction}")
        
        transactions = Transaction.get_transactions_for_user(
            self.user.id,
            limit=self.page_size,
            offset=offset,
            start_date=start_date,
            end_date=end_date,
            category_id=category_id,
            search_term=search_term,
            transaction_type=transaction_type,
            min_amount=min_amount,
            max_amount=max_amount,
            account_id=account_id,
            include_details=True,
            order_by=self.sort_column,
            order_dir=self.sort_direction
        )
        
        print(f"Found {len(transactions)} transactions")
        
        # Get total count for pagination
        # In a real implementation, you would have a separate count method
        # For now, we'll use the length of transactions as an approximation
        self.total_records = len(transactions)
        
        # Create header
        header_frame = ctk.CTkFrame(self.table_content, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=7, sticky="ew", padx=0, pady=(0, 10))
        header_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        
        # Header labels with sort functionality
        header_labels = ["Date", "Account", "Category", "Description", "Recipient", "Amount", "Type"]
        column_data = [
            ("transaction_date", "Date"),
            ("account_id", "Account"),
            ("category_id", "Category"),
            ("description", "Description"),
            ("external_recipient", "Recipient"),
            ("amount", "Amount"),
            ("transaction_type", "Type")
        ]
        
        for i, (col_name, label_text) in enumerate(column_data):
            # Add sort indicator if this column is being sorted
            if self.sort_column == col_name:
                indicator = "▲" if self.sort_direction == "ASC" else "▼"
                display_text = f"{label_text} {indicator}"
            else:
                display_text = label_text
                
            # Create clickable header label
            header_btn = ctk.CTkButton(
                header_frame,
                text=display_text,
                fg_color="transparent",
                hover_color=("#E1E1E1", "#333333"),
                height=32,
                anchor="w",
                command=lambda col=col_name: self.sort_by_column(col)
            )
            header_btn.grid(row=0, column=i, sticky="ew", padx=5)
        
        # Separator after header
        header_separator = ctk.CTkFrame(self.table_content, height=2, fg_color="#3B8ED0")
        header_separator.grid(row=1, column=0, columnspan=7, sticky="ew", padx=5, pady=(0, 10))
        
        if not transactions:
            no_data_label = ctk.CTkLabel(
                self.table_content,
                text="No transactions found with the current filters",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_data_label.grid(row=2, column=0, columnspan=7, padx=20, pady=40)
            self.update_pagination_info()
            return
        
        # Add transactions to the table
        for i, transaction in enumerate(transactions):
            # Format transaction data
            date_str = transaction.transaction_date.strftime("%Y-%m-%d %H:%M")
            account_name = transaction._account_name or "N/A"
            category_name = transaction._category_name or "N/A"
            description = transaction.description or ""
            
            # Recipient info
            recipient = ""
            if transaction.transaction_type == "transfer" and transaction._recipient_account_name:
                recipient = transaction._recipient_account_name
            elif transaction.transaction_type == "external_transfer" and transaction.external_recipient:
                recipient = transaction.external_recipient
            
            # Amount with color
            amount = float(transaction.amount)
            if transaction.transaction_type in ["withdrawal", "external_transfer", "transfer"] and transaction.account_id:
                amount_text = f"-${amount:,.2f}"
                amount_color = "#F44336"  # Red
            else:
                amount_text = f"${amount:,.2f}"
                amount_color = "#4CAF50"  # Green
            
            # Transaction type display
            type_map = {
                "deposit": "Deposit",
                "withdrawal": "Withdrawal",
                "transfer": "Transfer",
                "external_transfer": "External Transfer"
            }
            type_text = type_map.get(transaction.transaction_type, transaction.transaction_type)
            
            # Create row frame with alternating background
            row_bg = "#F5F5F5" if i % 2 == 0 else "#FFFFFF"
            row_frame = ctk.CTkFrame(self.table_content, fg_color=row_bg, corner_radius=0)
            row_frame.grid(row=i+2, column=0, columnspan=7, sticky="ew", padx=0, pady=0)
            row_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
            
            # Add transaction data to row
            ctk.CTkLabel(row_frame, text=date_str, anchor="w").grid(row=0, column=0, padx=5, pady=8, sticky="w")
            ctk.CTkLabel(row_frame, text=account_name, anchor="w").grid(row=0, column=1, padx=5, pady=8, sticky="w")
            ctk.CTkLabel(row_frame, text=category_name, anchor="w").grid(row=0, column=2, padx=5, pady=8, sticky="w")
            ctk.CTkLabel(row_frame, text=description, anchor="w").grid(row=0, column=3, padx=5, pady=8, sticky="w")
            ctk.CTkLabel(row_frame, text=recipient, anchor="w").grid(row=0, column=4, padx=5, pady=8, sticky="w")
            
            amount_label = ctk.CTkLabel(row_frame, text=amount_text, text_color=amount_color, anchor="e")
            amount_label.grid(row=0, column=5, padx=5, pady=8, sticky="e")
            
            ctk.CTkLabel(row_frame, text=type_text, anchor="w").grid(row=0, column=6, padx=5, pady=8, sticky="w")
            
            # Add a separator line
            separator = ctk.CTkFrame(self.table_content, height=1, fg_color="#E0E0E0")
            separator.grid(row=i+3, column=0, columnspan=7, sticky="ew", padx=0, pady=0)
        
        # Update pagination info
        self.update_pagination_info()

    def sort_by_column(self, column_name):
        """Sort the transactions by the selected column."""
        # Toggle direction if same column is clicked again
        if self.sort_column == column_name:
            self.sort_direction = "ASC" if self.sort_direction == "DESC" else "DESC"
        else:
            self.sort_column = column_name
            self.sort_direction = "ASC"
        
        # Reset to first page when sorting changes
        self.current_page = 1
        
        # Refresh with new sorting
        self.refresh_transactions()

    def create_transactions_table(self):
        """Create the transactions table."""
        # Main content frame 
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)
        
        # Table header frame (will be populated in refresh_transactions)
        self.table_header = ctk.CTkFrame(self.content_frame)
        self.table_header.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        
        # Table content (scrollable)
        self.table_content = ctk.CTkScrollableFrame(self.content_frame)
        self.table_content.grid(row=1, column=0, padx=0, pady=(0, 10), sticky="nsew")
        
        # Pagination frame
        self.pagination_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.pagination_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Previous page button
        self.prev_btn = ctk.CTkButton(
            self.pagination_frame,
            text="Previous",
            width=100,
            command=self.prev_page
        )
        self.prev_btn.pack(side="left", padx=5, pady=5)
        
        # Page information
        self.page_info = ctk.CTkLabel(
            self.pagination_frame,
            text="Page 1"
        )
        self.page_info.pack(side="left", padx=20, pady=5)
        
        # Next page button
        self.next_btn = ctk.CTkButton(
            self.pagination_frame,
            text="Next",
            width=100,
            command=self.next_page
        )
        self.next_btn.pack(side="left", padx=5, pady=5)
        
        # Total records
        self.records_info = ctk.CTkLabel(
            self.pagination_frame,
            text="0 transactions"
        )
        self.records_info.pack(side="right", padx=20, pady=5)

    def create_filters_frame(self):
        """Create filters for the transactions table."""
        self.filters_frame = ctk.CTkFrame(self)
        self.filters_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Create a grid layout for the filters
        self.filters_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.filters_frame.grid_rowconfigure((0, 1, 2), weight=1)
        
        # Title for filters section
        filters_label = ctk.CTkLabel(
            self.filters_frame,
            text="Filters",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        filters_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # Account filter
        account_label = ctk.CTkLabel(self.filters_frame, text="Account:", anchor="w")
        account_label.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="w")
        
        self.account_menu = ctk.CTkOptionMenu(
            self.filters_frame,
            variable=self.account_var,
            values=["All Accounts"],
            width=150
        )
        self.account_menu.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Category filter
        category_label = ctk.CTkLabel(self.filters_frame, text="Category:", anchor="w")
        category_label.grid(row=1, column=2, padx=(10, 5), pady=5, sticky="w")
        
        self.category_menu = ctk.CTkOptionMenu(
            self.filters_frame,
            variable=self.category_var,
            values=["All Categories"],
            width=150
        )
        self.category_menu.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        
        # Transaction type filter
        type_label = ctk.CTkLabel(self.filters_frame, text="Type:", anchor="w")
        type_label.grid(row=1, column=4, padx=(10, 5), pady=5, sticky="w")
        
        transaction_types = ["All Types", "Deposit", "Withdrawal", "Transfer", "External Transfer"]
        self.type_menu = ctk.CTkOptionMenu(
            self.filters_frame,
            variable=self.transaction_type_var,
            values=transaction_types,
            width=150
        )
        self.type_menu.grid(row=1, column=5, padx=5, pady=5, sticky="w")
        
        # Amount range
        amount_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        amount_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        amount_label = ctk.CTkLabel(amount_frame, text="Amount:", anchor="w")
        amount_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        
        self.min_amount_entry = ctk.CTkEntry(
            amount_frame,
            placeholder_text="Min",
            width=80,
            textvariable=self.min_amount_var
        )
        self.min_amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        amount_to_label = ctk.CTkLabel(amount_frame, text="to")
        amount_to_label.grid(row=0, column=2, padx=5, pady=5)
        
        self.max_amount_entry = ctk.CTkEntry(
            amount_frame,
            placeholder_text="Max",
            width=80,
            textvariable=self.max_amount_var
        )
        self.max_amount_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Search box
        search_frame = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        search_frame.grid(row=2, column=2, columnspan=2, padx=10, pady=5, sticky="w")
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search...",
            width=150,
            textvariable=self.search_var
        )
        self.search_entry.grid(row=0, column=0, padx=5, pady=5)
        
        # Apply filters button
        self.apply_btn = ctk.CTkButton(
            search_frame,
            text="Apply Filters",
            width=120,
            command=self.refresh_transactions
        )
        self.apply_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Load account and category options
        self.load_filter_options()
    
    def load_filter_options(self):
        """Load account and category options for filters."""
        # Get all user accounts
        accounts = Account.get_accounts_for_user(self.user.id)
        account_options = ["All Accounts"] + [account.account_name for account in accounts]
        self.account_menu.configure(values=account_options)
        
        # Get all categories
        income_categories = Category.get_categories_by_type(self.user.id, "income")
        expense_categories = Category.get_categories_by_type(self.user.id, "expense")
        category_options = ["All Categories"] + [cat.category_name for cat in income_categories + expense_categories]
        self.category_menu.configure(values=category_options)
    
    def update_pagination_info(self):
        """Update pagination information."""
        self.page_info.configure(text=f"Page {self.current_page}")
        self.records_info.configure(text=f"{self.total_records} transactions")
        
        # Enable/disable pagination buttons based on current page
        if self.current_page <= 1:
            self.prev_btn.configure(state="disabled")
        else:
            self.prev_btn.configure(state="normal")
        
        if self.current_page >= self.total_records / self.page_size:
            self.next_btn.configure(state="disabled")
        else:
            self.next_btn.configure(state="normal")
    
    def next_page(self):
        """Go to the next page."""
        if self.current_page < self.total_records / self.page_size:
            self.current_page += 1
            self.refresh_transactions()
    
    def prev_page(self):
        """Go to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_transactions() 