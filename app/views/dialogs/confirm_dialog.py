import customtkinter as ctk

class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, message, callback=None):
        super().__init__(parent)
        
        self.parent = parent
        self.callback = callback
        self.message = message  # Store the message parameter
        
        # Set up the dialog window
        self.title(title)
        self.geometry("300x200")
        self.resizable(False, False)
        
        # Make dialog modal
        self.transient(parent)
        self.grab_set()
        
        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        # Create the dialog content
        self.create_widgets()
        
        # Make dialog modal and focus it
        self.focus_set()
        
        # Handle window close button
        self.protocol("WM_DELETE_WINDOW", self.cancel)
    
    def create_widgets(self):
        """Create the dialog widgets."""
        # Message label
        message_label = ctk.CTkLabel(
            self,
            text=self.message,
            wraplength=250
        )
        message_label.pack(pady=(30, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=(0, 20))
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            width=100,
            command=self.cancel
        )
        cancel_btn.pack(side="left", padx=10)
        
        # Confirm button
        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Confirm",
            width=100,
            fg_color="#E74C3C",  # Red color for delete confirmation
            command=self.confirm
        )
        confirm_btn.pack(side="left", padx=10)
    
    def confirm(self):
        """Handle confirmation."""
        if self.callback:
            self.callback(True)
        self.destroy()
    
    def cancel(self):
        """Handle cancellation."""
        if self.callback:
            self.callback(False)
        self.destroy() 