import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking Google Search Console session...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "search.google.com/search-console" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                page = context.new_page()
                print("Created new tab for Google Search Console")
                page.goto("https://search.google.com/search-console", wait_until="domcontentloaded")
            
            page.wait_for_timeout(5000)
            print(f"Current URL: {page.url}")
            print(f"Current Title: {page.title()}")
            
            # Check if we are redirected to the GSC welcome or sign-in page
            is_logged_in = page.evaluate("""() => {
                const welcome = document.querySelector('div[data-g-event="welcome-page"]');
                const signin = document.querySelector('a[href*="signin"]');
                const propertySelector = document.querySelector('.search-console-property-selector, [aria-label*="Property"], [aria-label*="资源"], [aria-label*="属性"]');
                return {
                    welcomeExists: !!welcome,
                    signinExists: !!signin,
                    propertySelectorExists: !!propertySelector
                };
            }""")
            print("GSC Indicators:", is_logged_in)
            
            # Screenshot of the GSC page
            screenshot_path = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\gsc_status.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to: {screenshot_path}")
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
