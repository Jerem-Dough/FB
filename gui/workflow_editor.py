"""
Workflow editor interface
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from pathlib import Path

class WorkflowEditor(ctk.CTkFrame):
    def __init__(self, parent, db, config):
        super().__init__(parent)
        
        self.db = db
        self.config = config
        self.current_workflow = None
        self.descriptions = []
        
        self.setup_ui()
        self.refresh_workflow_list()
    
    def setup_ui(self):
        """Setup the workflow editor UI"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # Left panel - Workflow list
        self.left_panel = ctk.CTkFrame(self)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.left_panel.grid_rowconfigure(1, weight=1)
        self.left_panel.grid_columnconfigure(0, weight=1)
        
        # Workflow list header
        header = ctk.CTkLabel(
            self.left_panel,
            text="Workflows",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")
        
        # Workflow listbox
        self.workflow_listbox = ctk.CTkScrollableFrame(self.left_panel)
        self.workflow_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.workflow_listbox.grid_columnconfigure(0, weight=1)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.left_panel)
        button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        self.new_btn = ctk.CTkButton(
            button_frame,
            text="New Workflow",
            command=self.new_workflow,
            font=ctk.CTkFont(size=13)
        )
        self.new_btn.grid(row=0, column=0, pady=5, padx=(0, 5), sticky="ew")
        
        self.duplicate_btn = ctk.CTkButton(
            button_frame,
            text="Duplicate",
            command=self.duplicate_workflow,
            font=ctk.CTkFont(size=13)
        )
        self.duplicate_btn.grid(row=0, column=1, pady=5, padx=(5, 0), sticky="ew")
        
        self.delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self.delete_workflow,
            fg_color="darkred",
            font=ctk.CTkFont(size=13)
        )
        self.delete_btn.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")
        
        # Right panel - Workflow editor
        self.right_panel = ctk.CTkScrollableFrame(self)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        self.right_panel.grid_columnconfigure(0, weight=1)
        
        self.create_editor_form()
    
    def create_editor_form(self):
        """Create the workflow editing form"""
        # Title
        title_label = ctk.CTkLabel(
            self.right_panel,
            text="Workflow Editor",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(10, 20), sticky="w")
        
        # Workflow name
        ctk.CTkLabel(self.right_panel, text="Workflow Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ctk.CTkEntry(self.right_panel, width=400)
        self.name_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        # Title
        ctk.CTkLabel(self.right_panel, text="Listing Title:").grid(row=3, column=0, sticky="w", pady=5)
        self.title_entry = ctk.CTkEntry(self.right_panel, width=400)
        self.title_entry.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        
        # Price
        ctk.CTkLabel(self.right_panel, text="Price ($):").grid(row=5, column=0, sticky="w", pady=5)
        self.price_entry = ctk.CTkEntry(self.right_panel, width=200)
        self.price_entry.grid(row=6, column=0, sticky="w", pady=(0, 10))
        
        # Category
        ctk.CTkLabel(self.right_panel, text="Category:").grid(row=7, column=0, sticky="w", pady=5)
        self.category_var = ctk.StringVar(value="Home & Garden")
        self.category_menu = ctk.CTkOptionMenu(
            self.right_panel,
            variable=self.category_var,
            values=["Home & Garden", "Vehicles", "Electronics", "Clothing & Accessories",
                   "Entertainment", "Family", "Hobbies", "Misc", "Other"]
        )
        self.category_menu.grid(row=8, column=0, sticky="w", pady=(0, 10))
        
        # Condition
        ctk.CTkLabel(self.right_panel, text="Condition:").grid(row=9, column=0, sticky="w", pady=5)
        self.condition_var = ctk.StringVar(value="New")
        self.condition_menu = ctk.CTkOptionMenu(
            self.right_panel,
            variable=self.condition_var,
            values=["New", "Used - Like new", "Used - good", "Used - fair"]
        )
        self.condition_menu.grid(row=10, column=0, sticky="w", pady=(0, 10))
        
        # Location
        ctk.CTkLabel(self.right_panel, text="Location (optional):").grid(row=11, column=0, sticky="w", pady=5)
        self.location_entry = ctk.CTkEntry(self.right_panel, width=400)
        self.location_entry.grid(row=12, column=0, sticky="ew", pady=(0, 10))

        # Delivery Method
        ctk.CTkLabel(self.right_panel, text="Delivery Method:").grid(row=13, column=0, sticky="w", pady=5)
        self.delivery_method_var = ctk.StringVar(value="Door pickup")
        self.delivery_method_menu = ctk.CTkOptionMenu(
            self.right_panel,
            variable=self.delivery_method_var,
            values=["Public meetup", "Door pickup", "Door dropoff"]
        )
        self.delivery_method_menu.grid(row=14, column=0, sticky="w", pady=(0, 10))

        # Groups
        ctk.CTkLabel(self.right_panel, text="Groups (comma-separated, optional):").grid(row=15, column=0, sticky="w", pady=5)
        self.groups_entry = ctk.CTkEntry(self.right_panel, width=400, placeholder_text="Group 1, Group 2, Group 3")
        self.groups_entry.grid(row=16, column=0, sticky="ew", pady=(0, 10))

        # Boost Listing
        self.boost_var = ctk.BooleanVar(value=False)
        boost_checkbox = ctk.CTkCheckBox(
            self.right_panel,
            text="Enable Boost Listing (promoted/paid listing)",
            variable=self.boost_var,
            font=ctk.CTkFont(size=13)
        )
        boost_checkbox.grid(row=17, column=0, sticky="w", pady=(5, 10))

        # Descriptions section
        desc_header = ctk.CTkLabel(
            self.right_panel,
            text="Description Variations (2-3 recommended)",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        desc_header.grid(row=18, column=0, sticky="w", pady=(20, 10))

        # Description list
        self.desc_frame = ctk.CTkFrame(self.right_panel)
        self.desc_frame.grid(row=19, column=0, sticky="ew", pady=(0, 10))
        self.desc_frame.grid_columnconfigure(0, weight=1)

        # Add description button
        self.add_desc_btn = ctk.CTkButton(
            self.right_panel,
            text="+ Add Description",
            command=self.add_description_field,
            width=150
        )
        self.add_desc_btn.grid(row=20, column=0, sticky="w", pady=5)

        # Save button
        self.save_btn = ctk.CTkButton(
            self.right_panel,
            text="Save Workflow",
            command=self.save_workflow,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.save_btn.grid(row=21, column=0, sticky="ew", pady=(20, 10))

        # Batch generate section
        batch_header = ctk.CTkLabel(
            self.right_panel,
            text="Batch Generate Listings",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        batch_header.grid(row=22, column=0, sticky="w", pady=(30, 10))

        batch_frame = ctk.CTkFrame(self.right_panel)
        batch_frame.grid(row=23, column=0, sticky="ew", pady=5)
        batch_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(batch_frame, text="Images per listing:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.images_per_listing = ctk.CTkEntry(batch_frame, width=60)
        self.images_per_listing.insert(0, "4")
        self.images_per_listing.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(batch_frame, text="Number of listings:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.num_listings = ctk.CTkEntry(batch_frame, width=60)
        self.num_listings.insert(0, "5")
        self.num_listings.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.batch_btn = ctk.CTkButton(
            self.right_panel,
            text="Select Images & Generate",
            command=self.batch_generate,
            font=ctk.CTkFont(size=14),
            height=40
        )
        self.batch_btn.grid(row=24, column=0, sticky="ew", pady=10)
    
    def add_description_field(self):
        """Add a new description text box"""
        row = len(self.descriptions)
        
        frame = ctk.CTkFrame(self.desc_frame)
        frame.grid(row=row, column=0, sticky="ew", pady=5)
        frame.grid_columnconfigure(0, weight=1)
        
        textbox = ctk.CTkTextbox(frame, height=100)
        textbox.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        remove_btn = ctk.CTkButton(
            frame,
            text="Remove",
            command=lambda: self.remove_description(frame, textbox),
            width=80,
            fg_color="darkred"
        )
        remove_btn.grid(row=0, column=1, padx=5)
        
        self.descriptions.append(textbox)
    
    def remove_description(self, frame, textbox):
        """Remove a description field"""
        self.descriptions.remove(textbox)
        frame.destroy()
    
    def new_workflow(self):
        """Create a new workflow"""
        self.current_workflow = None
        self.clear_form()
        # Add one description field by default
        if not self.descriptions:
            self.add_description_field()
    
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, 'end')
        self.title_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.category_var.set("Home & Garden")
        self.condition_var.set("New")
        self.location_entry.delete(0, 'end')
        self.delivery_method_var.set("Door pickup")
        self.groups_entry.delete(0, 'end')
        self.boost_var.set(False)

        # Clear descriptions
        for desc in self.descriptions:
            desc.master.destroy()
        self.descriptions.clear()
    
    def save_workflow(self):
        """Save the current workflow"""
        name = self.name_entry.get().strip()
        title = self.title_entry.get().strip()
        price = self.price_entry.get().strip()
        
        if not name or not title or not price:
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        try:
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number")
            return
        
        # Get descriptions
        desc_list = []
        for textbox in self.descriptions:
            text = textbox.get("1.0", "end-1c").strip()
            if text:
                desc_list.append(text)
        
        if not desc_list:
            messagebox.showerror("Error", "Please add at least one description")
            return
        
        category = self.category_var.get()
        condition = self.condition_var.get()
        location = self.location_entry.get().strip()
        delivery_method = self.delivery_method_var.get()
        boost_listing = self.boost_var.get()

        # Parse groups (comma-separated)
        groups_str = self.groups_entry.get().strip()
        groups = [g.strip() for g in groups_str.split(',')] if groups_str else None

        if self.current_workflow:
            # Update existing
            self.db.update_workflow(
                self.current_workflow['id'],
                name, title, desc_list, price, category, condition, location, delivery_method, groups, boost_listing
            )
            messagebox.showinfo("Success", "Workflow updated successfully!")
        else:
            # Create new
            workflow_id = self.db.create_workflow(
                name, title, desc_list, price, category, condition, location, delivery_method, groups, boost_listing
            )
            if workflow_id:
                messagebox.showinfo("Success", "Workflow created successfully!")
            else:
                messagebox.showerror("Error", "Workflow name already exists")
                return

        self.refresh_workflow_list()
    
    def duplicate_workflow(self):
        """Duplicate the selected workflow"""
        if not self.current_workflow:
            messagebox.showwarning("Warning", "Please select a workflow to duplicate")
            return
        
        # Create dialog for duplication options
        dialog = ctk.CTkToplevel(self)
        dialog.title("Duplicate Workflow")
        dialog.geometry("400x300")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Duplicate Options", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(dialog, text="New workflow name:").pack(pady=5)
        name_entry = ctk.CTkEntry(dialog, width=300)
        name_entry.insert(0, f"{self.current_workflow['name']} (Copy)")
        name_entry.pack(pady=5)
        
        change_desc = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(dialog, text="Use different descriptions", variable=change_desc).pack(pady=10)
        
        def confirm():
            new_name = name_entry.get().strip()
            if not new_name:
                messagebox.showerror("Error", "Please enter a name")
                return
            
            descriptions = self.current_workflow['descriptions']
            
            if change_desc.get():
                # Just duplicate and let user edit descriptions
                self.db.create_workflow(
                    new_name,
                    self.current_workflow['title'],
                    descriptions,
                    self.current_workflow['price'],
                    self.current_workflow['category'],
                    self.current_workflow['condition'],
                    self.current_workflow['location'],
                    self.current_workflow.get('delivery_method', 'Door pickup'),
                    self.current_workflow.get('groups'),
                    self.current_workflow.get('boost_listing', False)
                )
                dialog.destroy()
                self.refresh_workflow_list()
                messagebox.showinfo("Success", "Workflow duplicated! You can now edit the descriptions.")
            else:
                # Exact duplicate
                workflow_id = self.db.create_workflow(
                    new_name,
                    self.current_workflow['title'],
                    descriptions,
                    self.current_workflow['price'],
                    self.current_workflow['category'],
                    self.current_workflow['condition'],
                    self.current_workflow['location'],
                    self.current_workflow.get('delivery_method', 'Door pickup'),
                    self.current_workflow.get('groups'),
                    self.current_workflow.get('boost_listing', False)
                )
                if workflow_id:
                    dialog.destroy()
                    self.refresh_workflow_list()
                    messagebox.showinfo("Success", "Workflow duplicated successfully!")
                else:
                    messagebox.showerror("Error", "Workflow name already exists")
        
        ctk.CTkButton(dialog, text="Confirm", command=confirm).pack(pady=20)
    
    def delete_workflow(self):
        """Delete the selected workflow"""
        if not self.current_workflow:
            messagebox.showwarning("Warning", "Please select a workflow to delete")
            return
        
        if messagebox.askyesno("Confirm", f"Delete workflow '{self.current_workflow['name']}'?"):
            self.db.delete_workflow(self.current_workflow['id'])
            self.current_workflow = None
            self.clear_form()
            self.refresh_workflow_list()
            messagebox.showinfo("Success", "Workflow deleted")
    
    def load_workflow(self, workflow):
        """Load workflow into the editor"""
        self.current_workflow = workflow

        self.name_entry.delete(0, 'end')
        self.name_entry.insert(0, workflow['name'])

        self.title_entry.delete(0, 'end')
        self.title_entry.insert(0, workflow['title'])

        self.price_entry.delete(0, 'end')
        self.price_entry.insert(0, str(workflow['price']))

        self.category_var.set(workflow['category'])
        self.condition_var.set(workflow['condition'])

        self.location_entry.delete(0, 'end')
        self.location_entry.insert(0, workflow['location'])

        self.delivery_method_var.set(workflow.get('delivery_method', 'Door pickup'))

        self.groups_entry.delete(0, 'end')
        if workflow.get('groups'):
            self.groups_entry.insert(0, ', '.join(workflow['groups']))

        self.boost_var.set(workflow.get('boost_listing', False))

        # Load descriptions
        for desc in self.descriptions:
            desc.master.destroy()
        self.descriptions.clear()

        for desc_text in workflow['descriptions']:
            self.add_description_field()
            self.descriptions[-1].insert("1.0", desc_text)
    
    def refresh_workflow_list(self):
        """Refresh the workflow list"""
        # Clear current list
        for widget in self.workflow_listbox.winfo_children():
            widget.destroy()
        
        workflows = self.db.get_all_workflows()
        
        for workflow in workflows:
            btn = ctk.CTkButton(
                self.workflow_listbox,
                text=workflow['name'],
                command=lambda w=workflow: self.load_workflow(w),
                anchor="w",
                font=ctk.CTkFont(size=13)
            )
            btn.grid(sticky="ew", pady=2)
    
    def batch_generate(self):
        """Generate multiple listings from images"""
        if not self.current_workflow:
            messagebox.showwarning("Warning", "Please select or create a workflow first")
            return
        
        # Select image folder
        folder = filedialog.askdirectory(title="Select folder with images")
        if not folder:
            return
        
        # Get all image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        image_files = []
        for file in Path(folder).iterdir():
            if file.suffix.lower() in image_extensions:
                image_files.append(str(file))
        
        if not image_files:
            messagebox.showerror("Error", "No images found in selected folder")
            return
        
        try:
            images_per = int(self.images_per_listing.get())
            num_listings = int(self.num_listings.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number format")
            return
        
        if images_per * num_listings > len(image_files):
            messagebox.showwarning(
                "Warning",
                f"Not enough images. You have {len(image_files)} images but need {images_per * num_listings}.\n"
                f"Will create as many listings as possible."
            )
            num_listings = len(image_files) // images_per
        
        # Generate listings
        descriptions = self.current_workflow['descriptions']
        generated = 0
        
        for i in range(num_listings):
            # Get images for this listing
            start_idx = i * images_per
            end_idx = start_idx + images_per
            listing_images = image_files[start_idx:end_idx]
            
            # Rotate through descriptions
            desc_idx = i % len(descriptions)
            description = descriptions[desc_idx]
            
            # Add to queue
            self.db.add_to_queue(
                self.current_workflow['id'],
                self.current_workflow['title'],
                description,
                self.current_workflow['price'],
                self.current_workflow['category'],
                self.current_workflow['condition'],
                self.current_workflow['location'],
                listing_images,
                self.current_workflow.get('delivery_method', 'Door pickup'),
                self.current_workflow.get('groups'),
                self.current_workflow.get('boost_listing', False)
            )
            generated += 1
        
        messagebox.showinfo("Success", f"Generated {generated} listings and added to queue!")
