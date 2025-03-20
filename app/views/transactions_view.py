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
        self.grid_rowconfigure(1, weight=1)  # Changed from 2 to 1 since we'll use a main container
        
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
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Transactions",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=0, pady=0)
        
        # Export button
        self.export_button = ctk.CTkButton(
            self.header_frame,
            text="Export Report",
            width=120,
            command=self.export_report
        )
        self.export_button.grid(row=0, column=1, sticky="e", padx=0, pady=0)
        
        # Create filters frame and transactions table in a single container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(1, weight=1)  # Make table row expandable
        
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
        
        print(f"Refreshing transactions for User ID: {self.user.id}")
        
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
        
        print(f"Getting transactions with parameters: limit={self.page_size}, offset={offset}, account_id={account_id}, category_id={category_id}, type={transaction_type}")
        
        # Get transactions with filters
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
        
        # Define fixed column widths for better alignment
        col_widths = [120, 140, 140, 250, 140, 100, 140]
        
        # Get total count for pagination
        self.total_records = len(transactions)
        
        # Create header
        header_frame = ctk.CTkFrame(self.table_content, fg_color=("gray90", "gray25"))
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        # Configure the header frame's column weights
        for i in range(7):
            header_frame.grid_columnconfigure(i, weight=1, minsize=col_widths[i])
        
        # Header labels with sort functionality
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
                hover_color=("gray80", "gray30"),
                height=40,
                width=col_widths[i],
                anchor="w",
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda col=col_name: self.sort_by_column(col)
            )
            header_btn.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        # Separator after header
        header_separator = ctk.CTkFrame(self.table_content, height=2, fg_color="#3B8ED0")
        header_separator.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 10))
        
        if not transactions:
            no_data_label = ctk.CTkLabel(
                self.table_content,
                text="No transactions found with the current filters",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_data_label.grid(row=2, column=0, padx=20, pady=40)
            self.update_pagination_info()
            return
        
        # Create a main table frame for rows
        table_rows_frame = ctk.CTkFrame(self.table_content, fg_color="transparent")
        table_rows_frame.grid(row=2, column=0, sticky="nsew", padx=0, pady=0)
        table_rows_frame.grid_columnconfigure(0, weight=1)
        
        # Add transactions to the table
        for i, transaction in enumerate(transactions):
            try:
                # Format transaction data
                date_str = transaction.transaction_date.strftime("%Y-%m-%d %H:%M")
                account_name = getattr(transaction, '_account_name', 'N/A')
                category_name = getattr(transaction, '_category_name', 'N/A')
                description = transaction.description or ""
                
                # Recipient info
                recipient = ""
                if transaction.transaction_type == "transfer" and hasattr(transaction, '_recipient_account_name'):
                    recipient = transaction._recipient_account_name
                elif transaction.transaction_type == "external_transfer" and transaction.external_recipient:
                    recipient = transaction.external_recipient
                
                # Amount with color
                amount = float(transaction.amount)
                if transaction.transaction_type in ["withdrawal", "external_transfer", "transfer"] and transaction.account_id:
                    amount_text = f"-${amount:,.2f}"
                    amount_color = "#FF5252"  # Brighter red for dark theme
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
                
                # Create row frame with alternating background for dark theme
                row_bg = ("gray90", "gray20") if i % 2 == 0 else ("gray85", "gray17")
                row_frame = ctk.CTkFrame(table_rows_frame, fg_color=row_bg, corner_radius=0, height=40)
                row_frame.grid(row=i, column=0, sticky="ew", padx=0, pady=(0, 1))
                
                # Configure the row frame's column weights
                for j in range(7):
                    row_frame.grid_columnconfigure(j, weight=1, minsize=col_widths[j])
                
                # Make sure the row has a fixed height and doesn't resize
                row_frame.grid_propagate(False)
                
                # Add transaction data to row with consistent widths
                date_label = ctk.CTkLabel(row_frame, text=date_str, anchor="w", width=col_widths[0])
                date_label.grid(row=0, column=0, padx=5, pady=8, sticky="w")
                
                account_label = ctk.CTkLabel(row_frame, text=account_name, anchor="w", width=col_widths[1])
                account_label.grid(row=0, column=1, padx=5, pady=8, sticky="w")
                
                category_label = ctk.CTkLabel(row_frame, text=category_name, anchor="w", width=col_widths[2])
                category_label.grid(row=0, column=2, padx=5, pady=8, sticky="w")
                
                # Description with ellipsis if too long
                description_text = (description[:30] + '...') if len(description) > 30 else description
                desc_label = ctk.CTkLabel(row_frame, text=description_text, anchor="w", width=col_widths[3])
                desc_label.grid(row=0, column=3, padx=5, pady=8, sticky="w")
                
                recipient_label = ctk.CTkLabel(row_frame, text=recipient, anchor="w", width=col_widths[4])
                recipient_label.grid(row=0, column=4, padx=5, pady=8, sticky="w")
                
                amount_label = ctk.CTkLabel(
                    row_frame, 
                    text=amount_text, 
                    text_color=amount_color, 
                    anchor="e", 
                    width=col_widths[5],
                    font=ctk.CTkFont(weight="bold")
                )
                amount_label.grid(row=0, column=5, padx=5, pady=8, sticky="e")
                
                # Transaction type with styled background
                type_frame = ctk.CTkFrame(row_frame, fg_color=self._get_type_color(transaction.transaction_type), corner_radius=8)
                type_frame.grid(row=0, column=6, padx=5, pady=4, sticky="w")
                
                type_label = ctk.CTkLabel(
                    type_frame, 
                    text=type_text, 
                    text_color="white", 
                    anchor="w", 
                    font=ctk.CTkFont(size=12, weight="bold"),
                    corner_radius=8
                )
                type_label.grid(row=0, column=0, padx=8, pady=2)
                
            except Exception as e:
                print(f"Error displaying transaction {i+1}: {e}")
                import traceback
                traceback.print_exc()
        
        # Update pagination info
        self.update_pagination_info()

    def _get_type_color(self, transaction_type):
        """Get color based on transaction type for better visual distinction."""
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
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.grid(row=1, column=0, padx=0, pady=0, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)  # Changed to make scrollable frame expand
        
        # Total width of all columns plus some padding
        table_total_width = 1000
        
        # Table content with both vertical and horizontal scrolling
        self.table_content = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color=("gray95", "gray15"),  # Match theme colors
            height=500,  # Make it taller by default
            width=table_total_width,  # Set minimum width for horizontal scrolling
            orientation="vertical"  # Use vertical scrolling by default
        )
        self.table_content.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        
        # Pagination frame
        self.pagination_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.pagination_frame.grid(row=1, column=0, padx=0, pady=(10, 0), sticky="ew")
        self.pagination_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Previous page button
        self.prev_btn = ctk.CTkButton(
            self.pagination_frame,
            text="Previous",
            width=100,
            command=self.prev_page
        )
        self.prev_btn.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # Page information
        self.page_info = ctk.CTkLabel(
            self.pagination_frame,
            text="Page 1"
        )
        self.page_info.grid(row=0, column=1, padx=20, pady=5, sticky="w")
        
        # Next page button
        self.next_btn = ctk.CTkButton(
            self.pagination_frame,
            text="Next",
            width=100,
            command=self.next_page
        )
        self.next_btn.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        # Total records
        self.records_info = ctk.CTkLabel(
            self.pagination_frame,
            text="0 transactions"
        )
        self.records_info.grid(row=0, column=3, padx=20, pady=5, sticky="e")

    def create_filters_frame(self):
        """Create filters for the transactions table."""
        self.filters_frame = ctk.CTkFrame(self.main_container)
        self.filters_frame.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        
        # Create a grid layout for the filters
        self.filters_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.filters_frame.grid_rowconfigure((0, 1, 2), weight=0)  # Don't expand rows
        
        # Title for filters section
        filters_label = ctk.CTkLabel(
            self.filters_frame,
            text="Filter Transactions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        filters_label.grid(row=0, column=0, padx=10, pady=(15, 10), sticky="w")
        
        # Account filter with label in a single container
        account_container = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        account_container.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        account_label = ctk.CTkLabel(
            account_container, 
            text="Account:", 
            anchor="w",
            width=70
        )
        account_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        
        self.account_menu = ctk.CTkOptionMenu(
            account_container,
            variable=self.account_var,
            values=["All Accounts"],
            width=180,
            dynamic_resizing=False
        )
        self.account_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Category filter with label
        category_container = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        category_container.grid(row=1, column=2, columnspan=2, padx=10, pady=5, sticky="w")
        
        category_label = ctk.CTkLabel(
            category_container, 
            text="Category:", 
            anchor="w",
            width=70
        )
        category_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        
        self.category_menu = ctk.CTkOptionMenu(
            category_container,
            variable=self.category_var,
            values=["All Categories"],
            width=180,
            dynamic_resizing=False
        )
        self.category_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Transaction type filter with label
        type_container = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        type_container.grid(row=1, column=4, columnspan=2, padx=10, pady=5, sticky="w")
        
        type_label = ctk.CTkLabel(
            type_container, 
            text="Type:", 
            anchor="w",
            width=70
        )
        type_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        
        transaction_types = ["All Types", "Deposit", "Withdrawal", "Transfer", "External Transfer"]
        self.type_menu = ctk.CTkOptionMenu(
            type_container,
            variable=self.transaction_type_var,
            values=transaction_types,
            width=180,
            dynamic_resizing=False
        )
        self.type_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # Amount range with label
        amount_container = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        amount_container.grid(row=2, column=0, columnspan=2, padx=10, pady=(5, 15), sticky="w")
        
        amount_label = ctk.CTkLabel(
            amount_container, 
            text="Amount:", 
            anchor="w",
            width=70
        )
        amount_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        
        amount_inputs = ctk.CTkFrame(amount_container, fg_color="transparent")
        amount_inputs.grid(row=0, column=1, padx=0, pady=0, sticky="w")
        
        self.min_amount_entry = ctk.CTkEntry(
            amount_inputs,
            placeholder_text="Min",
            width=85,
            textvariable=self.min_amount_var
        )
        self.min_amount_entry.grid(row=0, column=0, padx=(0, 5), pady=5)
        
        amount_to_label = ctk.CTkLabel(amount_inputs, text="to", width=20)
        amount_to_label.grid(row=0, column=1, padx=5, pady=5)
        
        self.max_amount_entry = ctk.CTkEntry(
            amount_inputs,
            placeholder_text="Max",
            width=85,
            textvariable=self.max_amount_var
        )
        self.max_amount_entry.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # Search box with label
        search_container = ctk.CTkFrame(self.filters_frame, fg_color="transparent")
        search_container.grid(row=2, column=2, columnspan=2, padx=10, pady=(5, 15), sticky="w")
        
        search_label = ctk.CTkLabel(
            search_container, 
            text="Search:", 
            anchor="w",
            width=70
        )
        search_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
        
        self.search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text="Search in descriptions...",
            width=180,
            textvariable=self.search_var
        )
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Apply filters button
        self.apply_btn = ctk.CTkButton(
            self.filters_frame,
            text="Apply Filters",
            width=120,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(weight="bold"),
            command=self.refresh_transactions
        )
        self.apply_btn.grid(row=2, column=4, padx=10, pady=(5, 15), sticky="e")
        
        # Reset filters button
        self.reset_btn = ctk.CTkButton(
            self.filters_frame,
            text="Reset",
            width=80,
            height=35,
            corner_radius=8,
            fg_color="gray60",
            hover_color="gray50",
            command=self.reset_filters
        )
        self.reset_btn.grid(row=2, column=5, padx=10, pady=(5, 15), sticky="w")
        
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
    
    def reset_filters(self):
        """Reset all filters to default values and refresh the transactions."""
        self.account_var.set("All Accounts")
        self.category_var.set("All Categories")
        self.transaction_type_var.set("All Types")
        self.search_var.set("")
        self.min_amount_var.set("")
        self.max_amount_var.set("")
        
        # Reset to first page
        self.current_page = 1
        
        # Refresh with reset filters
        self.refresh_transactions() 