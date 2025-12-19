"""
Settings window interface
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent, config):
        super().__init__(parent)
        
        self.config = config

        self.title("Settings")
        self.geometry("600x600")
        self.transient(parent)
        self.grab_set()

        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"600x600+{x}+{y}")

        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the settings UI"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(20, 30))
        
        # Scrollable frame for settings
        settings_frame = ctk.CTkScrollableFrame(self, width=550, height=400)
        settings_frame.pack(pady=10, padx=20, fill="both", expand=False)
        
        # Chrome Profile Path
        ctk.CTkLabel(
            settings_frame,
            text="Chrome Profile Path:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5))
        
        ctk.CTkLabel(
            settings_frame,
            text="Location of your Chrome user data folder (contains your login)",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w")
        
        path_frame = ctk.CTkFrame(settings_frame)
        path_frame.pack(fill="x", pady=5)
        path_frame.grid_columnconfigure(0, weight=1)
        
        self.chrome_path_entry = ctk.CTkEntry(path_frame, width=400)
        self.chrome_path_entry.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        browse_btn = ctk.CTkButton(
            path_frame,
            text="Browse",
            command=self.browse_chrome_path,
            width=100
        )
        browse_btn.grid(row=0, column=1)
        
        # Delays
        ctk.CTkLabel(
            settings_frame,
            text="Posting Delays:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(20, 5))

        ctk.CTkLabel(
            settings_frame,
            text="Random delay between posts (helps avoid detection)",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w")

        delay_frame = ctk.CTkFrame(settings_frame)
        delay_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(delay_frame, text="Minimum:").pack(side="left", padx=5)
        self.min_delay_entry = ctk.CTkEntry(delay_frame, width=80)
        self.min_delay_entry.pack(side="left", padx=5)

        self.min_delay_unit = ctk.StringVar(value="minutes")
        min_unit_menu = ctk.CTkOptionMenu(
            delay_frame,
            variable=self.min_delay_unit,
            values=["seconds", "minutes", "hours"],
            width=100
        )
        min_unit_menu.pack(side="left", padx=5)

        ctk.CTkLabel(delay_frame, text="Maximum:").pack(side="left", padx=5)
        self.max_delay_entry = ctk.CTkEntry(delay_frame, width=80)
        self.max_delay_entry.pack(side="left", padx=5)

        self.max_delay_unit = ctk.StringVar(value="minutes")
        max_unit_menu = ctk.CTkOptionMenu(
            delay_frame,
            variable=self.max_delay_unit,
            values=["seconds", "minutes", "hours"],
            width=100
        )
        max_unit_menu.pack(side="left", padx=5)
        
        # Default Settings
        ctk.CTkLabel(
            settings_frame,
            text="Default Listing Settings:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(20, 5))
        
        # Location
        ctk.CTkLabel(settings_frame, text="Default Location:").pack(anchor="w", pady=(5, 2))
        self.location_entry = ctk.CTkEntry(settings_frame, width=300)
        self.location_entry.pack(anchor="w", pady=(0, 10))
        
        # Category
        ctk.CTkLabel(settings_frame, text="Default Category:").pack(anchor="w", pady=(5, 2))
        self.category_var = ctk.StringVar(value="Home & Garden")
        category_menu = ctk.CTkOptionMenu(
            settings_frame,
            variable=self.category_var,
            values=["Home & Garden", "Vehicles", "Electronics", "Clothing & Accessories", 
                   "Entertainment", "Family", "Hobbies", "Other"]
        )
        category_menu.pack(anchor="w", pady=(0, 10))
        
        # Condition
        ctk.CTkLabel(settings_frame, text="Default Condition:").pack(anchor="w", pady=(5, 2))
        self.condition_var = ctk.StringVar(value="New")
        condition_menu = ctk.CTkOptionMenu(
            settings_frame,
            variable=self.condition_var,
            values=["New", "Used - Like New", "Used - Good", "Used - Fair"]
        )
        condition_menu.pack(anchor="w", pady=(0, 10))
        
        # Images per listing
        ctk.CTkLabel(settings_frame, text="Images per Listing (default):").pack(anchor="w", pady=(5, 2))
        self.images_per_entry = ctk.CTkEntry(settings_frame, width=80)
        self.images_per_entry.pack(anchor="w", pady=(0, 10))
        
        # Buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Settings",
            command=self.save_settings,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150
        )
        save_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="gray",
            width=100
        )
        cancel_btn.pack(side="left", padx=10)
    
    def browse_chrome_path(self):
        """Browse for Chrome profile folder"""
        folder = filedialog.askdirectory(title="Select Chrome User Data folder")
        if folder:
            self.chrome_path_entry.delete(0, 'end')
            self.chrome_path_entry.insert(0, folder)
    
    def load_settings(self):
        """Load current settings into form"""
        self.chrome_path_entry.insert(0, self.config.get('chrome_profile_path', ''))

        # Load delay times (stored in seconds, display in friendly units)
        min_delay_seconds = self.config.get('min_delay_between_posts', 60)
        max_delay_seconds = self.config.get('max_delay_between_posts', 180)

        # Convert to friendly units (default to minutes for display)
        if min_delay_seconds >= 3600 and min_delay_seconds % 3600 == 0:
            self.min_delay_entry.insert(0, str(min_delay_seconds // 3600))
            self.min_delay_unit.set("hours")
        elif min_delay_seconds >= 60 and min_delay_seconds % 60 == 0:
            self.min_delay_entry.insert(0, str(min_delay_seconds // 60))
            self.min_delay_unit.set("minutes")
        else:
            self.min_delay_entry.insert(0, str(min_delay_seconds))
            self.min_delay_unit.set("seconds")

        if max_delay_seconds >= 3600 and max_delay_seconds % 3600 == 0:
            self.max_delay_entry.insert(0, str(max_delay_seconds // 3600))
            self.max_delay_unit.set("hours")
        elif max_delay_seconds >= 60 and max_delay_seconds % 60 == 0:
            self.max_delay_entry.insert(0, str(max_delay_seconds // 60))
            self.max_delay_unit.set("minutes")
        else:
            self.max_delay_entry.insert(0, str(max_delay_seconds))
            self.max_delay_unit.set("seconds")

        self.location_entry.insert(0, self.config.get('default_location', ''))
        self.category_var.set(self.config.get('default_category', 'Home & Garden'))
        self.condition_var.set(self.config.get('default_condition', 'New'))
        self.images_per_entry.insert(0, str(self.config.get('images_per_listing', 4)))
    
    def save_settings(self):
        """Save settings"""
        try:
            min_delay = int(self.min_delay_entry.get())
            max_delay = int(self.max_delay_entry.get())
            images_per = int(self.images_per_entry.get())

            if min_delay < 0 or max_delay < 0 or images_per < 1:
                raise ValueError("Invalid values")

            # Convert delays to seconds based on selected unit
            min_delay_unit = self.min_delay_unit.get()
            max_delay_unit = self.max_delay_unit.get()

            if min_delay_unit == "minutes":
                min_delay_seconds = min_delay * 60
            elif min_delay_unit == "hours":
                min_delay_seconds = min_delay * 3600
            else:  # seconds
                min_delay_seconds = min_delay

            if max_delay_unit == "minutes":
                max_delay_seconds = max_delay * 60
            elif max_delay_unit == "hours":
                max_delay_seconds = max_delay * 3600
            else:  # seconds
                max_delay_seconds = max_delay

            if min_delay_seconds > max_delay_seconds:
                messagebox.showerror("Error", "Minimum delay must be less than maximum delay")
                return

            settings = {
                'chrome_profile_path': self.chrome_path_entry.get().strip(),
                'min_delay_between_posts': min_delay_seconds,
                'max_delay_between_posts': max_delay_seconds,
                'default_location': self.location_entry.get().strip(),
                'default_category': self.category_var.get(),
                'default_condition': self.condition_var.get(),
                'images_per_listing': images_per
            }

            self.config.update(settings)
            messagebox.showinfo("Success", "Settings saved successfully!")
            self.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for delays and images")
