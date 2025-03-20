import customtkinter as ctk
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")
from datetime import datetime, timedelta
import numpy as np

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.category import Category

class AnalyticsView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.user = user
        
        # Set up grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Analytics",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", padx=0, pady=0)
        
        # Time period selection dropdown
        self.periods = ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last Year", "All Time"]
        self.period_var = ctk.StringVar(value=self.periods[0])
        
        self.period_dropdown = ctk.CTkOptionMenu(
            self.header_frame,
            values=self.periods,
            variable=self.period_var,
            command=self.on_period_change
        )
        self.period_dropdown.pack(side="right", padx=0, pady=0)
        
        # Tab view for different analytics sections
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Create tabs
        self.overview_tab = self.tabview.add("Overview")
        self.revenues_tab = self.tabview.add("Revenues")
        self.expenses_tab = self.tabview.add("Expenses")
        
        # Set up grid for each tab
        for tab in [self.overview_tab, self.revenues_tab, self.expenses_tab]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)
        
        # Initialize charts in each tab
        self.setup_overview_tab()
        self.setup_revenues_tab()
        self.setup_expenses_tab()
        
        # Update analytics with current period
        self.update_analytics()
    
    def on_period_change(self, selection):
        """Handle time period change."""
        print(f"Period changed to {selection}")
        # Refresh analytics with the new period
        self.update_analytics()
    
    def setup_overview_tab(self):
        """Set up the overview tab with balance evolution chart."""
        # Create frame for balance evolution chart
        self.balance_chart_frame = ctk.CTkFrame(self.overview_tab)
        self.balance_chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Title for the chart
        self.balance_chart_title = ctk.CTkLabel(
            self.balance_chart_frame,
            text="Balance Evolution",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.balance_chart_title.pack(pady=(10, 0))
        
        # Placeholder for the chart
        self.balance_chart_placeholder = ctk.CTkFrame(self.balance_chart_frame, fg_color="transparent")
        self.balance_chart_placeholder.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_revenues_tab(self):
        """Set up the revenues tab with pie chart for revenue distribution by category."""
        # Create frame for revenue distribution chart
        self.revenue_chart_frame = ctk.CTkFrame(self.revenues_tab)
        self.revenue_chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Title for the chart
        self.revenue_chart_title = ctk.CTkLabel(
            self.revenue_chart_frame,
            text="Revenue Distribution by Category",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.revenue_chart_title.pack(pady=(10, 0))
        
        # Placeholder for the chart
        self.revenue_chart_placeholder = ctk.CTkFrame(self.revenue_chart_frame, fg_color="transparent")
        self.revenue_chart_placeholder.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_expenses_tab(self):
        """Set up the expenses tab with pie chart for expense distribution by category."""
        # Create frame for expense distribution chart
        self.expense_chart_frame = ctk.CTkFrame(self.expenses_tab)
        self.expense_chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Title for the chart
        self.expense_chart_title = ctk.CTkLabel(
            self.expense_chart_frame,
            text="Expense Distribution by Category",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.expense_chart_title.pack(pady=(10, 0))
        
        # Placeholder for the chart
        self.expense_chart_placeholder = ctk.CTkFrame(self.expense_chart_frame, fg_color="transparent")
        self.expense_chart_placeholder.pack(fill="both", expand=True, padx=10, pady=10)
    
    def get_date_range(self):
        """Get start and end dates based on current period selection."""
        end_date = datetime.now()
        period = self.period_var.get()
        
        if period == "Last 30 Days":
            start_date = end_date - timedelta(days=30)
        elif period == "Last 3 Months":
            start_date = end_date - timedelta(days=90)
        elif period == "Last 6 Months":
            start_date = end_date - timedelta(days=180)
        elif period == "Last Year":
            start_date = end_date - timedelta(days=365)
        else:  # All Time
            start_date = None
        
        return start_date, end_date
    
    def update_analytics(self):
        """Update all charts based on the current period selection."""
        self.update_balance_chart()
        self.update_revenue_chart()
        self.update_expense_chart()
    
    def update_balance_chart(self):
        """Update the balance evolution chart."""
        # Clear current chart
        for widget in self.balance_chart_placeholder.winfo_children():
            widget.destroy()
        
        # Get date range
        start_date, end_date = self.get_date_range()
        
        # Get all accounts for the user
        accounts = Account.get_accounts_for_user(self.user.id)
        
        if not accounts:
            # Show no data message
            no_data_label = ctk.CTkLabel(
                self.balance_chart_placeholder,
                text="No accounts found. Create an account to see balance evolution.",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_data_label.pack(pady=100)
            return
        
        # Get balance history for all accounts
        all_dates = set()
        account_balances = {}
        
        for account in accounts:
            history = Account.get_balance_history(account.id, start_date, end_date)
            if history:
                account_balances[account.id] = {item['date']: float(item['balance']) for item in history}
                all_dates.update(account_balances[account.id].keys())
        
        if not all_dates:
            # Create sample data if no data available
            if start_date is None:
                days = 30  # Default to 30 days for "All Time" if no data
                start_date = end_date - timedelta(days=days)
            
            # Create dates from start_date to end_date
            delta = end_date.date() - start_date.date()
            dates = [(end_date.date() - timedelta(days=i)) for i in range(delta.days, -1, -1)]
            
            # Get the current total balance across all accounts
            total_balance = sum(account.balance for account in accounts)
            balances = [total_balance] * len(dates)
        else:
            # Sort dates
            dates = sorted(all_dates)
            
            # Calculate total balance for each date
            balances = []
            for date in dates:
                total = 0
                for account_id, history in account_balances.items():
                    if date in history:
                        total += history[date]
                balances.append(total)
        
        # Create the chart
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
        
        # Add title
        period = self.period_var.get()
        ax.set_title(f"Balance Evolution - {period}", color='white', fontsize=12)
        
        # Adjust figure layout
        plt.tight_layout()
        
        # Embed the chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.balance_chart_placeholder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def update_revenue_chart(self):
        """Update the revenue distribution pie chart."""
        # Clear current chart
        for widget in self.revenue_chart_placeholder.winfo_children():
            widget.destroy()
        
        # Get date range
        start_date, end_date = self.get_date_range()
        
        # Get all transactions for income
        transactions = Transaction.get_transactions_for_user(
            self.user.id,
            start_date=start_date,
            end_date=end_date,
            transaction_type="deposit",
            include_details=True
        )
        
        if not transactions:
            # Show no data message
            no_data_label = ctk.CTkLabel(
                self.revenue_chart_placeholder,
                text="No revenue transactions found for the selected period.",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_data_label.pack(pady=100)
            return
        
        # Group transactions by category
        category_totals = {}
        for transaction in transactions:
            category_name = getattr(transaction, '_category_name', 'Uncategorized')
            if category_name in category_totals:
                category_totals[category_name] += float(transaction.amount)
            else:
                category_totals[category_name] = float(transaction.amount)
        
        # Sort categories by amount (descending)
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        # For visual clarity, limit to top 5 categories and group the rest as "Other"
        if len(sorted_categories) > 5:
            top_5 = sorted_categories[:5]
            other_amount = sum(amount for _, amount in sorted_categories[5:])
            if other_amount > 0:
                top_5.append(("Other", other_amount))
            categories, amounts = zip(*top_5)
        else:
            categories, amounts = zip(*sorted_categories)
        
        # Create chart
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        
        # Generate pleasant colors
        colors = plt.cm.viridis(np.linspace(0, 0.8, len(categories)))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            amounts, 
            labels=None, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': '#1a1a1a', 'linewidth': 1}
        )
        
        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
        
        # Add legend
        legend_labels = [f'{cat} (${amt:,.2f})' for cat, amt in zip(categories, amounts)]
        ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(0.9, 0.5))
        
        # Add title
        period = self.period_var.get()
        ax.set_title(f"Revenue by Category - {period}", color='white', fontsize=12)
        
        # Adjust figure layout
        plt.tight_layout()
        
        # Embed the chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.revenue_chart_placeholder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def update_expense_chart(self):
        """Update the expense distribution pie chart."""
        # Clear current chart
        for widget in self.expense_chart_placeholder.winfo_children():
            widget.destroy()
        
        # Get date range
        start_date, end_date = self.get_date_range()
        
        # Get all transactions for expenses
        transactions = Transaction.get_transactions_for_user(
            self.user.id,
            start_date=start_date,
            end_date=end_date,
            transaction_type="withdrawal",
            include_details=True
        )
        
        # Also get external transfers as expenses
        external_transfers = Transaction.get_transactions_for_user(
            self.user.id,
            start_date=start_date,
            end_date=end_date,
            transaction_type="external_transfer",
            include_details=True
        )
        
        # Combine both types of transactions
        transactions.extend(external_transfers)
        
        if not transactions:
            # Show no data message
            no_data_label = ctk.CTkLabel(
                self.expense_chart_placeholder,
                text="No expense transactions found for the selected period.",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_data_label.pack(pady=100)
            return
        
        # Group transactions by category
        category_totals = {}
        for transaction in transactions:
            category_name = getattr(transaction, '_category_name', 'Uncategorized')
            if category_name in category_totals:
                category_totals[category_name] += float(transaction.amount)
            else:
                category_totals[category_name] = float(transaction.amount)
        
        # Sort categories by amount (descending)
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        # For visual clarity, limit to top 5 categories and group the rest as "Other"
        if len(sorted_categories) > 5:
            top_5 = sorted_categories[:5]
            other_amount = sum(amount for _, amount in sorted_categories[5:])
            if other_amount > 0:
                top_5.append(("Other", other_amount))
            categories, amounts = zip(*top_5)
        else:
            categories, amounts = zip(*sorted_categories)
        
        # Create chart
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 6))
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        
        # Generate pleasant colors (using a different colormap for expenses)
        colors = plt.cm.magma(np.linspace(0, 0.8, len(categories)))
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            amounts, 
            labels=None, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': '#1a1a1a', 'linewidth': 1}
        )
        
        # Style the percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
        
        # Add legend
        legend_labels = [f'{cat} (${amt:,.2f})' for cat, amt in zip(categories, amounts)]
        ax.legend(wedges, legend_labels, loc='center left', bbox_to_anchor=(0.9, 0.5))
        
        # Add title
        period = self.period_var.get()
        ax.set_title(f"Expenses by Category - {period}", color='white', fontsize=12)
        
        # Adjust figure layout
        plt.tight_layout()
        
        # Embed the chart in the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.expense_chart_placeholder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True) 