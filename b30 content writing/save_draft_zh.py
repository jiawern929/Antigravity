import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to Chrome to click '保存草稿'...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "businessinsider101.com/wp-admin" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find the open editor tab.")
                return
            
            # Click Save Draft in Chinese
            print("Locating '保存草稿' button...")
            save_button = page.locator('button:has-text("保存草稿"), button.editor-post-save-draft')
            if save_button.is_visible():
                save_button.click()
                print("Clicked '保存草稿'. Waiting for save completion...")
                page.wait_for_timeout(5000)
                print("Draft saved.")
            else:
                print("Button '保存草稿' not visible.")
                
        except Exception as e:
            print("Error saving draft:", e)

if __name__ == "__main__":
    run()
