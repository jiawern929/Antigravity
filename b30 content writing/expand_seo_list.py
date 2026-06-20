import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to Chrome to expand Yoast SEO Analysis bullets...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "businessinsider101.com/wp-admin" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find the open editor tab.")
                return
            
            # Click the SEO Analysis collapsible button
            print("Locating SEO Analysis toggle button...")
            toggle_btn = page.locator('button:has-text("SEO分析")').first
            if toggle_btn.is_visible():
                toggle_btn.click()
                print("Clicked SEO analysis toggle. Waiting for animation...")
                page.wait_for_timeout(2000)
            else:
                print("SEO analysis toggle button not visible.")
                
            # Print list items
            items = page.evaluate("""() => {
                const list = [];
                const lis = document.querySelectorAll('#wpseo_meta li');
                lis.forEach(l => list.push(l.innerText));
                return list;
            }""")
            
            print("List items inside #wpseo_meta:")
            for item in items:
                if item.strip():
                    print(f"- {item}")
                    
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
