import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Loading Google Search Console dashboard...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Create a clean page to prevent matching any 404 or bad tab
            page = context.new_page()
            print("Navigating to GSC...")
            page.goto("https://search.google.com/search-console", wait_until="networkidle", timeout=60000)
            
            page.wait_for_timeout(5000)
            print(f"Loaded URL: {page.url}")
            print(f"Page Title: {page.title()}")
            
            # Screenshot of the GSC dashboard
            screenshot_path = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\gsc_dashboard.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to: {screenshot_path}")
            
            # Let's extract properties list if the property selector dropdown can be clicked
            # The dropdown button usually has class or text containing 'Property' or '资源'
            properties = page.evaluate("""() => {
                const results = [];
                // Look for elements representing properties or dropdown
                const dropdown = document.querySelector('.search-console-property-selector, [aria-label*="Property"], [aria-label*="资源"], [aria-label*="属性"]');
                if (dropdown) {
                    // Let's click it to open the list
                    dropdown.click();
                    return { clicked: true };
                }
                return { clicked: false };
            }""")
            
            print("Dropdown click status:", properties)
            if properties.get("clicked"):
                page.wait_for_timeout(2000)
                # Dump dropdown items
                items = page.evaluate("""() => {
                    const elements = document.querySelectorAll('[role="listbox"] [role="option"], .search-console-property-selector-menu-item, [data-value]');
                    return Array.from(elements).map(el => ({
                        text: el.innerText,
                        val: el.getAttribute('data-value')
                    }));
                }""")
                print("Properties list:")
                for item in items:
                    print(f"- Text: {item['text']} | Val: {item['val']}")
                    
            page.close()
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
