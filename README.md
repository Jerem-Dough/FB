# Facebook Marketplace Automation Tool

A simple desktop application to automate Facebook Marketplace listings with workflow templates and batch posting.

## Features
- Create reusable workflow templates
- Multiple description variations per workflow
- Batch image selection and auto-assignment
- Queue system for automated posting
- Human-like behavior (random delays, natural typing)
- Uses your existing Chrome profile (stay logged in)

## Setup Instructions

### 1. Install Python
- Download Python 3.8 or higher from [python.org](https://www.python.org/downloads/)
- **Important:** Check "Add Python to PATH" during installation

### 2. Run Setup Script
The easiest way to set up everything:

```bash
# Navigate to the project folder
cd path/to/fb_marketplace_bot

# Run the automated setup
python setup.py
```

This will:
- Install all dependencies
- Install Playwright browsers
- Create necessary directories

**OR** Manual installation:

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### 3. Create Automation Chrome Profile
**IMPORTANT:** Run this to avoid browser errors:

```bash
python create_automation_profile.py
```

This creates a dedicated Chrome profile for automation, preventing encryption and timeout errors.

### 4. Run the Application
```bash
python main.py
```

## First Time Setup

### Initial Login
1. When you first click "Start Posting", Chrome will open automatically
2. If you're not logged into Facebook, you'll see the Facebook login page
3. **Manually log in** to Facebook in that browser window
4. Your login will be saved in the automation profile
5. You won't need to log in again for future sessions!

**Note:** The automation profile is separate from your regular Chrome profile.

## How to Use

### Create a Workflow
1. Click "New Workflow"
2. Enter product details (title, price, category, location)
3. Add 2-3 description variations
4. Save the workflow

### Batch Generate Listings
1. Select a workflow
2. Click "Batch Generate"
3. Choose a folder with images
4. Set number of listings to create
5. App will auto-assign images and rotate descriptions

### Post to Marketplace
1. Review your queue
2. Click "Start Posting"
3. The app will open Chrome and post listings automatically
4. Monitor progress in real-time

## Troubleshooting

**Chrome timeout or encryption errors:**
- Run `python create_automation_profile.py` to create a dedicated profile
- Make sure Chrome is completely closed before running automation
- Don't use your main Chrome profile - use the automation profile

**Chrome won't open:**
- Make sure Chrome is installed
- Close ALL Chrome windows before running automation
- Check that the automation profile was created successfully

**Listings fail to post:**
- Make sure you're logged into Facebook (log in manually when Chrome opens)
- Ensure images are valid (JPG, PNG)
- Try increasing delays in settings (anti-detection)
- Check your internet connection

**App crashes:**
- Make sure all dependencies are installed (`python setup.py`)
- Check Python version (3.8+)
- Look for error messages in the console
- Try recreating the automation profile

## Safety Tips
- Don't post too many listings at once (5-10 per session)
- Use random delays between posts (recommended: 60-180 seconds)
- Vary your descriptions to look more natural
- Facebook may flag suspicious automation - use responsibly

## Support
For issues or questions, contact the developer.
