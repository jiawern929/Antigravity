import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

site_url = "https://businessinsider101.com/wp-admin/post-new.php"

def run():
    print(f"Connecting to Chrome to prepare new post editor...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "businessinsider101.com" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find the businessinsider101.com tab. Creating one.")
                page = context.new_page()
            
            print(f"Navigating to: {site_url}...")
            page.goto(site_url)
            print("Waiting for Gutenberg to load...")
            page.wait_for_function("() => window.wp && window.wp.data && window.wp.data.dispatch")
            print(f"Gutenberg loaded! Current URL: {page.url}")
            
        except Exception as e:
            print("Error preparing editor:", e)

if __name__ == "__main__":
    run()
