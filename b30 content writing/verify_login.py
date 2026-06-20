import os
import time
import undetected_chromedriver as uc

def verify():
    dest_user_data = os.path.abspath('chrome_temp_profile')
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={dest_user_data}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--headless")  # Run headlessly for verification
    
    print("Launching verification browser in headless mode...")
    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"Failed to launch verification Chrome: {e}")
        return
        
    try:
        print("Navigating to Gmail...")
        driver.get("https://mail.google.com")
        print("Waiting 10 seconds for redirects and content to load...")
        time.sleep(10)  # Give enough time for redirects
        
        url = driver.current_url
        title = driver.title
        
        print("\n" + "="*70)
        print("VERIFICATION RESULTS:")
        print(f"Final URL: {url}")
        print(f"Page Title: {title}")
        print("="*70 + "\n")
        
        # Check if we successfully bypassed login page and hit Gmail app
        if "mail.google.com/mail" in url or "Inbox" in title or "收件箱" in title or "Gmail" in title:
            print("SUCCESS: Gmail session is active and authenticated!")
            # We can print some text content to show it works
            try:
                body_text = driver.find_element(by="tag name", value="body").text
                print(f"Page Body Preview (first 150 chars): {body_text[:150].strip()}")
            except Exception:
                pass
        else:
            print("FAILED: Session not active, redirected to sign-in page.")
            
    except Exception as e:
        print(f"Verification failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify()
