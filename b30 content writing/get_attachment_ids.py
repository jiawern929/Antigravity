import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking uploaded media library IDs...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "top50malaysia.com" in p_page.url:
                    page = p_page
                    break
            
            if not page:
                print("Could not find top50malaysia.com tab.")
                return
            
            # Fetch media items from WP API
            media_items = page.evaluate("""async () => {
                const apiRoot = wpApiSettings.root;
                const nonce = wpApiSettings.nonce;
                const res = await fetch(apiRoot + "wp/v2/media?search=filken&per_page=20", {
                    headers: { "X-WP-Nonce": nonce }
                });
                return await res.json();
            }""")
            
            print("Media Items found:")
            for item in media_items:
                print(f"ID: {item['id']} | Filename: {item['media_details'].get('sizes', {}).get('full', {}).get('file', '')} | URL: {item['source_url']}")
                
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
