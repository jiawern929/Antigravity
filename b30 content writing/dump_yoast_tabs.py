import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Dumping Yoast tabs and lists...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "iconicmafia.com" in p_page.url:
                    page = p_page
                    break
            
            if not page:
                print("Could not find iconicmafia.com tab.")
                return
            
            print(f"Found page: {page.url}")
            
            # Let's check what elements exist in the Yoast meta box
            yoast_details = page.evaluate("""() => {
                const results = [];
                // Look for any assessment tabs
                const tabs = document.querySelectorAll('.yoast-assessment-tabs button, .yoast-assessment-tab, button[class*="tab"]');
                const tabTexts = Array.from(tabs).map(t => t.innerText || t.getAttribute('aria-label') || t.className);
                
                // Get all list items or divs that have bad/ok/good classes
                const items = document.querySelectorAll('[class*="assessment"], [class*="analysis"], [class*="result"]');
                const itemDetails = [];
                items.forEach(el => {
                    if (el.innerText && el.innerText.length > 5 && el.innerText.length < 200) {
                        itemDetails.push({
                            tag: el.tagName,
                            class: el.className,
                            text: el.innerText
                        });
                    }
                });
                
                return {
                    tabTexts,
                    itemDetails: itemDetails.slice(0, 30)
                };
            }""")
            
            print("Tabs:")
            for t in yoast_details['tabTexts']:
                print(f"- {t}")
            print("\nItems:")
            for item in yoast_details['itemDetails']:
                print(f"[{item['tag']}] {item['class']}: {item['text']}")
                
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
