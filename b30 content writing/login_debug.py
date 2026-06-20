import os
import subprocess
import time
from playwright.sync_api import sync_playwright

def find_chrome():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%USERPROFILE%\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return "chrome.exe" # Fallback to path

def run():
    chrome_path = find_chrome()
    print(f"Using Chrome path: {chrome_path}")
    print("Launching Google Chrome with remote debugging on port 9222...")
    print("Please make sure all Google Chrome windows are closed first!")
    
    # Start Chrome with remote debugging
    try:
        # Start Chrome using Popen so it runs asynchronously without blocking Python
        # Use shell=True if path contains spaces or arguments are complex on Windows
        cmd = f'"{chrome_path}" --remote-debugging-port=9222 --profile-directory="Profile 3"'
        print(f"Running command: {cmd}")
        subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        print("Chrome launch command sent. Waiting 5 seconds for it to initialize...")
        time.sleep(5)
    except Exception as e:
        print(f"Failed to launch Chrome automatically: {e}")
        return
        
    with sync_playwright() as p:
        try:
            print("Connecting Playwright to http://127.0.0.1:9222...")
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print("Connected successfully!")
            
            context = browser.contexts[0]
            
            # Let's find if Gmail is already open, otherwise open it
            page = None
            for p_in_ctx in context.pages:
                if "mail.google.com" in p_in_ctx.url:
                    page = p_in_ctx
                    print("Found existing Gmail tab, switching to it...")
                    page.bring_to_front()
                    break
                    
            if not page:
                print("Opening Gmail in a new tab...")
                page = context.new_page()
                page.goto("https://mail.google.com")
                
            print("\n" + "="*70)
            print("STATUS:")
            print(f"Active URL: {page.url}")
            print(f"Active Page Title: {page.title()}")
            print("Playwright is now successfully connected to your real Chrome session!")
            print("="*70 + "\n")
            
            # Wait for 15 seconds to let the session run
            time.sleep(15)
            
        except Exception as e:
            print(f"\nConnection failed: {e}")
            print("Please make sure Chrome was completely closed before starting the script,")
            print("so it could start with the debugging port enabled.")

if __name__ == "__main__":
    run()
