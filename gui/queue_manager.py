"""
Queue manager interface
"""
import customtkinter as ctk
from tkinter import messagebox
import asyncio
import threading
from automation.browser import BrowserManager
from automation.marketplace import MarketplaceAutomation
import random

class QueueManager(ctk.CTkFrame):
    def __init__(self, parent, db, config, status_callback):
        super().__init__(parent)
        
        self.db = db
        self.config = config
        self.status_callback = status_callback
        self.is_posting = False
        
        self.setup_ui()
        self.refresh_queue()
    
    def setup_ui(self):
        """Setup the queue manager UI"""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Posting Queue",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Stats
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text="0 pending | 0 posted | 0 failed",
            font=ctk.CTkFont(size=12)
        )
        self.stats_label.grid(row=0, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(header_frame)
        button_frame.grid(row=0, column=2, padx=10, pady=10)
        
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="Start Posting",
            command=self.start_posting,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            width=130
        )
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = ctk.CTkButton(
            button_frame,
            text="Stop",
            command=self.stop_posting,
            font=ctk.CTkFont(size=14),
            fg_color="red",
            width=80,
            state="disabled"
        )
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear Completed",
            command=self.clear_completed,
            font=ctk.CTkFont(size=12),
            width=130
        )
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        # Queue list
        self.queue_frame = ctk.CTkScrollableFrame(self)
        self.queue_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.queue_frame.grid_columnconfigure(0, weight=1)
        
        # Progress section
        progress_frame = ctk.CTkFrame(self)
        progress_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to post",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.progress_bar.set(0)
    
    def refresh_queue(self):
        """Refresh the queue display"""
        # Clear current queue display
        for widget in self.queue_frame.winfo_children():
            widget.destroy()
        
        # Get queue items
        items = self.db.get_queue_items()
        
        if not items:
            empty_label = ctk.CTkLabel(
                self.queue_frame,
                text="Queue is empty\nUse 'Batch Generate' in Workflows to add listings",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            empty_label.grid(row=0, column=0, pady=50)
        
        # Count by status
        pending = sum(1 for item in items if item['status'] == 'pending')
        posted = sum(1 for item in items if item['status'] == 'posted')
        failed = sum(1 for item in items if item['status'] == 'failed')
        
        self.stats_label.configure(text=f"{pending} pending | {posted} posted | {failed} failed")
        
        # Display items
        for idx, item in enumerate(items):
            self.create_queue_item_widget(item, idx)
    
    def create_queue_item_widget(self, item, row):
        """Create a widget for a queue item"""
        # Main frame
        item_frame = ctk.CTkFrame(self.queue_frame)
        item_frame.grid(row=row, column=0, sticky="ew", pady=5, padx=5)
        item_frame.grid_columnconfigure(1, weight=1)
        
        # Status indicator
        status_colors = {
            'pending': 'gray',
            'posting': 'blue',
            'posted': 'green',
            'failed': 'red'
        }
        
        status_frame = ctk.CTkFrame(item_frame, width=10, fg_color=status_colors.get(item['status'], 'gray'))
        status_frame.grid(row=0, column=0, rowspan=3, sticky="ns", padx=(5, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            item_frame,
            text=item['title'],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=1, sticky="w", padx=5, pady=(5, 0))
        
        # Details
        delivery = item.get('delivery_method', 'Door pickup')
        groups_count = len(item.get('groups', [])) if item.get('groups') else 0
        groups_str = f" | {groups_count} group(s)" if groups_count > 0 else ""
        details = f"${item['price']} | {item['category']} | {len(item['images'])} images | {delivery}{groups_str}"
        details_label = ctk.CTkLabel(
            item_frame,
            text=details,
            font=ctk.CTkFont(size=11),
            anchor="w",
            text_color="gray"
        )
        details_label.grid(row=1, column=1, sticky="w", padx=5)
        
        # Status text
        status_text = (item.get('status') or 'pending').capitalize()
        if item.get('error_message'):
            status_text += f" - {item['error_message']}"
        
        status_label = ctk.CTkLabel(
            item_frame,
            text=status_text,
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        status_label.grid(row=2, column=1, sticky="w", padx=5, pady=(0, 5))
        
        # Delete button
        if item['status'] in ['pending', 'failed']:
            delete_btn = ctk.CTkButton(
                item_frame,
                text="Delete",
                command=lambda: self.delete_item(item['id']),
                width=80,
                height=30,
                fg_color="darkred"
            )
            delete_btn.grid(row=0, column=2, rowspan=3, padx=10)
    
    def delete_item(self, item_id):
        """Delete a queue item"""
        if messagebox.askyesno("Confirm", "Delete this listing from queue?"):
            self.db.delete_queue_item(item_id)
            self.refresh_queue()
    
    def clear_completed(self):
        """Clear all completed/failed items"""
        if messagebox.askyesno("Confirm", "Clear all posted and failed listings from queue?"):
            self.db.clear_completed_queue()
            self.refresh_queue()
    
    def start_posting(self):
        """Start posting listings from queue"""
        pending_items = self.db.get_queue_items(status='pending')
        
        if not pending_items:
            messagebox.showinfo("Info", "No pending listings in queue")
            return
        
        # Check Chrome profile
        chrome_path = self.config.get('chrome_profile_path')
        if not chrome_path:
            messagebox.showerror(
                "Error",
                "Chrome profile path not configured.\nPlease set it in Settings."
            )
            return
        
        self.is_posting = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        # Start posting in separate thread
        thread = threading.Thread(target=self.posting_worker, args=(pending_items,))
        thread.daemon = True
        thread.start()
    
    def stop_posting(self):
        """Stop posting process"""
        self.is_posting = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_callback("Stopped")
    
    def posting_worker(self, items):
        """Worker thread for posting listings"""
        # Create new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(self.post_listings(items))
        except Exception as e:
            print(f"Error in posting worker: {e}")
        finally:
            loop.close()
            
            # Reset UI
            self.after(0, lambda: self.start_btn.configure(state="normal"))
            self.after(0, lambda: self.stop_btn.configure(state="disabled"))
            self.after(0, lambda: self.status_callback("Ready"))
            self.after(0, self.refresh_queue)
    
    async def post_listings(self, items):
        """Async function to post listings"""
        chrome_path = self.config.get('chrome_profile_path')
        browser = BrowserManager(chrome_path)
        automation = MarketplaceAutomation(browser)
        
        try:
            await automation.initialize()
            
            total = len(items)
            for idx, item in enumerate(items):
                if not self.is_posting:
                    break
                
                # Update progress
                progress = (idx + 1) / total
                self.after(0, lambda p=progress: self.progress_bar.set(p))
                self.after(0, lambda i=idx: self.progress_label.configure(
                    text=f"Posting {i+1} of {total}..."
                ))
                self.after(0, lambda: self.status_callback(f"Posting {idx+1}/{total}"))
                
                # Update item status
                self.db.update_queue_status(item['id'], 'posting')
                self.after(0, self.refresh_queue)
                
                # Post listing
                result = await automation.create_listing(
                    item['title'],
                    item['description'],
                    item['price'],
                    item['category'],
                    item['condition'],
                    item['location'],
                    item['images'],
                    item.get('delivery_method', 'Door pickup'),
                    item.get('groups')
                )
                
                # Update status based on result
                if result['success']:
                    self.db.update_queue_status(item['id'], 'posted')
                else:
                    self.db.update_queue_status(item['id'], 'failed', result['error'])
                
                self.after(0, self.refresh_queue)
                
                # Random delay between posts
                if idx < total - 1:  # Don't delay after last post
                    min_delay = self.config.get('min_delay_between_posts', 60)
                    max_delay = self.config.get('max_delay_between_posts', 180)
                    delay = random.uniform(min_delay, max_delay)
                    
                    self.after(0, lambda d=delay: self.progress_label.configure(
                        text=f"Waiting {int(d)} seconds before next post..."
                    ))
                    
                    await asyncio.sleep(delay)
            
            self.after(0, lambda: self.progress_label.configure(text="Posting complete!"))
            self.after(0, lambda: self.status_callback("Complete"))
            
        except Exception as e:
            print(f"Error posting listings: {e}")
            error_msg = str(e)
            self.after(0, lambda: messagebox.showerror("Error", f"Posting failed: {error_msg}"))
        finally:
            await automation.close()
            self.is_posting = False
