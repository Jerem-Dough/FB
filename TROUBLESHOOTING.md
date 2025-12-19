# Troubleshooting Guide

## Installation Issues

### "Python is not recognized as a command"
**Problem**: Python not in system PATH

**Solutions**:
1. Reinstall Python and CHECK "Add Python to PATH"
2. Or manually add Python to PATH:
   - Windows: System Properties → Environment Variables → Path → Add Python folder
   - Mac/Linux: Add to `.bashrc` or `.zshrc`: `export PATH="/usr/local/bin/python3:$PATH"`

### "pip install fails with permission error"
**Problem**: Need admin rights or using wrong Python

**Solutions**:
- Windows: Run Command Prompt as Administrator
- Mac/Linux: Use `pip install --user -r requirements.txt`
- Or create virtual environment first:
  ```bash
  python -m venv venv
  # Windows:
  venv\Scripts\activate
  # Mac/Linux:
  source venv/bin/activate
  pip install -r requirements.txt
  ```

### "playwright install fails"
**Problem**: Network issues or disk space

**Solutions**:
1. Check internet connection
2. Free up disk space (needs ~300MB)
3. Try manual install:
   ```bash
   python -m playwright install chromium --with-deps
   ```

---

## Chrome Profile Issues

### "Can't find Chrome profile path"
**Default Locations**:
- **Windows**: `C:\Users\[YourUsername]\AppData\Local\Google\Chrome\User Data`
- **Mac**: `/Users/[YourUsername]/Library/Application Support/Google/Chrome`
- **Linux**: `/home/[YourUsername]/.config/google-chrome`

**Finding it manually**:
1. Open Chrome
2. Type in address bar: `chrome://version`
3. Look for "Profile Path"
4. Copy the path UP TO "User Data" (not including "Default")

### "Chrome won't open when automation starts"
**Causes & Solutions**:
1. **Chrome is already running**
   - Solution: Close ALL Chrome windows completely
   - Check Task Manager/Activity Monitor for chrome processes

2. **Wrong profile path**
   - Solution: Go to Settings and verify the path
   - Should end with "User Data" folder

3. **Chrome not installed**
   - Solution: Install Google Chrome first
   - Make sure it's Google Chrome, not Chromium or Edge

### "Automation opens Chrome but not logged in"
**Problem**: Not using the right profile

**Solutions**:
1. Log into Facebook in your normal Chrome first
2. Close Chrome completely
3. Make sure profile path is correct (should include your bookmarks/extensions)
4. Try opening Chrome with the automation - should have all your stuff

---

## Posting Issues

### "Not logged into Facebook"
**Solutions**:
1. Open Chrome normally
2. Go to Facebook.com and log in
3. Stay logged in (check "Remember me")
4. Close Chrome completely
5. Run automation again

### "Images won't upload"
**Causes**:
- Wrong file format
- Files corrupted
- Files too large
- Path has special characters

