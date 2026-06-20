import os
import sys
import time
import undetected_chromedriver as uc

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def debug():
    dest_user_data = os.path.abspath('chrome_temp_profile')
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={dest_user_data}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--headless")
    
    print("Launching Chrome...")
    driver = uc.Chrome(options=options)
    try:
        url = "https://dushitoutiao.com/brandnews30010/?loggedout=true&wp_lang=en_US"
        print(f"Navigating to: {url}")
        driver.get(url)
        print("Waiting 5 seconds for page load...")
        time.sleep(5)
        
        print(f"Final URL: {driver.current_url}")
        print(f"Page Title: {driver.title}")
        
        print("\nForm inputs found on the page:")
        inputs = driver.find_elements(by="tag name", value="input")
        for idx, inp in enumerate(inputs):
            print(f"[{idx}] ID: '{inp.get_attribute('id')}', Name: '{inp.get_attribute('name')}', Type: '{inp.get_attribute('type')}', Class: '{inp.get_attribute('class')}'")
            
        print("\nPage text preview:")
        try:
            body_text = driver.find_element(by="tag name", value="body").text
            print(body_text[:500])
        except Exception:
            pass
            
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    debug()
