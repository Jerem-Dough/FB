"""
Main GUI window for Facebook Marketplace Automation
"""
import customtkinter as ctk
from gui.workflow_editor import WorkflowEditor
from gui.queue_manager import QueueManager
from gui.settings_window import SettingsWindow
from database.db import Database
from config.config import Config

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize
        self.title("Facebook Marketplace Automation")
        self.geometry("1200x700")
        
        # Initialize database and config
        self.db = Database()
        self.config = Config()
        
        # Setup UI
        self.setup_ui()
        
        # Check if Chrome profile is configured
        if not self.config.get('chrome_profile_path'):
            self.after(500, self.show_first_time_setup)
    
    def setup_ui(self):
        """Setup the main UI layout"""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="FB Marketplace\nAutomation",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Navigation buttons
        self.workflows_btn = ctk.CTkButton(
            self.sidebar,
            text="Workflows",
            command=self.show_workflows,
            font=ctk.CTkFont(size=14)
        )
        self.workflows_btn.grid(row=1, column=0, padx=20, pady=10)
        
        self.queue_btn = ctk.CTkButton(
            self.sidebar,
            text="Posting Queue",
            command=self.show_queue,
            font=ctk.CTkFont(size=14)
        )
        self.queue_btn.grid(row=2, column=0, padx=20, pady=10)
        
        self.settings_btn = ctk.CTkButton(
            self.sidebar,
            text="Settings",
            command=self.show_settings,
            font=ctk.CTkFont(size=14)
        )
        self.settings_btn.grid(row=3, column=0, padx=20, pady=10)
        
        # Status indicator
        self.status_label = ctk.CTkLabel(
            self.sidebar,
            text="Status: Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=7, column=0, padx=20, pady=(10, 20))
        
        # Main content area
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Show workflows by default
        self.current_view = None
        self.show_workflows()
    
    def show_workflows(self):
        """Show workflows view"""
        self.clear_content()
        self.current_view = WorkflowEditor(self.content_frame, self.db, self.config)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.highlight_button(self.workflows_btn)
    
    def show_queue(self):
        """Show queue view"""
        self.clear_content()
        self.current_view = QueueManager(self.content_frame, self.db, self.config, self.update_status)
        self.current_view.grid(row=0, column=0, sticky="nsew")
        self.highlight_button(self.queue_btn)
    
    def show_settings(self):
        """Show settings window"""
        SettingsWindow(self, self.config)
    
    def show_first_time_setup(self):
        """Show first-time setup dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("First Time Setup")
        dialog.geometry("600x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"600x400+{x}+{y}")
        
        # Content
        label = ctk.CTkLabel(
            dialog,
            text="Welcome to Facebook Marketplace Automation!",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label.pack(pady=(30, 20))
        
        info = ctk.CTkLabel(
            dialog,
            text="To get started, we need to know where your Chrome profile is located.\n"
                 "This allows the bot to use your existing Facebook login.\n\n"
                 "Common locations:\n"
                 "Windows: C:\\Users\\YourName\\AppData\\Local\\Google\\Chrome\\User Data\n"
                 "Mac: ~/Library/Application Support/Google/Chrome\n"
                 "Linux: ~/.config/google-chrome",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info.pack(pady=20, padx=30)
        
        entry = ctk.CTkEntry(dialog, width=500, placeholder_text="Chrome profile path")
        entry.pack(pady=10)
        
        def browse_folder():
            from tkinter import filedialog
            folder = filedialog.askdirectory(title="Select Chrome User Data folder")
            if folder:
                entry.delete(0, 'end')
                entry.insert(0, folder)
        
        browse_btn = ctk.CTkButton(dialog, text="Browse", command=browse_folder, width=100)
        browse_btn.pack(pady=10)
        
        def save_and_close():
            path = entry.get().strip()
            if path:
                self.config.set('chrome_profile_path', path)
                dialog.destroy()
            else:
                error_label = ctk.CTkLabel(dialog, text="Please enter a valid path", text_color="red")
                error_label.pack()
        
        save_btn = ctk.CTkButton(
            dialog,
            text="Save and Continue",
            command=save_and_close,
            font=ctk.CTkFont(size=14)
        )
        save_btn.pack(pady=20)
        
        skip_btn = ctk.CTkButton(
            dialog,
            text="Skip for now",
            command=dialog.destroy,
            fg_color="gray",
            font=ctk.CTkFont(size=12)
        )
        skip_btn.pack()
    
    def clear_content(self):
        """Clear current content view"""
        if self.current_view:
            self.current_view.destroy()
    
    def highlight_button(self, button):
        """Highlight the active navigation button"""
        for btn in [self.workflows_btn, self.queue_btn]:
            btn.configure(fg_color=("gray75", "gray25"))
        button.configure(fg_color=("gray85", "gray40"))
    
    def update_status(self, text):
        """Update status label"""
        self.status_label.configure(text=f"Status: {text}")
    
    def run(self):
        """Run the application"""
        self.mainloop()
