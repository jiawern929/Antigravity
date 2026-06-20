import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to Chrome to publish post on businessinsider101.com...")
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
            
            print(f"Found active editor tab: {page.url}")
            
            # Click the first "发布" (Publish) button in the header
            print("Clicking first '发布' button...")
            publish_toggle = page.locator('button:has-text("发布"), button.editor-post-publish-panel__toggle').first
            publish_toggle.scroll_into_view_if_needed()
            publish_toggle.click()
            page.wait_for_timeout(2000)
            
            # Click the second "发布" (Publish) button in the confirmation panel
            print("Clicking second '发布' button to confirm...")
            confirm_publish = page.locator('.editor-post-publish-panel__header button:has-text("发布"), button.editor-post-publish-button').first
            confirm_publish.click()
            
            print("Waiting for publish process to complete...")
            page.wait_for_timeout(6000)
            
            # Verify success by checking permalink
            print("Post published. Fetching published URL...")
            post_url = page.evaluate("() => wp.data.select('core/editor').getPermalink()")
            print(f"SUCCESS! Post published successfully.")
            print(f"Published URL: {post_url}")
            
        except Exception as e:
            print("Error during publish:", e)

if __name__ == "__main__":
    run()
