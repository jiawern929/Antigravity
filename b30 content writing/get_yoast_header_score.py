import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking Gutenberg header Yoast score...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "top50malaysia.com" in p_page.url:
                    page = p_page
                    break
            
            if not page:
                print("Could not find top50malaysia.com tab.")
                return
            
            print(f"Found page: {page.url}")
            
            header_data = page.evaluate("""() => {
                const buttons = document.querySelectorAll('.interface-pinned-items button, .editor-header button, button[class*="yoast"], button[aria-label*="Yoast"]');
                const results = [];
                buttons.forEach(b => {
                    results.push({
                        text: b.innerText,
                        ariaLabel: b.getAttribute('aria-label'),
                        className: b.className,
                        html: b.innerHTML.substring(0, 200)
                    });
                });
                return results;
            }""")
            
            print("Buttons in header/toolbar:")
            for r in header_data:
                print(r)
                
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
