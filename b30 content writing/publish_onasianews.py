import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to Chrome for onasianews.com publishing...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "onasianews.com" in p_page.url:
                    page = p_page
                    break
            
            if not page:
                print("Could not find onasianews.com tab.")
                return
            
            print(f"Found active editor tab: {page.url}")
            page.bring_to_front()
            
            # Click Publish Toggle
            print("Clicking Publish button toggle...")
            publish_toggle = page.locator('button:has-text("Publish"), button:has-text("发布"), button.editor-post-publish-panel__toggle').first
            publish_toggle.scroll_into_view_if_needed()
            publish_toggle.click()
            page.wait_for_timeout(2000)
            
            # Click Confirm Publish
            print("Clicking Confirm Publish button...")
            confirm_publish = page.locator('.editor-post-publish-panel__header button:has-text("Publish"), .editor-post-publish-panel__header button:has-text("发布"), button.editor-post-publish-button').first
            confirm_publish.click()
            
            print("Waiting for post publication...")
            page.wait_for_timeout(8000)
            
            # Extract published permalink
            post_url = page.evaluate("() => wp.data.select('core/editor').getPermalink()")
            print(f"SUCCESS! Post published successfully.")
            print(f"Published URL: {post_url}")
            
        except Exception as e:
            print("Error during execution:", e)

if __name__ == "__main__":
    run()
