import os
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def publish_to_wp(site_url, username, password, title, content, status="draft"):
    # Ensure URL ends with a slash
    if not site_url.endswith('/'):
        site_url += '/'
        
    login_url = f"{site_url}wp-login.php"
    admin_url = f"{site_url}wp-admin/"
    
    user_data_dir = os.path.abspath('chrome_temp_profile')
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--headless")
    
    print(f"Launching Chrome for {site_url}...")
    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"Failed to launch Chrome: {e}")
        return False
    
    try:
        print(f"Navigating to login page: {login_url}")
        driver.get(login_url)
        time.sleep(3)
        
        # Check if already logged in (redirected to admin)
        if "wp-admin" in driver.current_url and "wp-login.php" not in driver.current_url:
            print("Already logged in!")
        else:
            # Type username
            print("Entering username...")
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "user_login"))
            )
            username_field.clear()
            username_field.send_keys(username)
            
            # Type password
            print("Entering password...")
            password_field = driver.find_element(By.ID, "user_pass")
            password_field.clear()
            password_field.send_keys(password)
            
            # Click login
            print("Submitting login form...")
            driver.find_element(By.ID, "wp-submit").click()
            time.sleep(5)
            
        # Verify login success
        current_url = driver.current_url
        print(f"Current URL after login: {current_url}")
        if "wp-admin" not in current_url:
            print("Login failed! Could not reach admin page.")
            return False
            
        print("Logged in successfully. Navigating to wp-admin main page to fetch nonce...")
        driver.get(admin_url)
        time.sleep(3)
        
        # Extract REST API nonce
        print("Extracting API Nonce...")
        nonce = None
        api_root = None
        try:
            nonce = driver.execute_script("return wpApiSettings.nonce;")
            api_root = driver.execute_script("return wpApiSettings.root;")
            print(f"Found Nonce from JS: {nonce}")
            print(f"API Root: {api_root}")
        except Exception as e:
            print(f"Failed to get nonce from wpApiSettings: {e}")
            
        if not nonce:
            print("Attempting fallback to find nonce in page HTML...")
            html = driver.page_source
            match = re.search(r'"nonce"\s*:\s*"([a-zA-Z0-9]+)"', html)
            if match:
                nonce = match.group(1)
                print(f"Found Nonce via regex: {nonce}")
                api_root = f"{site_url}wp-json/"
            else:
                # Try finding in localized scripts
                match_api = re.search(r'var wpApiSettings = ({.*?});', html)
                if match_api:
                    import json
                    try:
                        settings = json.loads(match_api.group(1))
                        nonce = settings.get("nonce")
                        api_root = settings.get("root")
                        print(f"Found Nonce from regex JSON: {nonce}")
                    except Exception:
                        pass

        if not nonce:
            print("Could not find nonce. Cannot proceed with REST API.")
            return False
            
        # Publish post using Javascript Fetch inside the browser context
        print("Publishing post via REST API fetch...")
        publish_js = f"""
        return fetch("{api_root}wp/v2/posts", {{
            method: "POST",
            headers: {{
                "Content-Type": "application/json",
                "X-WP-Nonce": "{nonce}"
            }},
            body: JSON.stringify({{
                title: {repr(title)},
                content: {repr(content)},
                status: "{status}"
            }})
        }}).then(res => {{
            if (!res.ok) {{
                return res.text().then(text => {{ throw new Error(text); }});
            }}
            return res.json();
        }});
        """
        
        result = driver.execute_async_script(f"""
            var callback = arguments[arguments.length - 1];
            {publish_js}
            .then(data => callback({{success: true, data: data}}))
            .catch(err => callback({{success: false, error: err.message}}));
        """)
        
        if result.get("success"):
            post_data = result.get("data")
            print(f"\n[SUCCESS] Post published successfully!")
            print(f"Post ID: {post_data.get('id')}")
            print(f"Post Link: {post_data.get('link')}")
            return post_data.get('link')
        else:
            print(f"\n[FAILED] REST API publishing failed: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    # Test publishing a draft post
    site = "https://dushitoutiao.com/brandnews30010/"
    user = "jwern929@gmail.com"
    pw = "PFHx1pBpwoD*7#lPthajn!YC"
    
    test_title = "Test Article from AI Assistant"
    test_content = "<p>This is a test article published automatically via Python and Chrome session.</p>"
    
    publish_to_wp(site, user, pw, test_title, test_content, status="draft")
