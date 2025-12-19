"""
Facebook Marketplace Automation Tool
Main entry point
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui.main_window import MainWindow

def main():
    """Main entry point"""
    print("Starting Facebook Marketplace Automation Tool...")
    print("=" * 50)
    
    # Create and run the GUI
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()
