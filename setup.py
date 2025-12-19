#!/usr/bin/env python3
"""
Setup script for Facebook Marketplace Automation Tool
Run this to set up the environment
"""
import subprocess
import sys
import platform
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is adequate"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[ERROR] Python 3.8 or higher is required!")
        print("Please install Python 3.8+ from https://www.python.org/downloads/")
        return False

    print("[OK] Python version is compatible")
    return True

def install_requirements():
    """Install required packages"""
    print_header("Installing Required Packages")
    
    try:
        print("Installing dependencies from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[OK] Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("[ERROR] Error installing dependencies")
        return False

def install_playwright():
    """Install Playwright browsers"""
    print_header("Installing Playwright Browsers")
    
    try:
        print("This may take a few minutes...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("[OK] Playwright browsers installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("[ERROR] Error installing Playwright browsers")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        "data",
        "data/workflows",
        "data/images",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"[OK] Created: {directory}")

    return True

def get_chrome_profile_path():
    """Get the default Chrome profile path for the OS"""
    system = platform.system()
    
    if system == "Windows":
        return str(Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data")
    elif system == "Darwin":  # macOS
        return str(Path.home() / "Library" / "Application Support" / "Google" / "Chrome")
    elif system == "Linux":
        return str(Path.home() / ".config" / "google-chrome")
    
    return ""

def print_next_steps():
    """Print instructions for next steps"""
    print_header("Setup Complete!")
    
    chrome_path = get_chrome_profile_path()
    
    print("Next steps:")
    print("\n1. Run the application:")
    print("   python main.py")
    print("\n2. On first launch, you'll be asked for your Chrome profile path.")
    print(f"   Default location: {chrome_path}")
    print("\n3. Make sure Chrome is closed before running the automation!")
    print("\n4. Create a workflow with your product details")
    print("\n5. Use 'Batch Generate' to create multiple listings")
    print("\n6. Start posting from the Queue tab")
    print("\n[!] IMPORTANT SAFETY TIPS:")
    print("   - Start with 3-5 listings to test")
    print("   - Use delays of 60-180 seconds between posts")
    print("   - Don't post too many listings per day (Facebook may flag it)")
    print("   - Vary your descriptions to look more natural")
    print("\nFor help, check README.md")
    print("\n" + "="*60 + "\n")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  Facebook Marketplace Automation Tool - Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("\n[ERROR] Setup failed during directory creation")
        sys.exit(1)

    # Install requirements
    if not install_requirements():
        print("\n[ERROR] Setup failed during dependency installation")
        sys.exit(1)

    # Install Playwright
    if not install_playwright():
        print("\n[ERROR] Setup failed during Playwright installation")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
