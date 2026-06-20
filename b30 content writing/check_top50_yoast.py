import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to browser via CDP...")
    with sync_playwright() as p:
        try:
            # Add a timeout to connection
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222", timeout=15000)
            context = browser.contexts[0]
            print("Connected. Finding top50malaysia.com tab...")
            
            page = None
            for p_page in context.pages:
                if "top50malaysia.com" in p_page.url:
                    page = p_page
                    break
            
            if not page:
                print("Could not find top50malaysia.com tab.")
                return
            
            print(f"Found page: {page.url}")
            page.bring_to_front()
            
            # Check if Yoast metabox is in the page at all
            yoast_exists = page.evaluate("""() => {
                const metabox = document.querySelector('#wpseo_meta');
                const sidebar = document.querySelector('.yoast-sidebar');
                return {
                    metaboxExists: !!metabox,
                    sidebarExists: !!sidebar,
                    metaboxVisible: metabox ? metabox.offsetParent !== null : false
                };
            }""")
            print("Yoast elements in DOM:", yoast_exists)
            
            # Let's inspect the current post state from wp.data
            wp_data = page.evaluate("""() => {
                if (!window.wp || !window.wp.data) return { error: "wp or wp.data not loaded" };
                const editedPost = wp.data.select('core/editor').getEditedPostAttribute('meta') || {};
                const slug = wp.data.select('core/editor').getEditedPostAttribute('slug');
                return {
                    slug,
                    meta: editedPost
                };
            }""")
            print("WordPress Edited Post Meta:")
            print(wp_data)
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
