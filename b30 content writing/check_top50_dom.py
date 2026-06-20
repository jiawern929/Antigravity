import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking Yoast DOM input values...")
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
            
            print(f"Found page: {page.url}")
            
            dom_values = page.evaluate("""() => {
                const getVal = (selector) => {
                    const el = document.querySelector(selector);
                    return el ? el.value || el.innerText : null;
                };
                
                return {
                    focus_kw: getVal('#focus-keyword-input-metabox'),
                    seo_title: getVal('#yoast-google-preview-title-metabox'),
                    seo_desc: getVal('#yoast-google-preview-description-metabox')
                };
            }""")
            
            print("DOM Input Values:")
            print(f"Focus Keyword: {dom_values['focus_kw']}")
            print(f"SEO Title: {dom_values['seo_title']}")
            print(f"Meta Description: {dom_values['seo_desc']}")
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
