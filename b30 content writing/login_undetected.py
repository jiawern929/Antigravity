import os
import shutil
import time
import undetected_chromedriver as uc

def copy_profile():
    src_user_data = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
    src_profile = os.path.join(src_user_data, 'Profile 3')
    
    dest_user_data = os.path.abspath('chrome_temp_profile')
    dest_profile = os.path.join(dest_user_data, 'Default')
    
    print(f"Copying Chrome Profile 3 from {src_profile} to {dest_profile}...")
    
    # Only clean up dest if it exists
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
    # Copy profile first to ensure fresh state
    copy_profile()
    
    dest_user_data = os.path.abspath('chrome_temp_profile')
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={dest_user_data}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--start-maximized")
    
    print("Launching undetected Google Chrome...")
    try:
        # undetected-chromedriver handles chrome version auto-detection and downloads driver
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"\nFailed to launch Chrome: {e}")
        print("Please verify that Google Chrome is installed in the default location.")
        return
        
    print("Navigating to Gmail...")
    driver.get("https://mail.google.com")
    
    print("\n" + "="*70)
    print("ACTION REQUIRED:")
    print("1. An undetected Google Chrome window has opened.")
    print("2. Google's secure browser protection is bypassed!")
    print("3. Enter your email and password if requested, and complete verification.")
    print("4. Once you are successfully in Gmail Inbox, CLOSE the browser window.")
    print("="*70 + "\n")
    
    # Loop and check if window is closed
    while True:
        try:
            handles = driver.window_handles
            if not handles:
                print("Browser window was closed by the user.")
                break
        except Exception:
            print("Browser connection closed.")
            break
        time.sleep(1)
        
    driver.quit()
    print("Process finished successfully.")

if __name__ == "__main__":
    run()
