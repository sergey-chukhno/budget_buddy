import customtkinter as ctk
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.category import Category

class CategoriesView(ctk.CTkFrame):
    def __init__(self, master, user):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.user = user
        
        # Set up grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Categories",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", padx=0, pady=0)
        
        self.add_btn = ctk.CTkButton(
            self.header_frame,
            text="Add Category",
            command=self.add_category
        )
        self.add_btn.pack(side="right", padx=0, pady=0)
        
        # Filter section
        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Create a segmented button for filtering
        self.segment_values = ["All", "Income", "Expense"]
        self.segment = ctk.CTkSegmentedButton(
            self.filter_frame,
            values=self.segment_values,
            command=self.filter_changed
        )
        self.segment.pack(side="left", padx=10, pady=10)
        self.segment.set("All")
        
        # Search field
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            self.filter_frame,
            placeholder_text="Search categories...",
            width=200,
            textvariable=self.search_var
        )
        self.search_entry.pack(side="right", padx=10, pady=10)
        self.search_var.trace_add("write", self.on_search)
        
        # Categories content frame
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        # Placeholder for categories
        self.placeholder = ctk.CTkLabel(
            self.content_frame,
            text="In a complete implementation, this view would display all categories with options to:\n\n"
                 "• Create new categories\n"
                 "• Edit existing categories\n"
                 "• Delete categories\n"
                 "• View spending in each category\n"
                 "• Set budgets per category\n\n"
                 "Categories would be color-coded and organized by type (income/expense).",
            wraplength=600
        )
        self.placeholder.pack(pady=100)
    
    def add_category(self):
        """Open add category dialog."""
        print("Add category dialog would open here")
        # In a complete implementation, this would show the AddCategoryDialog
    
    def filter_changed(self, value):
        """Handle filter changes."""
        print(f"Filter changed to {value}")
        # In a complete implementation, this would filter the categories shown
    
    def on_search(self, *args):
        """Handle search input changes."""
        search_text = self.search_var.get()
        print(f"Searching for: {search_text}")
        # In a complete implementation, this would search the categories 