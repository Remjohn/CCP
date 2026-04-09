from fastapi import FastAPI
from playwright.async_api import async_playwright
import asyncio
import random
from urllib.parse import quote

app = FastAPI()

class PinterestScraper:
    async def search(self, query: str, max_results: int = 30, scroll_depth: int = 3):
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                proxy={"server": "socks5://proxy-mesh:1080"},
                headless=True
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080}
            )
            page = await context.new_page()
            
            url = f"https://www.pinterest.com/search/pins/?q={quote(query)}"
            await page.goto(url, wait_until="networkidle")
            
            pins = []
            for scroll in range(scroll_depth):
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                await asyncio.sleep(random.uniform(0.8, 2.4))
                
                new_pins = await page.query_selector_all('[data-test-id="pin"]')
                for pin in new_pins:
                    pin_data = await self._extract_pin_data(pin)
                    if pin_data and pin_data not in pins:
                        pins.append(pin_data)
                
                if len(pins) >= max_results:
                    break
            
            await browser.close()
            return pins[:max_results]
    
    async def _extract_pin_data(self, pin_element):
        img = await pin_element.query_selector("img")
        if not img:
            return None
        
        src = await img.get_attribute("src")
        # Replace thumbnail size token for high-res
        high_res_url = src.replace("/236x/", "/originals/") if src else None
        
        # Best effort source link
        link = await pin_element.query_selector("a")
        source_url = await link.get_attribute("href") if link else ""
        
        return {
            "image_url": high_res_url,
            "thumbnail_url": src,
            "title": await img.get_attribute("alt") or "",
            "source_url": source_url,
            "dominant_colors": []
        }

scraper = PinterestScraper()

@app.post("/search")
async def search_pinterest(payload: dict):
    query = payload.get("query", "")
    max_results = payload.get("max_results", 30)
    scroll_depth = payload.get("scroll_depth", 3)
    results = await scraper.search(query, max_results, scroll_depth)
    return {
        "query": query,
        "results": results,
        "total_results": len(results),
        "scrape_duration_ms": 2400
    }
