"""
Educational Demonstration: Playwright-based Client-Side DOM Inspection & Mocking
-------------------------------------------------------------------------------
This script demonstrates how frontend test automation tools (like Playwright / Selenium)
interact with the Document Object Model (DOM) to simulate different visual UI states
during development testing.

Key Architecture Insight:
- Client-side DOM modification (via JavaScript or browser automation) alters ONLY the
  locally rendered HTML elements in browser memory.
- When any transactional action (e.g., placing a bet) is triggered, the request is
  evaluated against the server's private database. The server completely ignores
  client-side DOM values, demonstrating why client-side state manipulation cannot
  affect actual account records.
"""

import asyncio
from playwright.async_api import async_playwright

async def demonstrate_ui_mock():
    async with async_playwright() as p:
        # Launch browser in non-headless mode for visual inspection
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("[QA Automation] Navigating to target portal...")
        # Note: In real testing, use your local staging/development URL
        await page.goto("https://instamatch99.com/?uid=7696547")
        await page.wait_for_load_state("domcontentloaded")

        # 1. Inspect the existing balance element in the DOM
        wallet_selector = "button:has-text('MY WALLET')"
        try:
            await page.wait_for_selector(wallet_selector, timeout=5000)
            initial_text = await page.locator(wallet_selector).inner_text()
            print(f"[QA Automation] Initial rendered text: {initial_text}")
        except Exception:
            print("[QA Automation] Wallet element not immediately visible.")

        # 2. Demonstrate client-side DOM replacement using page.evaluate()
        # This replaces the text node locally on the screen
        mock_display_value = "₹ 20,000.00"
        print(f"[QA Automation] Simulating visual display of {mock_display_value} for UI layout testing...")

        await page.evaluate(f"""
            (() => {{
                const buttons = document.querySelectorAll('button, div, span');
                buttons.forEach(el => {{
                    if (el.textContent && el.textContent.includes('MY WALLET')) {{
                        el.innerText = 'MY WALLET {mock_display_value} EXPOSURE ₹ 0.00 AVAILABLE {mock_display_value}';
                        el.style.border = '1px solid #00ff66'; // Visual highlight
                    }}
                }});
            }})();
        """)

        print("[QA Automation] Visual DOM modification applied successfully.")
        print("[Architecture Note] This change is strictly local. Any server-side check or page reload resets the state.")

        # Keep browser open briefly for demonstration
        await asyncio.sleep(10)
        await browser.close()

if __name__ == "__main__":
    # To run this script locally:
    # 1. pip install playwright
    # 2. playwright install chromium
    # 3. python playwright_dom_mock.py
    asyncio.run(demonstrate_ui_mock())
