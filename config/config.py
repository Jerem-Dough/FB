"""
Configuration management for the application
"""
import json
from pathlib import Path

class Config:
    def __init__(self, config_path="config/settings.json"):
        self.config_path = config_path
        Path(config_path).parent.mkdir(parents=True, exist_ok=True)
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create defaults"""
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            # Default settings
            defaults = {
                'chrome_profile_path': '',
                'min_delay_between_posts': 60,  # seconds
                'max_delay_between_posts': 180,
                'typing_speed': 'medium',  # slow, medium, fast
                'default_location': '',
                'default_category': 'Home & Garden',
                'default_condition': 'New',
                'images_per_listing': 4,
                'auto_save_workflows': True
            }
            self.save_settings(defaults)
            return defaults
    
    def save_settings(self, settings=None):
        """Save settings to file"""
        if settings:
            self.settings = settings
        
        with open(self.config_path, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
    
    def update(self, settings_dict):
        """Update multiple settings at once"""
        self.settings.update(settings_dict)
        self.save_settings()
