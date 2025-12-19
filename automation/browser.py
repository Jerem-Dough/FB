"""
Browser automation setup with persistent Chrome profile
"""
from playwright.async_api import async_playwright
import asyncio
from pathlib import Path

class BrowserManager:
    def __init__(self, chrome_profile_path=None):
        self.chrome_profile_path = chrome_profile_path
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
    
    async def start(self):
        """Start browser with persistent profile"""
        self.playwright = await async_playwright().start()

        # Launch args for better stealth
        launch_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
        ]

        if self.chrome_profile_path:
            try:
                # Use persistent context (user's Chrome profile)
                self.context = await self.playwright.chromium.launch_persistent_context(
                    user_data_dir=self.chrome_profile_path,
                    headless=False,  # Must be False for persistent context
                    args=launch_args,
                    viewport={'width': 1920, 'height': 1080},
                    locale='en-US',
                    timezone_id='America/New_York',
                    timeout=60000,  # 60 second timeout
                    slow_mo=100,  # Slow down operations by 100ms
                )
                self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
            except Exception as e:
                error_msg = str(e)
                if 'Timeout' in error_msg or 'decrypt' in error_msg.lower():
                    raise Exception(
                        "Failed to launch Chrome with your profile. This usually means:\n"
                        "1. Chrome is currently open - Close ALL Chrome windows and try again\n"
                        "2. Profile encryption issues - Try using a different Chrome profile\n"
                        f"Original error: {error_msg}"
                    )
                else:
                    raise
        else:
            # Standard browser launch (no persistent profile)
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=launch_args
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                locale='en-US',
                timezone_id='America/New_York',
            )
            self.page = await self.context.new_page()
        
        # Add stealth scripts
        await self.page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        return self.page
    
    async def close(self):
        """Close browser and cleanup resources"""
        # Close page
        if self.page:
            try:
                if not self.page.is_closed():
                    await self.page.close()
            except Exception as e:
                print(f"Error closing page (non-critical): {str(e)[:100]}")

        # Close context
        if self.context:
            try:
                await self.context.close()
            except Exception as e:
                print(f"Error closing context (non-critical): {str(e)[:100]}")

        # Close browser
        if self.browser:
            try:
                await self.browser.close()
            except Exception as e:
                print(f"Error closing browser (non-critical): {str(e)[:100]}")

        # Stop playwright
        if self.playwright:
            try:
                await self.playwright.stop()
            except Exception as e:
                print(f"Error stopping playwright (non-critical): {str(e)[:100]}")
    
    async def navigate_to(self, url):
        """Navigate to URL"""
        if self.page:
            await self.page.goto(url, wait_until='networkidle', timeout=60000)
    
    async def wait_for_selector(self, selector, timeout=30000):
        """Wait for element to appear"""
        if self.page:
            return await self.page.wait_for_selector(selector, timeout=timeout)
    
    async def take_screenshot(self, path):
        """Take screenshot for debugging"""
        if self.page:
            await self.page.screenshot(path=path)
