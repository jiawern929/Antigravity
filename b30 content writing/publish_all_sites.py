import os
import sys
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure UTF-8 encoding for Windows console compatibility
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# List of all WordPress sites and credentials provided by the user
SITES = [
    {
        "name": "dushitoutiao",
        "url": "https://dushitoutiao.com/brandnews30010/?loggedout=true&wp_lang=en_US",
        "user": "jwern929@gmail.com",
        "pass": "PFHx1pBpwoD*7#lPthajn!YC"
    },
    {
        "name": "huawennews",
        "url": "https://huawennews.com/brandnews3007/?loggedout=true&wp_lang=en_US",
        "user": "jwern929@gmail.com",
        "pass": "PFHx1pBpwoD*7#lPthajn!YC"
    },
    {
        "name": "onasianews",
        "url": "https://onasianews.com/edd133/",
        "user": "Ashley",
        "pass": "($eiCp&6bNawGqCc*I6hw&*5"
    },
    {
        "name": "straitshub",
        "url": "http://straitshub.com/edd130/",
        "user": "Louis",
        "pass": "JMB87qTwe9ISJTNl6pA(A@kM"
    },
    {
        "name": "businessinsider101",
        "url": "https://businessinsider101.com/wp-admin/",
        "user": "jwern929@gmail.com",
        "pass": "PFHx1pBpwoD*7#lPthajn!YC"
    },
    {
        "name": "asiatop40",
        "url": "https://asiatop40.com/wp-admin/",
        "user": "jwern929@gmail.com",
        "pass": "PFHx1pBpwoD*7#lPthajn!YC"
    },
    {
        "name": "billionairechamp",
        "url": "https://billionairechamp.com/wp-admin/",
        "user": "editor2",
        "pass": "!r8ylrwOF$*&TrGtykk9o7xe"
    },
    {
        "name": "top50malaysia",
        "url": "https://top50malaysia.com/wp-admin/",
        "user": "Carmen",
        "pass": "PFHx1pBpwoD*7#lPthajn!YC"
    },
    {
        "name": "globalstraits",
        "url": "https://globalstraits.com/edd132/",
        "user": "Ashley",
        "pass": "($eiCp&6bNawGqCc*I6hw&*5"
    }
]

def publish_post(site, title, content, status="draft"):
    name = site["name"]
    login_url = site["url"]
    username = site["user"]
    password = site["pass"]
    
    print(f"\n" + "="*50)
    print(f"STARTING PUBLISH FOR SITE: {name}")
    print(f"URL: {login_url}")
    print(f"User: {username}")
    print("="*50)
    
    user_data_dir = os.path.abspath('chrome_temp_profile')
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={name}")  # Unique profile directory for each site
    # Headless mode is disabled so you can see the browser operations in real-time on your screen.
    
    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"Failed to launch Chrome for {name}: {e}")
        return {"site": name, "success": False, "error": f"Chrome launch error: {e}"}
        
    try:
        print("Navigating to URL...")
        driver.get(login_url)
        time.sleep(5)
        
        # Check if login fields exist
        try:
            username_field = driver.find_element(By.ID, "user_login")
            print("Found login form. Typing credentials...")
            username_field.clear()
            username_field.send_keys(username)
            
            password_field = driver.find_element(By.ID, "user_pass")
            password_field.clear()
            password_field.send_keys(password)
            
            driver.find_element(By.ID, "wp-submit").click()
            print("Login submitted. Waiting for dashboard redirect...")
            time.sleep(8)
        except Exception:
            print("Login form not found. Checking if already logged in...")
            
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
        if "wp-admin" not in current_url:
            # If login page did not redirect automatically, go to wp-admin/
            base_url = login_url.split('?')[0]
            if not base_url.endswith('/'):
                base_url += '/'
            if "wp-admin" not in base_url:
                admin_url = f"{base_url}wp-admin/"
            else:
                admin_url = base_url
                
            print(f"Navigating to admin dashboard: {admin_url}")
            driver.get(admin_url)
            time.sleep(5)
            current_url = driver.current_url
            
        if "wp-admin" not in current_url:
            print("Login verification failed. Not in WordPress admin.")
            return {"site": name, "success": False, "error": "Login failed"}
            
        print("Login verified. Fetching REST API configurations...")
        nonce = None
        api_root = None
        
        try:
            nonce = driver.execute_script("return wpApiSettings.nonce;")
            api_root = driver.execute_script("return wpApiSettings.root;")
        except Exception:
            pass
            
        if not nonce:
            print("Searching HTML source for API nonce...")
            html = driver.page_source
            match = re.search(r'"nonce"\s*:\s*"([a-zA-Z0-9]+)"', html)
            if match:
                nonce = match.group(1)
                base_admin = current_url.split('wp-admin')[0]
                api_root = f"{base_admin}wp-json/"
                
        if not nonce:
            print("Could not retrieve WordPress API nonce. Cannot publish via REST API.")
            return {"site": name, "success": False, "error": "Could not find REST API nonce"}
            
        print(f"API Nonce: {nonce}")
        print(f"API Root: {api_root}")
        
        print("Publishing post via REST API inside Chrome context...")
        js_code = f"""
        var callback = arguments[arguments.length - 1];
        fetch("{api_root}wp/v2/posts", {{
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
        }})
        .then(res => {{
            if (!res.ok) {{
                return res.text().then(text => {{ throw new Error(text); }});
            }}
            return res.json();
        }})
        .then(data => callback({{success: true, data: data}}))
        .catch(err => callback({{success: false, error: err.message}}));
        """
        
        result = driver.execute_async_script(js_code)
        
        if result.get("success"):
            post_data = result.get("data")
            post_link = post_data.get("link")
            post_id = post_data.get("id")
            print(f"SUCCESS! Post created on {name}. ID: {post_id}, Link: {post_link}")
            return {"site": name, "success": True, "link": post_link, "id": post_id}
        else:
            err_msg = result.get("error")
            print(f"FAILED to publish on {name}: {err_msg}")
            return {"site": name, "success": False, "error": err_msg}
            
    except Exception as e:
        print(f"Error occurred during execution for {name}: {e}")
        return {"site": name, "success": False, "error": str(e)}
    finally:
        driver.quit()

