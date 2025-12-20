"""
Facebook Marketplace posting automation
"""
import asyncio
import random
from pathlib import Path
from automation.human_behavior import HumanBehavior

class MarketplaceAutomation:
    def __init__(self, browser_manager):
        self.browser = browser_manager
        self.page = None
        self.human = HumanBehavior()
    
    async def initialize(self):
        """Initialize browser and navigate to Marketplace"""
        self.page = await self.browser.start()

        print("Navigating to Facebook Marketplace...")
        await self.browser.navigate_to("https://www.facebook.com/marketplace/create/item")
        await self.human.async_random_delay(3, 5)

        # Check if we need to log in
        print("Checking if logged in...")
        current_url = self.page.url
        print(f"Current URL: {current_url}")

        # Check for login page
        if "login" in current_url.lower() or "checkpoint" in current_url.lower():
            print("\n" + "="*60)
            print("NOT LOGGED IN - Please log in to Facebook")
            print("="*60)
            print("The browser window is now open.")
            print("Please log in to Facebook manually in the browser window.")
            print("The automation will wait for you to complete login...")
            print("="*60 + "\n")

            # Wait for navigation away from login page (max 5 minutes)
            try:
                await self.page.wait_for_url(lambda url: "login" not in url.lower(), timeout=300000)
                print("Login detected! Continuing...")

                # Navigate to marketplace again after login
                await self.browser.navigate_to("https://www.facebook.com/marketplace/create/item")
                await self.human.async_random_delay(3, 5)
            except Exception as e:
                raise Exception("Login timeout - please log in within 5 minutes")

        # Verify we're on the right page
        final_url = self.page.url
        print(f"Final URL: {final_url}")

        if "marketplace/create" not in final_url:
            raise Exception(
                f"Not on the create listing page. Current page: {final_url}\n"
                "You may need to manually navigate to Marketplace > Create New Listing"
            )

        # Dismiss common Facebook popups
        await self._dismiss_popups()
    
    async def create_listing(self, title, description, price, category, condition, location, image_paths, delivery_method="Door pickup", group_names=None, boost_listing=False):
        """
        Create a Facebook Marketplace listing

        Args:
            title: Listing title
            description: Listing description
            price: Price as float
            category: Category string
            condition: "New", "Used - Like New", "Used - Good", "Used - Fair"
            location: Location string
            image_paths: List of image file paths
            delivery_method: "Public meetup", "Door pickup", or "Door dropoff" (default: "Door pickup")
            group_names: List of group names to list in (optional, max 20)
            boost_listing: Whether to enable boost listing (default: False)

        Returns:
            dict: {'success': bool, 'error': str or None}
        """
        try:
            print(f"\nCreating listing: {title}")
            await self.human.async_random_delay(0.5, 1)
            await self._dismiss_popups()

            # STEP 1: Fill in all listing details
            await self._upload_images(image_paths)
            await self.human.async_random_delay(0.8, 1.2)  # Wait for form to load after upload

            await self._fill_title(title)
            await self._fill_price(price)
            await self._select_category(category)
            await self._select_condition(condition)
            await self._fill_description(description)

            if location:
                await self._fill_location(location)

            # Enable boost if requested (must be done BEFORE first Next click)
            if boost_listing:
                await self._toggle_boost_listing()

            # STEP 2: Click "Next" to go to delivery method page
            print("\n[STEP 1] Clicking Next to go to delivery page...")
            await self._click_next_button()
            print("✓ Clicked Next button")
            await self.human.async_random_delay(0.8, 1.2)

            # STEP 3: Select delivery method on the new page
            print("\n[STEP 2] Selecting delivery method...")
            await self._select_delivery_method(delivery_method)
            await self.human.async_random_delay(0.5, 0.8)

            # STEP 4: Click "Next" again to go to groups page
            print("\n[STEP 3] Clicking Next to go to groups page...")
            await self._click_next_button()
            print("✓ Clicked Next button")
            await self.human.async_random_delay(0.8, 1.2)

            # STEP 5: Select groups
            print("\n[STEP 4] Selecting groups...")
            await self._select_groups(group_names)
            await self.human.async_random_delay(0.5, 0.8)

            # STEP 6: Click "Next" one more time (there might be another Next after groups)
            print("\n[STEP 5] Checking for additional Next button...")

            # Try to find Next or Publish button
            has_next = await self.page.evaluate("""
                () => {
                    const spans = Array.from(document.querySelectorAll('span'));
                    return spans.some(span => (span.innerText || span.textContent || '').trim() === 'Next');
                }
            """)

            if has_next:
                print("Found Next button, clicking it...")
                await self._click_next_button()
                print("✓ Clicked Next button")
                await self.human.async_random_delay(0.8, 1.2)

            # STEP 7: Click "Publish" to complete
            print("\n[STEP 6] Clicking Publish to complete listing...")
            await self._click_publish_button()
            print("✓ Clicked Publish button")
            await self.human.async_random_delay(1, 1.5)

            print(f"✓ Listing created successfully!\n")

            # Navigate back to create listing page for next listing
            print("Navigating back to create listing page for next listing...")
            await self.human.async_random_delay(2, 3)  # Wait for confirmation page to load
            await self.browser.navigate_to("https://www.facebook.com/marketplace/create/item")
            await self.human.async_random_delay(2, 3)  # Wait for create page to load
            await self._dismiss_popups()

            return {'success': True, 'error': None}

        except Exception as e:
            print(f"Error creating listing: {str(e)}")

            # Try to navigate back to create listing page even on error
            try:
                print("Attempting to navigate back to create listing page after error...")
                await self.human.async_random_delay(1, 2)
                await self.browser.navigate_to("https://www.facebook.com/marketplace/create/item")
                await self.human.async_random_delay(2, 3)
                await self._dismiss_popups()
            except:
                pass  # Ignore navigation errors during error recovery

            return {'success': False, 'error': str(e)}
    
    async def _upload_images(self, image_paths):
        """Upload images to listing"""
        try:
            # Wait for page to fully load
            await self.human.async_random_delay(1.5, 2)

            # Find file input (it exists on page, might be hidden)
            file_input = await self.page.query_selector('input[type="file"][accept*="image"]')

            if file_input:
                # Convert paths to absolute paths
                abs_paths = [str(Path(p).resolve()) for p in image_paths]

                # Make file input visible (it's usually hidden)
                await self.page.evaluate("""
                    (selector) => {
                        const input = document.querySelector(selector);
                        if (input) {
                            input.style.display = 'block';
                            input.style.visibility = 'visible';
                            input.style.opacity = '1';
                        }
                    }
                """, 'input[type="file"][accept*="image"]')

                # Upload files
                await file_input.set_input_files(abs_paths)
                print(f"✓ Uploaded {len(image_paths)} image(s)")
                await self.human.async_random_delay(1, 1.5)
            else:
                raise Exception("Could not find image upload input")

        except Exception as e:
            raise Exception(f"Failed to upload images: {str(e)}")
    
    async def _fill_title(self, title):
        """Fill in listing title - uses first visible text input"""
        # Get all text inputs, filter visible ones (excluding search)
        text_inputs = await self.page.query_selector_all('input[type="text"]')
        for inp in text_inputs:
            is_visible = await inp.is_visible()
            aria_label = await inp.get_attribute('aria-label') or ''
            placeholder = await inp.get_attribute('placeholder') or ''
            if is_visible and 'search' not in aria_label.lower() and 'search' not in placeholder.lower():
                await inp.fill("")
                await self.human.human_type(self.page, 'input[type="text"]', title)
                print("✓ Title entered")
                return
        raise Exception("Could not find title input field")
    
    async def _fill_price(self, price):
        """Fill in price - uses second visible text input"""
        price_str = str(int(price)) if price == int(price) else str(price)

        # Get all text inputs, find the second visible one (first is title, second is price)
        text_inputs = await self.page.query_selector_all('input[type="text"]')
        visible_text_inputs = []
        for inp in text_inputs:
            is_visible = await inp.is_visible()
            aria_label = await inp.get_attribute('aria-label') or ''
            placeholder = await inp.get_attribute('placeholder') or ''
            if is_visible and 'search' not in aria_label.lower() and 'search' not in placeholder.lower():
                visible_text_inputs.append(inp)

        if len(visible_text_inputs) >= 2:
            price_input = visible_text_inputs[1]
            await price_input.fill("")
            for char in price_str:
                await price_input.type(char)
                await asyncio.sleep(random.uniform(0.03, 0.08))
            print("✓ Price entered")
            return

        raise Exception("Could not find price input field")
    
    async def _select_category(self, category):
        """Select category - type and pick from Facebook's dropdown suggestions"""
        try:
            print(f"Looking for category field to enter: {category}")

            # Look for category field by aria-label
            category_selectors = [
                'input[aria-label*="Category" i]',
                'input[aria-label*="category" i]',
                'input[type="search"]',
                'input[role="combobox"]'
            ]

            for selector in category_selectors:
                try:
                    inputs = await self.page.query_selector_all(selector)
                    for inp in inputs:
                        is_visible = await inp.is_visible()
                        if not is_visible:
                            continue

                        aria_label = (await inp.get_attribute('aria-label') or '').lower()

                        # Found the category field
                        if 'category' in aria_label:
                            print("✓ Found category field")

                            # Click the field to focus it
                            await inp.click()
                            await self.human.async_random_delay(0.2, 0.3)

                            # Clear any existing text
                            await inp.fill("")
                            await self.human.async_random_delay(0.1, 0.2)

                            # Type just the first few characters to trigger dropdown
                            search_term = category[:5] if len(category) > 5 else category
                            for char in search_term:
                                await inp.type(char)
                                await asyncio.sleep(random.uniform(0.08, 0.15))

                            print(f"✓ Typed search term: {search_term}")

                            # Wait for dropdown to populate
                            await self.human.async_random_delay(1, 1.5)

                            # PRIMARY METHOD: Use keyboard to select (most reliable)

                            # Press ArrowDown to highlight first option
                            await inp.press("ArrowDown")
                            await self.human.async_random_delay(0.3, 0.5)

                            # Press Enter to select it
                            await inp.press("Enter")
                            await self.human.async_random_delay(0.5, 0.8)

                            # Verify something was selected by checking field value
                            is_valid = await self.page.evaluate("""
                                () => {
                                    const categoryInput = document.querySelector('input[aria-label*="Category" i]');
                                    if (categoryInput) {
                                        const value = categoryInput.value;
                                        // Check if it's more than just what we typed
                                        return value && value.length > 5;
                                    }
                                    return false;
                                }
                            """)

                            if is_valid:
                                print(f"✓ Selected category from dropdown using keyboard")
                                return
                            else:
                                # BACKUP: Try clicking dropdown option directly
                                dropdown_clicked = await self.page.evaluate("""
                                    () => {
                                        const selectors = [
                                            'div[role="option"]',
                                            'li[role="option"]',
                                            '[role="listbox"] div',
                                            'div[role="menuitem"]'
                                        ];

                                        for (const selector of selectors) {
                                            const options = Array.from(document.querySelectorAll(selector));
                                            if (options.length > 0) {
                                                for (const option of options) {
                                                    if (option.offsetParent !== null) {
                                                        option.click();
                                                        return true;
                                                    }
                                                }
                                            }
                                        }
                                        return false;
                                    }
                                """)

                                if dropdown_clicked:
                                    print(f"✓ Selected category by clicking dropdown")
                                    await self.human.async_random_delay(0.3, 0.5)
                                    return
                                else:
                                    print("WARNING: Could not select category from dropdown")
                                    return
                except Exception as e:
                    print(f"Error in this selector: {str(e)[:100]}")
                    continue

            raise Exception("Could not find category input field")

        except Exception as e:
            raise Exception(f"Error setting category: {str(e)}")
    
    async def _select_condition(self, condition):
        """Select item condition"""
        try:
            print(f"Looking for condition field to select: {condition}")

            # STEP 1: Find and click the condition dropdown/selector
            dropdown_opened = await self.page.evaluate("""
                () => {
                    // Look for elements containing "Condition" text
                    const allElements = Array.from(document.querySelectorAll('div, label, span'));

                    for (const el of allElements) {
                        const text = (el.innerText || el.textContent || '').trim();

                        // Found an element with "Condition" text
                        if (text === 'Condition' || text.toLowerCase().includes('condition')) {
                            // Try to find a clickable parent or sibling
                            let clickTarget = el;

                            // Check if element itself is clickable
                            if (el.onclick || el.getAttribute('role') === 'button') {
                                el.click();
                                return true;
                            }

                            // Try parent elements
                            let parent = el.parentElement;
                            let attempts = 0;
                            while (parent && attempts < 5) {
                                const role = parent.getAttribute('role');
                                const ariaLabel = (parent.getAttribute('aria-label') || '').toLowerCase();

                                if (role === 'button' || role === 'combobox' ||
                                    ariaLabel.includes('condition') || parent.onclick) {
                                    parent.click();
                                    return true;
                                }
                                parent = parent.parentElement;
                                attempts++;
                            }

                            // Try clicking the element itself as last resort
                            el.click();
                            return true;
                        }
                    }
                    return false;
                }
            """)

            if dropdown_opened:
                print("✓ Opened condition dropdown")
                await self.human.async_random_delay(0.8, 1.2)
            else:
                print("WARNING: Could not find condition dropdown")
                return

            # STEP 2: Click the specific condition option from dropdown
            condition_selected = await self.page.evaluate(f"""
                (conditionText) => {{
                    // Wait a moment for dropdown to populate
                    const allElements = Array.from(document.querySelectorAll('div, span, li, [role="option"]'));

                    for (const el of allElements) {{
                        const text = (el.innerText || el.textContent || '').trim();

                        // Exact match or contains the condition text
                        if (text === conditionText || text.includes(conditionText)) {{
                            // Make sure element is visible
                            if (el.offsetParent !== null) {{
                                el.click();
                                return true;
                            }}
                        }}
                    }}

                    return false;
                }}
            """, condition)

            if condition_selected:
                print(f"✓ Selected condition: {condition}")
                await self.human.async_random_delay(0.5, 0.8)
            else:
                print(f"WARNING: Could not select condition '{condition}' from dropdown, using default")

        except Exception as e:
            print(f"WARNING: Error setting condition: {str(e)}")
    
    async def _fill_description(self, description):
        """Fill in description - uses textarea element"""
        # Find first visible textarea
        textareas = await self.page.query_selector_all('textarea')
        for ta in textareas:
            is_visible = await ta.is_visible()
            if is_visible:
                await ta.click()
                await asyncio.sleep(0.2)
                await ta.fill("")
                for char in description:
                    await ta.type(char)
                    await asyncio.sleep(random.uniform(0.01, 0.03))
                print("✓ Description entered")
                return

        raise Exception("Could not find description field")
    
    async def _fill_location(self, location):
        """Fill in location"""
        try:
            location_selectors = [
                'input[placeholder*="location" i]',
                'input[aria-label*="location" i]'
            ]

            for selector in location_selectors:
                try:
                    element = await self.page.wait_for_selector(selector, timeout=5000)
                    if element:
                        await element.fill("")
                        await self.human.human_type(self.page, selector, location)
                        await self.human.async_random_delay(0.5, 0.8)

                        # Press Enter or click first suggestion
                        await element.press("Enter")
                        await self.human.async_random_delay(0.5, 0.8)
                        return
                except:
                    continue

            print(f"Warning: Could not set location to {location}")

        except Exception as e:
            print(f"Warning: Error setting location: {str(e)}")

    async def _select_delivery_method(self, method="Door pickup"):
        """
        Select delivery method checkbox
        Options: 'Public meetup', 'Door pickup', 'Door dropoff'
        """
        try:
            print(f"Looking for delivery method: {method}")

            # Try to find and click the delivery method
            delivery_clicked = await self.page.evaluate(f"""
                (methodText) => {{
                    // Find all divs and labels
                    const allElements = Array.from(document.querySelectorAll('div, label, span'));

                    for (const el of allElements) {{
                        const text = (el.innerText || el.textContent || '').toLowerCase().trim();

                        // Check if this element's direct text matches our delivery method
                        if (text === methodText.toLowerCase() ||
                            text.includes(methodText.toLowerCase().replace(' ', ''))) {{

                            // Try clicking the element itself
                            if (el.onclick || el.getAttribute('role') === 'checkbox') {{
                                el.click();
                                return true;
                            }}

                            // Try finding parent that's clickable
                            let parent = el.parentElement;
                            let attempts = 0;
                            while (parent && attempts < 5) {{
                                const role = parent.getAttribute('role');
                                if (role === 'checkbox' || parent.onclick) {{
                                    parent.click();
                                    return true;
                                }}
                                parent = parent.parentElement;
                                attempts++;
                            }}

                            // Try to find any checkbox within this element's parent
                            const parentEl = el.closest('label, div');
                            if (parentEl) {{
                                const checkbox = parentEl.querySelector('input[type="checkbox"]');
                                if (checkbox) {{
                                    checkbox.click();
                                    return true;
                                }}

                                // Try clicking the parent itself
                                parentEl.click();
                                return true;
                            }}
                        }}
                    }}

                    return false;
                }}
            """, method)

            if delivery_clicked:
                print(f"✓ Selected delivery method: {method}")
                await self.human.async_random_delay(0.5, 0.8)
            else:
                print(f"WARNING: Could not find delivery method checkbox for '{method}'")

        except Exception as e:
            print(f"ERROR: Exception selecting delivery method: {str(e)}")

    async def _select_groups(self, group_names=None):
        """
        Select groups to list in (up to 20 groups)
        If group_names is None or empty, selects the first available group
        """
        try:
            print("Looking for groups to select...")

            if not group_names:
                # Select first available group by default
                selected = await self.page.evaluate("""
                    () => {
                        const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"]'));

                        for (const checkbox of checkboxes) {
                            const parent = checkbox.closest('label, div[role="checkbox"], div');
                            if (parent && !checkbox.checked) {
                                checkbox.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)

                if selected:
                    print("✓ Selected first available group")
                    await self.human.async_random_delay(0.5, 0.8)
                else:
                    print("Warning: No groups found to select (may not be required)")
            else:
                # Select specific groups
                selected_count = 0
                for group_name in group_names[:20]:  # Limit to 20 groups
                    group_selected = await self.page.evaluate(f"""
                        (groupName) => {{
                            const checkboxes = Array.from(document.querySelectorAll('input[type="checkbox"]'));

                            for (const checkbox of checkboxes) {{
                                const parent = checkbox.closest('label, div[role="checkbox"], div');
                                if (parent) {{
                                    const text = parent.textContent || '';
                                    if (text.includes(groupName) && !checkbox.checked) {{
                                        checkbox.click();
                                        return true;
                                    }}
                                }}
                            }}
                            return false;
                        }}
                    """, group_name)

                    if group_selected:
                        selected_count += 1
                        await self.human.async_random_delay(0.3, 0.5)

                if selected_count > 0:
                    print(f"✓ Selected {selected_count} group(s)")
                else:
                    print("Warning: No matching groups found")

        except Exception as e:
            print(f"Warning: Error selecting groups: {str(e)}")

    async def _toggle_boost_listing(self):
        """
        Toggle boost listing switch (must be called BEFORE first Next click)
        """
        try:
            print("Looking for boost listing toggle...")

            # Find and click the boost switch
            boost_toggled = await self.page.evaluate("""
                () => {
                    // Look for switch/checkbox with role="switch"
                    const switches = Array.from(document.querySelectorAll('input[role="switch"], input[type="checkbox"][aria-checked]'));

                    for (const switchEl of switches) {
                        const ariaLabel = switchEl.getAttribute('aria-label') || '';
                        const ariaChecked = switchEl.getAttribute('aria-checked') || '';

                        // Only proceed if switch is currently off
                        if (ariaChecked === 'false' || ariaLabel.toLowerCase().includes('disabled')) {
                            // Try to find parent container that might have boost-related text
                            let parent = switchEl.closest('div[role="group"], label, div');
                            if (parent) {
                                const parentText = (parent.textContent || '').toLowerCase();
                                // ONLY click if we find boost/promote keywords - no fallback clicking
                                if (parentText.includes('boost') || parentText.includes('promote') ||
                                    parentText.includes('featured') || parentText.includes('sponsored')) {
                                    // Make sure the switch is visible before clicking
                                    if (switchEl.offsetParent !== null) {
                                        switchEl.click();
                                        return true;
                                    }
                                }
                            }
                        }
                    }
                    return false;
                }
            """)

            if boost_toggled:
                print("✓ Boost listing enabled")
                await self.human.async_random_delay(0.5, 0.8)
            else:
                print("Warning: Could not find boost listing toggle (this is OK if boost isn't available)")

        except Exception as e:
            print(f"Warning: Error toggling boost listing: {str(e)}")

    async def _click_next_button(self):
        """Click the Next button"""
        clicked = await self.page.evaluate("""
            () => {
                // Find all spans with "Next" text
                const spans = Array.from(document.querySelectorAll('span'));

                for (const span of spans) {
                    const text = (span.innerText || span.textContent || '').trim();

                    if (text === 'Next') {
                        // Find the clickable parent (button or div with role=button)
                        let parent = span.parentElement;
                        let attempts = 0;

                        while (parent && attempts < 10) {
                            const role = parent.getAttribute('role');
                            const tagName = parent.tagName.toLowerCase();

                            if (tagName === 'button' || role === 'button') {
                                parent.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                setTimeout(() => parent.click(), 300);
                                return true;
                            }

                            parent = parent.parentElement;
                            attempts++;
                        }
                    }
                }
                return false;
            }
        """)

        if not clicked:
            raise Exception("Could not find Next button")

        return clicked

    async def _click_publish_button(self):
        """Click the Publish button"""
        clicked = await self.page.evaluate("""
            () => {
                // Find all spans with "Publish" text
                const spans = Array.from(document.querySelectorAll('span'));

                for (const span of spans) {
                    const text = (span.innerText || span.textContent || '').trim();

                    if (text === 'Publish') {
                        // Find the clickable parent (button or div with role=button)
                        let parent = span.parentElement;
                        let attempts = 0;

                        while (parent && attempts < 10) {
                            const role = parent.getAttribute('role');
                            const tagName = parent.tagName.toLowerCase();

                            if (tagName === 'button' || role === 'button') {
                                parent.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                setTimeout(() => parent.click(), 300);
                                return true;
                            }

                            parent = parent.parentElement;
                            attempts++;
                        }
                    }
                }
                return false;
            }
        """)

        if not clicked:
            raise Exception("Could not find Publish button")

        return clicked


    async def _dismiss_popups(self):
        """Dismiss common Facebook popups that block the page"""
        # Common popup dismissal patterns
        dismiss_buttons = [
            'div[aria-label="Not now" i]',
            'button:has-text("Not now")',
            '[role="button"]:has-text("Not now")',
            'button:has-text("Accept all")',
            'button:has-text("Block")',
            '[aria-label*="Close" i]',
            '[data-testid="close"]',
        ]

        dismissed_count = 0
        for selector in dismiss_buttons:
            try:
                button = await self.page.wait_for_selector(selector, timeout=2000)
                if button and await button.is_visible():
                    await button.click()
                    dismissed_count += 1
                    await self.human.async_random_delay(0.5, 0.8)
            except:
                continue

        if dismissed_count > 0:
            await self.human.async_random_delay(1, 1.5)

    async def close(self):
        """Close browser and cleanup resources"""
        try:
            await self.browser.close()
        except Exception as e:
            print(f"Error closing browser (non-critical): {str(e)[:100]}")
