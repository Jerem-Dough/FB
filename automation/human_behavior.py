"""
Human-like behavior simulation for browser automation
"""
import random
import time
import asyncio

class HumanBehavior:
    """Simulates human-like interactions to avoid detection"""
    
    @staticmethod
    def random_delay(min_seconds=1, max_seconds=3):
        """Random delay between actions"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    @staticmethod
    async def async_random_delay(min_seconds=1, max_seconds=3):
        """Async random delay between actions"""
        delay = random.uniform(min_seconds, max_seconds)
        await asyncio.sleep(delay)
    
    @staticmethod
    async def human_type(page, selector, text, min_delay=0.05, max_delay=0.15):
        """Type text character by character with random delays"""
        element = await page.query_selector(selector)
        if element:
            await element.click()
            await asyncio.sleep(random.uniform(0.2, 0.5))
            
            for char in text:
                await element.type(char)
                await asyncio.sleep(random.uniform(min_delay, max_delay))
    
    @staticmethod
    async def human_click(page, selector):
        """Click with small random delay"""
        await asyncio.sleep(random.uniform(0.3, 0.8))
        await page.click(selector)
        await asyncio.sleep(random.uniform(0.5, 1.5))
    
    @staticmethod
    async def scroll_smoothly(page, distance=500):
        """Scroll the page smoothly"""
        await page.evaluate(f"""
            window.scrollBy({{
                top: {distance},
                left: 0,
                behavior: 'smooth'
            }});
        """)
        await asyncio.sleep(random.uniform(1, 2))
    
    @staticmethod
    def random_mouse_movement():
        """Generate random mouse movements (for future implementation)"""
        # This could be expanded to move mouse in natural patterns
        pass
    
    @staticmethod
    def typing_speed_variation():
        """Vary typing speed to seem more human"""
        speeds = {
            'slow': (0.15, 0.30),
            'medium': (0.08, 0.15),
            'fast': (0.03, 0.08)
        }
        return random.choice(list(speeds.values()))
    
    @staticmethod
    async def random_pause(page):
        """Random pause like a human thinking"""
        await asyncio.sleep(random.uniform(2, 5))