def main():
    import json
    
    config_file = "article.json"
    template = {
        "title": "Your Article Title Here",
        "content": "<p>Your HTML content here. You can use standard HTML tags like &lt;p&gt;, &lt;h2&gt;, &lt;img&gt; etc.</p>",
        "status": "draft",
        "sites": ["dushitoutiao"]  # List of site names, or "all" to publish to all 9 sites
    }
    
    if not os.path.exists(config_file):
        # Create a template file if it doesn't exist
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=4, ensure_ascii=False)
        print(f"\n[Template Created] Created a template file: {config_file}")
        print("Please edit 'article.json' with your article's title, content, and target sites, then run this script again.")
        print(f"Available site names: {[s['name'] for s in SITES]}")
        return
        
    # Read the article config
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {config_file}: {e}")
        return
        
    title = data.get("title", "").strip()
    content = data.get("content", "").strip()
    status = data.get("status", "draft").strip()
    target_sites = data.get("sites", [])
    
    if not title or not content:
        print("Error: 'title' or 'content' in article.json cannot be empty.")
        return
        
    # Filter sites to run
    sites_to_run = []
    if isinstance(target_sites, str) and target_sites.lower() == "all":
        sites_to_run = SITES
    elif isinstance(target_sites, list):
        for name in target_sites:
            found = False
            for s in SITES:
                if s["name"] == name:
                    sites_to_run.append(s)
                    found = True
                    break
            if not found:
                print(f"Warning: Site name '{name}' not found in SITES list. Skipping.")
                
    if not sites_to_run:
        print("Error: No valid target sites specified. Please check 'sites' in article.json.")
        print(f"Available site names: {[s['name'] for s in SITES]} or 'all'")
        return
        
    print(f"\nFound {len(sites_to_run)} site(s) to publish to. Starting execution...")
    results = []
    
    for s in sites_to_run:
        res = publish_post(s, title, content, status=status)
        results.append(res)
        
    # Print beautiful summary report
    print("\n" + "="*70)
    print("PUBLISHING REPORT SUMMARY")
    print("="*70)
    success_count = 0
    for r in results:
        if r["success"]:
            print(f"[*] {r['site']}: SUCCESS! Link: {r['link']} (ID: {r['id']})")
            success_count += 1
        else:
            print(f"[x] {r['site']}: FAILED! Error: {r['error']}")
    print("="*70)
    print(f"Total Successful: {success_count} / {len(sites_to_run)}")
    print("="*70 + "\n")
    
    # Save report to a text file
    report_file = "last_publish_report.txt"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write(f"PUBLISHING REPORT - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Title: {title}\n")
            f.write(f"Status: {status}\n")
            f.write("="*70 + "\n")
            for r in results:
                if r["success"]:
                    f.write(f"[SUCCESS] {r['site']} -> {r['link']} (ID: {r['id']})\n")
                else:
                    f.write(f"[FAILED] {r['site']} -> {r['error']}\n")
            f.write("="*70 + "\n")
        print(f"Detailed report saved to: {os.path.abspath(report_file)}")
    except Exception as e:
        print(f"Could not save report file: {e}")

if __name__ == "__main__":
    main()
