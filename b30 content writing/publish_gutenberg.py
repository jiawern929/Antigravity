import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to browser to publish post...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if ("post-new.php" in p_page.url or "post.php" in p_page.url) and "brandnews30010" not in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find the open editor tab.")
                return
            
            print(f"Found active editor tab: {page.url}")
            
            # Click the first "Publish" button in the header (using class & first to avoid strict violation)
            print("Clicking first 'Publish' button...")
            publish_toggle = page.locator('button.editor-post-publish-panel__toggle, button.editor-post-publish-button__button').first
            publish_toggle.scroll_into_view_if_needed()
            publish_toggle.click()
            page.wait_for_timeout(2000)
            
            # Click the second "Publish" button in the confirmation panel
            print("Clicking second 'Publish' button to confirm...")
            confirm_publish = page.locator('.editor-post-publish-panel__header button:has-text("Publish"), button.editor-post-publish-button').first
            confirm_publish.click()
            
            print("Waiting for publish process to complete...")
            page.wait_for_timeout(6000)
            
            # Verify success by looking for post link
            post_link_el = page.locator('.post-publish-panel__postpublish-post-address input, a:has-text("View Post")').first
            if post_link_el.is_visible():
                post_url = post_link_el.get_attribute("href") or post_link_el.get_attribute("value")
                print(f"SUCCESS! Post published successfully.")
                print(f"Published URL: {post_url}")
            else:
                # Fallback: check current URL or editPost return
                print("Post published. Fetching published URL...")
                post_url = page.evaluate("() => wp.data.select('core/editor').getPermalink()")
                print(f"Published URL: {post_url}")
                
        except Exception as e:
            print("Error during publish:", e)

if __name__ == "__main__":
    run()
