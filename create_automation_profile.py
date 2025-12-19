#!/usr/bin/env python3
"""
Helper script to create a dedicated Chrome profile for automation
This avoids encryption errors with the main Chrome profile
"""
import json
import shutil
from pathlib import Path

def create_automation_profile():
    """Create a new Chrome profile for automation"""
    print("\n" + "="*60)
    print("  Creating Automation Chrome Profile")
    print("="*60 + "\n")

    # Create automation profile directory
    automation_profile = Path("chrome_automation_profile")

    if automation_profile.exists():
        print(f"Automation profile already exists at: {automation_profile.absolute()}")
        response = input("Do you want to delete and recreate it? (yes/no): ").strip().lower()
        if response == 'yes':
            shutil.rmtree(automation_profile)
            print("Deleted existing profile")
        else:
            print("Keeping existing profile")
            return str(automation_profile.absolute())

    automation_profile.mkdir(exist_ok=True)
    print(f"[OK] Created automation profile at: {automation_profile.absolute()}")

    # Update config
    config_path = Path("config/settings.json")
    if config_path.exists():
        with open(config_path, 'r') as f:
            settings = json.load(f)
    else:
        settings = {}

    settings['chrome_profile_path'] = str(automation_profile.absolute())

    with open(config_path, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f"[OK] Updated config to use automation profile")

    print("\n" + "="*60)
    print("  Setup Complete!")
    print("="*60)
    print("\nIMPORTANT:")
    print("1. The first time you run the bot, you'll need to log in to Facebook")
    print("2. Chrome will remember your login in this dedicated profile")
    print("3. This profile is separate from your regular Chrome profile")
    print("4. No encryption errors will occur!")
    print("\nYou can now run: python main.py")
    print("\n")

    return str(automation_profile.absolute())

if __name__ == "__main__":
    create_automation_profile()
