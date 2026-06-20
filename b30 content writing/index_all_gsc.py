import sys
import os
import time
from playwright.sync_api import sync_playwright

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# List of URLs and their domain properties
targets = [
    {
        "name": "dushitoutiao",
        "url": "https://dushitoutiao.com/klwaterfilter2026/",
        "domain": "sc-domain:dushitoutiao.com"
    },
    {
        "name": "businessinsider101",
        "url": "https://businessinsider101.com/klwaterfilter2026/",
        "domain": "sc-domain:businessinsider101.com"
    },
    {
        "name": "asiatop40",
        "url": "https://asiatop40.com/industry-insights/klwaterfilter2026/",
        "domain": "sc-domain:asiatop40.com"
    },
    {
        "name": "top50malaysia",
        "url": "https://top50malaysia.com/klwaterfilter2026/",
        "domain": "sc-domain:top50malaysia.com"
    },
    {
        "name": "iconicmafia",
        "url": "https://iconicmafia.com/klwaterfilter2026/",
        "domain": "sc-domain:iconicmafia.com"
    },
    {
        "name": "globalstraits",
        "url": "https://globalstraits.com/klwaterfilter2026/",
        "domain": "sc-domain:globalstraits.com"
    },
    {
        "name": "onasianews",
        "url": "https://onasianews.com/klwaterfilter2026/",
        "domain": "sc-domain:onasianews.com"
    }
]

BRAIN_DIR = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570"

def run():
    print("Connecting to Chrome CDP at port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            for idx, target in enumerate(targets, 1):
                name = target["name"]
                url = target["url"]
                domain = target["domain"]
                
                print("\n" + "="*50)
                print(f"[{idx}/7] Processing: {name} ({url})")
                print(f"GSC Domain Property: {domain}")
                print("="*50)
                
                page = context.new_page()
                dashboard_url = f"https://search.google.com/search-console?resource_id={domain}"
                print(f"Navigating to: {dashboard_url}")
                page.goto(dashboard_url, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(5000)
                
                # Check for welcome/sign-in page redirection
                if "welcome" in page.url or "signin" in page.url:
                    print("Error: Redirected to welcome or sign-in page. Please make sure GSC is logged in.")
                    page.close()
                    continue
                
                # Look for the inspect search input
                input_selector = "input.Ax4B8"
                search_input = page.locator(input_selector).first
                
                if not search_input.is_visible():
                    print("Search input 'input.Ax4B8' not immediately visible. Waiting up to 10s...")
                    try:
                        search_input.wait_for(state="visible", timeout=10000)
                    except Exception:
                        pass
                
                if not search_input.is_visible():
                    # Fallback selectors
                    for alt_sel in ["input[aria-label*='Inspect']", "input[aria-label*='检查']", "input[placeholder*='Inspect']"]:
                        try:
                            el = page.locator(alt_sel).first
                            if el.is_visible():
                                search_input = el
                                print(f"Found search input using fallback selector: {alt_sel}")
                                break
                        except Exception:
                            pass
                
                if not search_input.is_visible():
                    print("Error: Could not find search input. Taking diagnostic screenshot.")
                    diag_path = os.path.join(BRAIN_DIR, f"err_search_input_{name}.png")
                    page.screenshot(path=diag_path)
                    page.close()
                    continue
                
                print(f"Typing URL '{url}' into search input...")
                search_input.click()
                search_input.fill(url)
                search_input.press("Enter")
                
                # Wait for URL inspection page to load
                print("Waiting for URL inspection results to load...")
                
                # Let's poll for the REQUEST INDEXING button or equivalent
                btn_selectors = [
                    'text="REQUEST INDEXING"',
                    'text="Request Indexing"',
                    'text="请求编入索引"',
                    'div[role="button"]:has-text("REQUEST INDEXING")',
                    'div[role="button"]:has-text("请求编入索引")',
                    'span:has-text("REQUEST INDEXING")',
                    'span:has-text("请求编入索引")'
                ]
                
                request_btn = None
                start_time = time.time()
                while time.time() - start_time < 60:
                    page.wait_for_timeout(3000)
                    # Check if button is visible
                    for sel in btn_selectors:
                        try:
                            el = page.locator(sel).first
                            if el.is_visible():
                                request_btn = el
                                print(f"Found indexing button using selector: {sel}")
                                break
                        except Exception:
                            pass
                    if request_btn:
                        break
                
                if not request_btn:
                    print("Error: URL inspection page or REQUEST INDEXING button did not load in time.")
                    diag_path = os.path.join(BRAIN_DIR, f"err_inspect_load_{name}.png")
                    page.screenshot(path=diag_path)
                    page.close()
                    continue
                
                print("Clicking 'REQUEST INDEXING'...")
                request_btn.click()
                
                # Monitor submission dialog
                print("Waiting for indexing request to complete (up to 3 minutes)...")
                submitted = False
                dialog_start = time.time()
                
                # We check every 5 seconds for success indicators
                # Indicators: "Indexing requested", "已请求编入索引", "Dismiss", "知道了"
                dismiss_selectors = [
                    'text="Dismiss"',
                    'text="知道了"',
                    'span:has-text("Dismiss")',
                    'span:has-text("知道了")',
                    'div[role="button"]:has-text("Dismiss")',
                    'div[role="button"]:has-text("知道了")'
                ]
                
                dismiss_btn = None
                while time.time() - dialog_start < 180:
                    page.wait_for_timeout(5000)
                    
                    # Check if success message is visible or if dismiss button is available
                    page_text = page.evaluate("() => document.body.innerText")
                    if "Indexing requested" in page_text or "已请求编入索引" in page_text:
                        print("Detected success message in page text!")
                        submitted = True
                    
                    for sel in dismiss_selectors:
                        try:
                            el = page.locator(sel).first
                            if el.is_visible():
                                dismiss_btn = el
                                print(f"Found Dismiss/Got it button using selector: {sel}")
                                break
                        except Exception:
                            pass
                    
                    if dismiss_btn:
                        submitted = True
                        break
                
                if submitted:
                    print("Indexing requested successfully!")
                    # Take success screenshot
                    success_path = os.path.join(BRAIN_DIR, f"gsc_index_{name}.png")
                    page.screenshot(path=success_path)
                    print(f"Saved success screenshot to: {success_path}")
                    
                    # Click dismiss if found to clean up
                    if dismiss_btn:
                        try:
                            dismiss_btn.click()
                            page.wait_for_timeout(2000)
                        except Exception as e:
                            print("Note: Failed to click dismiss button:", e)
                else:
                    print("Warning: Indexing submission timed out or did not show completion confirmation.")
                    # Take warning screenshot anyway
                    warn_path = os.path.join(BRAIN_DIR, f"gsc_index_warn_{name}.png")
                    page.screenshot(path=warn_path)
                    print(f"Saved diagnostic/warning screenshot to: {warn_path}")
                
                print(f"Closing page for {name}...")
                page.close()
                time.sleep(2)
                
            print("\nAll tasks completed!")
            browser.close()
            
        except Exception as e:
            print("General error during execution:", e)

if __name__ == "__main__":
    run()
