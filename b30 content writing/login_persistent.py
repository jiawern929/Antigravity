import os
import sys
from playwright.sync_api import sync_playwright

def run():
    user_data_dir = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
    profile_name = "Profile 3"  # Jwern929
    
    print(f"Launching Google Chrome with profile: {profile_name}...")
    print("Please make sure all Google Chrome windows are closed before running this!")
    
    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                channel="chrome",
                headless=False,
                args=[f"--profile-directory={profile_name}", "--start-maximized"],
                viewport=None
            )
        except Exception as e:
            print("\n" + "!"*70)
            print("ERROR: Failed to launch Google Chrome.")
            print("This is almost always because Google Chrome is still running.")
            print("Please close all Chrome windows (or end Chrome in Task Manager) and run again.")
            print("!"*70 + "\n")
            print(f"Details: {e}")
            return
            
        page = context.new_page() if not context.pages else context.pages[0]
        
        print("Navigating to Gmail...")
        page.goto("https://mail.google.com")
        
        print("\n" + "="*70)
        print("ACTION REQUIRED ON YOUR SCREEN:")
        print("1. A new Google Chrome window has opened using your 'Jwern929' profile.")
        print("2. If you are already logged in to Gmail, it will open directly.")
        print("3. If not, please log in in that browser window.")
        print("4. When you are done, simply CLOSE the browser window.")
        print("="*70 + "\n")
        
        import time
        # Loop until page is closed by the user
        while True:
            try:
                if page.is_closed():
                    print("Browser page closed by user.")
                    break
            except Exception:
                break
            time.sleep(1)
            
        context.close()
        print("Browser context closed successfully.")

if __name__ == "__main__":
    run()
