import os
import sys
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Configure UTF-8 encoding for Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Site info (Site #3: onasianews)
site = {
    "name": "onasianews",
    "url": "https://onasianews.com/edd133/",
    "user": "Ashley",
    "pass": "($eiCp&6bNawGqCc*I6hw&*5"
}

slug = "kl-water-filter-recommendations-2026"

def run():
    user_data_dir = os.path.abspath('chrome_temp_profile_onasianews')
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory=onasianews")
    options.add_argument("--headless")  # Run headlessly for quick update
    
    print("Launching Chrome to update post status to draft...")
    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"Failed to launch Chrome: {e}")
        return
        
    try:
        print("Navigating to login page...")
        driver.get(site["url"])
        time.sleep(5)
        
        # Check if login is needed
        try:
            username_field = driver.find_element(By.ID, "user_login")
            print("Logging in...")
            username_field.clear()
            username_field.send_keys(site["user"])
            password_field = driver.find_element(By.ID, "user_pass")
            password_field.clear()
            password_field.send_keys(site["pass"])
            driver.find_element(By.ID, "wp-submit").click()
            time.sleep(8)
        except Exception:
            print("Already logged in or login form not found.")
            
        current_url = driver.current_url
        if "wp-admin" not in current_url:
            admin_url = "https://onasianews.com/edd133/wp-admin/"
            print(f"Navigating to admin dashboard: {admin_url}")
            driver.get(admin_url)
            time.sleep(5)
            current_url = driver.current_url
            
        if "wp-admin" not in current_url:
            print(f"Failed to reach dashboard. Current URL: {current_url}")
            return
            
        # Get nonce
        print("Retrieving API configurations...")
        nonce = driver.execute_script("return wpApiSettings.nonce;")
        api_root = driver.execute_script("return wpApiSettings.root;")
        
        # Script to find post ID by slug and update status to draft
        js_code = f"""
        var callback = arguments[arguments.length - 1];
        
        // 1. Fetch the post by slug to get ID
        fetch("{api_root}wp/v2/posts?slug={slug}&status=any", {{
            headers: {{
                "X-WP-Nonce": "{nonce}"
            }}
        }})
        .then(res => res.json())
        .then(posts => {{
            if (posts.length === 0) {{
                throw new Error("Post with slug '{slug}' not found.");
            }}
            var post = posts[0];
            var postId = post.id;
            
            // 2. Update status of this post to draft
            return fetch("{api_root}wp/v2/posts/" + postId, {{
                method: "POST",
                headers: {{
                    "Content-Type": "application/json",
                    "X-WP-Nonce": "{nonce}"
                }},
                body: JSON.stringify({{
                    status: "draft"
                }})
            }});
        }})
        .then(res => res.json())
        .then(data => callback({{success: true, data: data}}))
        .catch(err => callback({{success: false, error: err.message}}));
        """
        
        print("Sending update request to WordPress REST API...")
        result = driver.execute_async_script(js_code)
        
        if result.get("success"):
            print("\n[SUCCESS] Post status changed back to DRAFT!")
            print(f"Post ID: {result['data'].get('id')}")
            print(f"New Status: {result['data'].get('status')}")
            print(f"Edit Link: {current_url}post.php?post={result['data'].get('id')}&action=edit")
        else:
            print(f"\n[FAILED] Failed to update post: {result.get('error')}")
            
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    run()
