import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking active page in browser...")
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
                print("No iconicmafia.com tab found.")
                return
            
            print(f"Current URL: {page.url}")
            print(f"Current Title: {page.title()}")
            
            # Take a screenshot to see what's on the screen
            screenshot_path = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\yoast_result_iconicmafia.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to: {screenshot_path}")
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
