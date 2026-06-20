import os
import sys
import time
from playwright.sync_api import sync_playwright

def login():
    print("Starting Playwright headed browser...")
    with sync_playwright() as p:
        # Launch browser in headed mode
        # Using chrome/edge channel if available is less likely to trigger bot detection,
        # but default chromium is also supported. We fallback to default if channel launch fails.
        browser = None
        for channel in ["chrome", "msedge", None]:
            try:
                if channel:
                    print(f"Attempting to launch with channel={channel}...")
                    browser = p.chromium.launch(
                        headless=False,
                        channel=channel,
                        args=["--start-maximized"]
                    )
                else:
                    print("Attempting to launch default Chromium...")
                    browser = p.chromium.launch(
                        headless=False,
                        args=["--start-maximized"]
                    )
                break
            except Exception as launch_err:
                print(f"Could not launch browser with channel {channel}: {launch_err}")

        if not browser:
            print("Error: Could not launch any browser. Please ensure Google Chrome or Microsoft Edge is installed.")
            return

        # Create context with a modern User Agent and standard viewport
        context = browser.new_context(
            viewport=None,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Bypass navigator.webdriver detection
        page = context.new_page()
        page.add_init_script("delete navigator.__proto__.webdriver;")

        print("Navigating to Gmail...")
        page.goto("https://mail.google.com")

        email = "jwern929@gmail.com"
        password = "Todayisagoodday99@"

        try:
            # Wait for email input field
            print("Checking for email input field...")
            page.wait_for_selector("input[type='email']", timeout=8000)
            print("Entering email...")
            page.type("input[type='email']", email, delay=100)
            
            # Click Next
            print("Clicking next...")
            page.click("#identifierNext")
            
            # Wait for password input field
            print("Waiting for password input field...")
            page.wait_for_selector("input[type='password']", timeout=8000)
            print("Entering password...")
            page.type("input[type='password']", password, delay=100)
            
            # Click Next
            print("Clicking next...")
            page.click("#passwordNext")
        except Exception as e:
            print("\n[Notice] Semi-automated fill hit a bump (this is normal if Google showed a verification screen or different layout).")
            print("Please interact with the browser window directly to complete the login.")

        print("\n" + "="*70)
        print("ACTION REQUIRED ON YOUR SCREEN:")
        print("1. A browser window has opened on your computer.")
        print("2. Enter your email/password if not already filled.")
        print("3. Complete any verification (2FA prompt on phone or security code).")
        print("4. Keep the browser open until you see your Gmail Inbox.")
        print("5. Once you are successfully in the inbox, this script will save the session and close automatically.")
        print("="*70 + "\n")

        login_success = False
        start_time = time.time()
        timeout_seconds = 180  # 3 minutes to complete login

        while time.time() - start_time < timeout_seconds:
            try:
                current_url = page.url
                # Check if we reached the Gmail inbox
                if "mail.google.com/mail" in current_url:
                    print("Gmail Inbox detected! Saving session...")
                    login_success = True
                    break
            except Exception:
                # Browser might have been closed
                print("Browser connection lost.")
                break
            time.sleep(1)

        if login_success:
            # Wait 3 seconds to ensure storage and cookies are fully initialized
            time.sleep(3)
            session_file = "gmail_session.json"
            context.storage_state(path=session_file)
            print(f"\n[Success] Session successfully saved to {os.path.abspath(session_file)}")
            print("You can now close the browser window if it is still open.")
        else:
            print("\n[Timeout/Cancelled] Did not detect Gmail Inbox within 3 minutes, or the browser was closed.")

        try:
            browser.close()
        except Exception:
            pass

if __name__ == "__main__":
    login()
