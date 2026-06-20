import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to Chrome to expand Yoast SEO analysis...")
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
            
            # Find the SEO analysis header and click it if collapsed
            # Typically it has a class like .yoast-analysis-results__header or is a button containing "SEO" or "SEO分析"
            print("Locating headers...")
            
            # Let's log all buttons inside the Yoast SEO box
            buttons = page.evaluate("""() => {
                const list = [];
                const el = document.getElementById('wpseo_meta');
                if (el) {
                    const btns = el.querySelectorAll('button');
                    btns.forEach((b, i) => {
                        list.push({ index: i, text: b.innerText, id: b.id, className: b.className });
                    });
                }
                return list;
            }""")
            
            print("Buttons found in #wpseo_meta:")
            for b in buttons:
                print(f"[{b['index']}] Text: {b['text']} | Class: {b['className']}")
                
            # Click the SEO Analysis section if it's there. Usually it's the toggle header.
            # In the screenshot, there is a collapsible heading: "SEO analysis" or "SEO分析"
            # Let's click it using text matching
            header_locator = page.locator('button:has-text("SEO分析"), button:has-text("SEO analysis")').first
            if header_locator.is_visible():
                header_locator.click()
                print("Clicked SEO analysis header.")
                page.wait_for_timeout(2000)
            
            # Let's also look for `.yoast-analysis-results__header`
            toggle = page.locator('.yoast-analysis-results__header, .yoast-analysis-results__layout button').first
            if toggle.is_visible():
                toggle.click()
                print("Clicked toggle.")
                page.wait_for_timeout(2000)
                
            # Let's print out all list items in #wpseo_meta to check if they appeared
            items = page.evaluate("""() => {
                const list = [];
                const lis = document.querySelectorAll('#wpseo_meta li');
                lis.forEach(l => list.push(l.innerText));
                return list;
            }""")
            
            print("All list items currently in #wpseo_meta:")
            for item in items:
                if item.strip():
                    print(f"- {item}")
                    
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
