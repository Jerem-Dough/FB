# Facebook Marketplace Automation Tool - Project Overview

## What This Tool Does

This is a desktop application that automates posting listings to Facebook Marketplace. Instead of manually creating each listing, you can:

1. **Create workflow templates** with your product details
2. **Batch generate listings** from folders of images
3. **Queue and automate posting** with human-like behavior

Perfect for sellers who post similar items repeatedly (like your friend's CNC signs).

## Key Features

### ✅ Workflow Templates
- Save reusable listing templates
- Multiple description variations per workflow
- Duplicate workflows with one click
- Easy editing and management

### ✅ Batch Generation
- Select a folder of images
- Automatically create multiple listings
- Descriptions rotate across listings
- Images distributed evenly

### ✅ Smart Automation
- Uses your existing Chrome profile (stays logged in)
- Human-like typing and delays
- Random delays between posts (60-180 seconds)
- Real-time progress tracking

### ✅ User-Friendly GUI
- Simple, modern interface
- No coding required
- Visual workflow management
- Queue monitoring

## Architecture

### Technology Stack
- **Python 3.8+**: Core language
- **Playwright**: Browser automation (better than Selenium)
- **CustomTkinter**: Modern GUI framework
- **SQLite**: Local database for workflows/queue
- **Persistent Chrome Profile**: Uses user's existing Facebook session

### Project Structure
```
fb_marketplace_bot/
├── main.py                    # Entry point
├── setup.py                   # Installation script
├── requirements.txt           # Dependencies
├── automation/
│   ├── browser.py            # Playwright browser management
│   ├── marketplace.py        # FB Marketplace posting logic
│   └── human_behavior.py     # Anti-detection features
├── gui/
│   ├── main_window.py        # Main application window
│   ├── workflow_editor.py    # Workflow creation/editing
│   ├── queue_manager.py      # Queue display and posting
│   └── settings_window.py    # Settings configuration
├── database/
│   └── db.py                 # SQLite operations
├── config/
│   └── config.py             # Configuration management
└── data/                      # Runtime data (created on first run)
    ├── app.db                # SQLite database
    ├── workflows/            # Workflow backups
    └── images/               # Cached images
```

## How It Works

### 1. Workflow Creation
```
User creates workflow with:
├── Basic info (title, price, category, condition)
├── 2-3 description variations
└── Optional location

Saved to SQLite database
```

### 2. Batch Generation
```
User selects:
├── Image folder
├── Images per listing (e.g., 4)
└── Number of listings (e.g., 5)

Tool generates:
├── Listing 1: Images 1-4, Description A
├── Listing 2: Images 5-8, Description B
├── Listing 3: Images 9-12, Description C
├── Listing 4: Images 13-16, Description A (rotates)
└── Listing 5: Images 17-20, Description B

All added to queue
```

### 3. Automated Posting
```
For each queued listing:
1. Open Chrome with user's profile
2. Navigate to Marketplace create page
3. Upload images (file picker)
4. Fill title, price, category, condition
5. Paste description
6. Set location (if specified)
7. Click publish
8. Wait 60-180 seconds (random)
9. Repeat for next listing
```

### 4. Anti-Detection Features
- **Random delays**: Vary typing speed and action delays
- **Human-like behavior**: Natural mouse movements, typing patterns
- **Persistent profile**: Uses real Chrome with real login
- **Configurable pacing**: User controls delays between posts
- **Error handling**: Graceful failures, retry capability

## Security & Privacy

### What's Stored Locally
- Workflow templates (titles, descriptions, prices)
- Queue items (pending/posted listings)
- Settings (Chrome path, delay preferences)
- **NO passwords or credentials stored**

### Data Flow
```
User's Computer Only:
├── SQLite database (local)
├── Chrome profile (user's existing)
└── Configuration files (local)

No data sent anywhere except:
└── Facebook Marketplace (only when posting)
```

### Facebook ToS Considerations
⚠️ **Important**: Browser automation technically violates Facebook's Terms of Service. Users should:
- Use at their own risk
- Start with small batches (3-5 listings)
- Use realistic delays (60-180 seconds)
- Avoid posting 50+ listings per day
- Vary descriptions to look natural

## Limitations

### Technical Limitations
- **Facebook selectors change**: May need updates when FB changes their UI
- **Network dependent**: Requires stable internet connection
- **Chrome required**: Must have Chrome installed
- **Single account**: One Chrome profile at a time
- **No API**: Pure browser automation (slower but works)

### Safety Limitations
- **Detection risk**: Heavy usage may trigger Facebook flags
- **Account risk**: Possible account restrictions if abused
- **No guarantees**: Facebook can change detection at any time

## Future Enhancements

### Potential Improvements
1. **Multi-account support**: Switch between Chrome profiles
2. **Scheduling**: Post at specific times
3. **Templates library**: Pre-made description templates
4. **Image editing**: Resize, crop, watermark before posting
5. **Analytics**: Track which descriptions/prices perform best
6. **Export/Import**: Share workflows with others
7. **Cloud sync**: Backup workflows to cloud

### Advanced Features
- **AI descriptions**: Generate variations with GPT
- **Price optimization**: Suggest optimal pricing
- **Competitor monitoring**: Track similar listings
- **Auto-renew**: Repost expired listings

## Development Notes

### Code Quality
- Type hints where beneficial
- Comprehensive error handling
- Async/await for browser operations
- Threaded posting to keep GUI responsive
- Modular design for easy maintenance

### Testing Checklist
- [ ] Workflow CRUD operations
- [ ] Batch generation with various image counts
- [ ] Posting with different configurations
- [ ] Chrome profile detection
- [ ] Error recovery
- [ ] GUI responsiveness during posting
- [ ] Database integrity

### Deployment
1. Test on Windows, Mac, Linux
2. Verify Chrome profile paths
3. Test with actual Facebook account
4. Monitor for selector changes
5. Update documentation

## Support & Maintenance

### Common Issues
1. **Selectors outdated**: Facebook changed UI → Update marketplace.py
2. **Chrome won't open**: Profile path wrong → Check settings
3. **Can't log in**: Session expired → Log in manually first
4. **Images fail**: Wrong format → Check file types

### Updating Selectors
When Facebook changes their UI, update these in `marketplace.py`:
- Image upload input selector
- Title/price/description field selectors
- Category/condition dropdown selectors
- Publish button selector

### Version History
- **v1.0.0**: Initial release
  - Workflow management
  - Batch generation
  - Queue system
  - Persistent Chrome profile
  - Human-like behavior

## License & Credits

This tool was created for legitimate sellers who want to streamline their Marketplace posting workflow. Use responsibly and in accordance with Facebook's community standards.

**Built with:**
- Python & Playwright
- CustomTkinter
- SQLite
- A lot of trial and error 😄
