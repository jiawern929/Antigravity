import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to browser to inspect iconicmafia.com dashboard...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "iconicmafia.com" in p_page.url and "post-new.php" not in p_page.url:
                    page = p_page
                    break
            
            if not page:
                print("Could not find iconicmafia.com dashboard tab.")
                return
            
            print(f"Found page: {page.url}")
            page.bring_to_front()
            
            # Let's inspect wpApiSettings and some other globals
            wp_globals = page.evaluate("""() => {
                const settings = window.wpApiSettings || {};
                const ajaxurl = window.ajaxurl || null;
                const pagenow = window.pagenow || null;
                const typenow = window.typenow || null;
                
                return {
                    settings,
                    ajaxurl,
                    pagenow,
                    typenow,
                    url: window.location.href,
                    title: document.title
                };
            }""")
            
            print("WordPress Globals:")
            print(wp_globals)
            
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
