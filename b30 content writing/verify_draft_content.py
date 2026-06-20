import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Fetching draft content...")
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
            
            content = page.evaluate("() => wp.data.select('core/editor').getEditedPostAttribute('content')")
            print("="*60)
            print("DRAFT CONTENT:")
            print(content)
            print("="*60)
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
