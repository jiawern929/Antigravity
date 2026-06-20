import sys
import time
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

site_url = "https://businessinsider101.com/wp-admin/"
username = "jwern929@gmail.com"
password = "PFHx1pBpwoD*7#lPthajn!YC"

def run():
    print(f"Connecting to Chrome to log in to: {site_url}...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Check if there is already a tab with this site
            page = None
            for p_page in context.pages:
                if "businessinsider101.com" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    print(f"Found existing tab: {page.url}")
                    break
            
            if not page:
                page = context.new_page()
                print("Created new tab.")
            
            print(f"Navigating to: {site_url}...")
            page.goto(site_url)
            page.wait_for_timeout(3000)
            
            # Check if we are on the login page
            if "wp-login.php" in page.url:
                print("Redirected to login page. Logging in...")
                
                # Fill Username
                page.locator('#user_login').fill(username)
                page.wait_for_timeout(500)
                
                # Fill Password
                page.locator('#user_pass').fill(password)
                page.wait_for_timeout(500)
                
                # Click Login
                page.locator('#wp-submit').click()
                print("Submitted login form.")
                page.wait_for_timeout(8000)
                
            # Verify if logged in
            if "wp-admin" in page.url and "wp-login.php" not in page.url:
                print(f"Login successful! Current URL: {page.url}")
            else:
                print(f"Failed to log in. Current URL: {page.url}")
                
        except Exception as e:
            print("Error logging in:", e)

if __name__ == "__main__":
    run()
