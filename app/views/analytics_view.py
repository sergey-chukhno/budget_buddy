import customtkinter as ctk
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")
from datetime import datetime, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.transaction import Transaction
from app.models.account import Account

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
        
        # Analytics content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_columnconfigure((0, 1), weight=1)
        self.content_frame.grid_rowconfigure((0, 1), weight=1)
        
        # Placeholder for analytics sections
        self.placeholder = ctk.CTkLabel(
            self.content_frame,
            text="In a complete implementation, this view would display financial analytics including:\n\n"
                 "• Income vs. Expenses over time\n"
                 "• Spending by category\n"
                 "• Balance trends\n"
                 "• Monthly summaries\n\n"
                 "With interactive charts and filtering options.",
            wraplength=600
        )
        self.placeholder.pack(pady=100)
    
    def on_period_change(self, selection):
        """Handle time period change."""
        # In a complete implementation, this would update all the analytics charts
        print(f"Period changed to {selection}")
        
        # Refresh the view with the new period
        # Here we would recalculate all the analytics and update the charts 