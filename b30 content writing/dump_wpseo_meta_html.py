import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Dumping wpseo_meta inner HTML...")
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
            
            html = page.evaluate("() => document.querySelector('#wpseo_meta') ? document.querySelector('#wpseo_meta').innerHTML : 'not found'")
            
            with open("wpseo_meta.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("Successfully written wpseo_meta.html")
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
