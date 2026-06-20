import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to browser to verify/set slug...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Find the active editor tab
            page = None
            for p_page in context.pages:
                if ("post-new.php" in p_page.url or "post.php" in p_page.url) and "brandnews30010" not in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find the open editor tab.")
                return
            
            # Get current slug
            current_slug = page.evaluate("() => wp.data.select('core/editor').getEditedPostAttribute('slug')")
            print(f"Current Slug: {current_slug}")
            
            target_slug = "klwaterfilter2026"
            if current_slug != target_slug:
                print(f"Setting slug to: {target_slug}")
                page.evaluate("([slug]) => { wp.data.dispatch('core/editor').editPost({ slug: slug }); }", [target_slug])
                page.wait_for_timeout(1000)
                new_slug = page.evaluate("() => wp.data.select('core/editor').getEditedPostAttribute('slug')")
                print(f"Verified Slug: {new_slug}")
            else:
                print("Slug is already correct.")
                
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
