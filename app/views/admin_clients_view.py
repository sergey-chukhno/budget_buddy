import customtkinter as ctk
import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import models
from app.models.user import User
from app.models.account import Account

class AdminClientsView(ctk.CTkFrame):
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
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=0)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Clients Management",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Add client button
        self.add_client_btn = ctk.CTkButton(
            self.header_frame,
            text="Add Client",
            command=self.add_client
        )
        self.add_client_btn.grid(row=0, column=1, padx=10)
        
        # Search frame
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search clients...",
            width=300
        )
        self.search_entry.pack(side="left", padx=(20, 10), pady=10)
        
        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100,
            command=self.search_clients
        )
        self.search_btn.pack(side="left", padx=10, pady=10)
        
        # Clients list
        self.clients_frame = ctk.CTkFrame(self)
        self.clients_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.clients_frame.grid_columnconfigure(0, weight=1)
        self.clients_frame.grid_rowconfigure(0, weight=1)
        
        # Create table header
        self.create_clients_table()
        
        # Load clients data
        self.load_clients()
    
    def create_clients_table(self):
        # Column widths
        col_widths = [80, 150, 150, 200, 120, 200]
        
        # Table header
        header_frame = ctk.CTkFrame(self.clients_frame, fg_color=("gray90", "gray25"))
        header_frame.pack(fill="x", pady=(0, 2))
        
        # Configure header columns
        for i in range(6):
            header_frame.grid_columnconfigure(i, weight=1, minsize=col_widths[i])
        
        # Header labels
        header_labels = ["ID", "First Name", "Last Name", "Email", "Phone", "Actions"]
        for i, label_text in enumerate(header_labels):
            header_label = ctk.CTkLabel(
                header_frame,
                text=label_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w"
            )
            header_label.grid(row=0, column=i, sticky="w", padx=10, pady=10)
        
        # Scrollable frame for the table content
        self.table_content = ctk.CTkScrollableFrame(self.clients_frame, fg_color="transparent")
        self.table_content.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Configure content frame
        self.table_content.grid_columnconfigure(0, weight=1)
    
    def load_clients(self):
        """Load all clients assigned to the admin."""
        # Clear existing clients
        for widget in self.table_content.winfo_children():
            widget.destroy()
        
        # Get clients data
        clients = User.get_clients_for_admin(self.user.id)
        
        if not clients:
            no_clients_label = ctk.CTkLabel(
                self.table_content,
                text="No clients found",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            no_clients_label.pack(pady=40)
            return
        
        # Column widths (same as header)
        col_widths = [80, 150, 150, 200, 120, 200]
        
        # Add each client
        for i, client in enumerate(clients):
            # Row frame with alternating background
            row_bg = ("gray90", "gray20") if i % 2 == 0 else ("gray85", "gray17")
            row_frame = ctk.CTkFrame(self.table_content, fg_color=row_bg, corner_radius=0, height=50)
            row_frame.pack(fill="x", pady=(0, 1))
            row_frame.grid_propagate(False)
            
            # Configure columns
            for j in range(6):
                row_frame.grid_columnconfigure(j, weight=1, minsize=col_widths[j])
            
            # Client ID
            id_label = ctk.CTkLabel(
                row_frame,
                text=str(client.id),
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            id_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
            
            # First Name
            first_name_label = ctk.CTkLabel(
                row_frame,
                text=client.first_name,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            first_name_label.grid(row=0, column=1, sticky="w", padx=10, pady=10)
            
            # Last Name
            last_name_label = ctk.CTkLabel(
                row_frame,
                text=client.last_name,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            last_name_label.grid(row=0, column=2, sticky="w", padx=10, pady=10)
            
            # Email
            email_label = ctk.CTkLabel(
                row_frame,
                text=client.email,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            email_label.grid(row=0, column=3, sticky="w", padx=10, pady=10)
            
            # Phone (would need to be added to the User model)
            phone_label = ctk.CTkLabel(
                row_frame,
                text="N/A",  # This should come from the user object
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            phone_label.grid(row=0, column=4, sticky="w", padx=10, pady=10)
            
            # Action buttons frame
            action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_frame.grid(row=0, column=5, sticky="ew", padx=10, pady=5)
            
            # View button
            view_btn = ctk.CTkButton(
                action_frame,
                text="View",
                font=ctk.CTkFont(size=12),
                width=60,
                height=25,
                fg_color="#4CAF50",
                hover_color="#388E3C",
                command=lambda client_id=client.id: self.view_client(client_id)
            )
            view_btn.pack(side="left", padx=(0, 5))
            
            # Edit button
            edit_btn = ctk.CTkButton(
                action_frame,
                text="Edit",
                font=ctk.CTkFont(size=12),
                width=60,
                height=25,
                fg_color="#2196F3",
                hover_color="#1976D2",
                command=lambda client_id=client.id: self.edit_client(client_id)
            )
            edit_btn.pack(side="left", padx=5)
            
            # Delete button
            delete_btn = ctk.CTkButton(
                action_frame,
                text="Delete",
                font=ctk.CTkFont(size=12),
                width=60,
                height=25,
                fg_color="#F44336",
                hover_color="#D32F2F",
                command=lambda client_id=client.id: self.delete_client(client_id)
            )
            delete_btn.pack(side="left", padx=5)
    
    def add_client(self):
        """Open a dialog to add a new client."""
        # This would open a dialog to register a new client
        # For now, just a placeholder
        print("Add client dialog would open here")
    
    def search_clients(self):
        """Search clients based on search entry."""
        # This would search for clients matching the search term
        # For now, just a placeholder
        search_term = self.search_entry.get()
        print(f"Searching for clients with term: {search_term}")
        self.load_clients()  # Reload all clients for now
    
    def view_client(self, client_id):
        """View client details."""
        print(f"Viewing client with ID: {client_id}")
    
    def edit_client(self, client_id):
        """Edit client details."""
        print(f"Editing client with ID: {client_id}")
    
    def delete_client(self, client_id):
        """Delete a client."""
        print(f"Deleting client with ID: {client_id}") 