import os
import shutil
import time
from playwright.sync_api import sync_playwright

def copy_profile():
    src_user_data = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
    src_profile = os.path.join(src_user_data, 'Profile 3')
    
    dest_user_data = os.path.abspath('chrome_temp_profile')
    dest_profile = os.path.join(dest_user_data, 'Default')
    
    print(f"Copying Chrome Profile 3 from {src_profile} to {dest_profile}...")
    
    # Clean up destination
    if os.path.exists(dest_user_data):
        try:
            shutil.rmtree(dest_user_data)
        except Exception as e:
            print(f"Warning: could not clean up temp profile: {e}")
            
    os.makedirs(dest_profile, exist_ok=True)
    
    # 1. Copy Local State (crucial for cookie decryption)
    local_state_src = os.path.join(src_user_data, 'Local State')
    if os.path.exists(local_state_src):
        try:
            shutil.copy2(local_state_src, os.path.join(dest_user_data, 'Local State'))
        except Exception as e:
            print(f"Warning: failed to copy Local State: {e}")
        
    # 2. Copy essential profile files
    essential_items = [
        'Preferences',
        'Secure Preferences',
        'Web Data',
        'Login Data',
        'Network', # Contains Cookies database
    ]
    
    for item in essential_items:
        src_path = os.path.join(src_profile, item)
        dest_path = os.path.join(dest_profile, item)
        
        if os.path.exists(src_path):
            try:
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path)
                else:
                    shutil.copy2(src_path, dest_path)
            except Exception as e:
                print(f"Warning: failed to copy {item}: {e}")
                
    print("Profile copy completed.")

def run():
    copy_profile()
    
    dest_user_data = os.path.abspath('chrome_temp_profile')
    print("Launching Playwright with the temporary Chrome profile...")
    
    with sync_playwright() as p:
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=dest_user_data,
                channel="chrome",
                headless=False,
                args=["--start-maximized"],
                viewport=None
            )
        except Exception as e:
            print(f"Failed to launch Chrome: {e}")
            return
            
        page = context.new_page() if not context.pages else context.pages[0]
        
        print("Navigating to Gmail...")
        page.goto("https://mail.google.com")
        
        print("\n" + "="*70)
        print("ACTION REQUIRED ON YOUR SCREEN:")
        print("1. A new Google Chrome window has opened.")
        print("2. It should have all your settings, and hopefully you are already logged in to Gmail.")
        print("3. If you need to log in, do it now.")
        print("4. When you are done, simply CLOSE the browser window.")
        print("="*70 + "\n")
        
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