**Solutions**:
1. Use JPG or PNG only
2. Keep files under 5MB each
3. Remove special characters from filenames
4. Try copying files to a simple path like `C:\images\`

### "Can't find upload button / form fields"
**Cause**: Facebook changed their layout

**Solution**: Selectors need updating
1. Open an issue or contact developer
2. Or update `automation/marketplace.py` yourself:
   - Look for selector strings like `'input[type="file"]'`
   - Inspect Facebook's HTML and update selectors

### "Posting stops in the middle"
**Causes**:
- Network timeout
- Facebook detected automation
- Chrome crashed

**Solutions**:
1. Check your internet connection
2. Increase delays in Settings (try 120-240 seconds)
3. Clear the completed items and retry failed ones
4. Post in smaller batches (3-5 at a time)

### "Listing posted but shows as 'failed'"
**Cause**: Post succeeded but confirmation not detected

**Solutions**:
1. Check Facebook Marketplace - it might actually be there
2. Delete the failed item from queue
3. If happens often, selector for confirmation may need updating

---

## GUI Issues

### "GUI is blank or frozen"
**Causes**:
- Python version too old
- CustomTkinter not installed
- Database locked

**Solutions**:
1. Check Python version: `python --version` (need 3.8+)
2. Reinstall CustomTkinter: `pip install --upgrade customtkinter`
3. Delete `data/app.db` (will lose workflows - backup first)
4. Restart computer

### "Can't see some buttons or text"
**Cause**: Display scaling or theme issues

**Solutions**:
1. Try different appearance mode in Settings
2. Adjust OS display scaling to 100%
3. Update CustomTkinter: `pip install --upgrade customtkinter`

### "Window too small/large"
**Solution**: Edit `gui/main_window.py`
- Change line: `self.geometry("1200x700")`
- Try different sizes like `"1400x800"` or `"1000x600"`

---

## Database Issues

### "Database is locked"
**Cause**: Another instance running or corrupted

**Solutions**:
1. Close all instances of the app
2. Restart computer
3. Last resort: Delete `data/app.db` (will lose all workflows)

### "Workflow disappeared"
**Cause**: Database corruption

**Solutions**:
1. Check `data/app.db` exists
2. Try SQLite browser to view database
3. Restore from backup if you made one

### "Can't save workflow - name already exists"
**Solution**: Each workflow needs unique name
- Choose a different name
- Or delete the old workflow first

---

## Performance Issues

### "Posting is very slow"
**This is normal!** Safety first.

**Expected times**:
- 30-60 seconds per listing to post
- 60-180 seconds delay between posts
- Total: ~2-4 minutes per listing

**If unusually slow**:
1. Check internet speed
2. Try during off-peak hours
3. Close other programs using internet

### "High CPU usage"
**Cause**: Chrome + automation + GUI

**Solutions**:
1. Close other programs
2. Use a simpler Chrome profile (new profile with no extensions)
3. Reduce number of simultaneous operations

---

## Facebook-Specific Issues

### "Account restricted or flagged"
**Cause**: Too much automation detected

**Prevention**:
- Post max 10-15 listings per day
- Use 90-180 second delays
- Vary descriptions
- Mix with manual posts

**If it happens**:
1. Stop using automation immediately
2. Post manually for a few days
3. Check Facebook notifications/messages
4. Wait for restriction to lift (usually 24-48 hours)

### "Listings keep getting removed"
**Causes**:
- Violating Facebook policies
- Reported by users
- Duplicate content

**Solutions**:
1. Review Facebook Commerce Policies
2. Vary your listings more
3. Use different descriptions
4. Don't post identical items

### "Can't select certain categories"
**Cause**: Category selector changed

**Solution**:
1. Try selecting in GUI first
2. May need to update category list in code
3. Or manually select after automation starts

---

## Error Messages

### "playwright._impl._api_types.Error: Target closed"
**Cause**: Chrome crashed or was closed

**Solutions**:
1. Don't close Chrome while posting
2. Check Chrome isn't crashing
3. Update Chrome to latest version

### "sqlite3.OperationalError: no such table"
**Cause**: Database not initialized

**Solution**: Delete `data/app.db` and restart app (will recreate)

### "ModuleNotFoundError: No module named 'customtkinter'"
**Cause**: Dependencies not installed

**Solution**:
```bash
pip install -r requirements.txt
```

### "FileNotFoundError: [Errno 2] No such file or directory"
**Cause**: Missing directories or files

**Solution**: Run `python setup.py` again to recreate structure

---

## Getting Help

### Before Asking for Help
1. ✅ Check this troubleshooting guide
2. ✅ Read the README.md and QUICKSTART.md
3. ✅ Try running `python setup.py` again
4. ✅ Check Python version: `python --version`
5. ✅ Check all dependencies installed: `pip list`

### When Reporting Issues
Include:
- Python version
- Operating system
- Full error message
- What you were trying to do
- Screenshots if GUI issue

### Common "Not a Bug" Reports
- ❌ "It's slow" - This is intentional for safety
- ❌ "Facebook blocked me" - Use more carefully
- ❌ "Chrome opens logged out" - Wrong profile path
- ❌ "Only posts 1 per minute" - Safety delays are working correctly

---

## Debug Mode

### Enable Verbose Logging
Add to top of `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Take Screenshots During Posting
Uncomment in `automation/marketplace.py`:
```python
await self.browser.take_screenshot(f"debug_{step}.png")
```

### Check Database Contents
Use SQLite browser or:
```bash
sqlite3 data/app.db
.tables
SELECT * FROM workflows;
SELECT * FROM queue;
.exit
```

---

## Still Having Issues?

1. Try the nuclear option:
   ```bash
   # Backup workflows if any
   # Then fresh start:
   rm -rf venv data config
   python setup.py
   python main.py
   ```

2. Check if Facebook changed something:
   - Try posting manually first
   - Check if Marketplace layout changed
   - Other automation tools having same issues?

3. Consider if it's a Facebook issue:
   - Is Marketplace down?
   - Try different network/VPN
   - Try different Facebook account

Remember: This tool automates a browser, so anything that works manually should work automated. If manual posting works but automation doesn't, it's usually a selector or timing issue.
