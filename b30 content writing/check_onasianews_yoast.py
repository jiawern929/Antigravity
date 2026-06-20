import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking Yoast SEO and Readability scores on onasianews...")
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
            
            print(f"Found page: {page.url}")
            
            js_script = """
            () => {
                const results = {};
                try {
                    const seoIcon = document.querySelector('#wpseo-seo-score-icon');
                    if (seoIcon) {
                        results.seo = seoIcon.outerHTML;
                    }
                    const readIcon = document.querySelector('#wpseo-readability-score-icon');
                    if (readIcon) {
                        results.readability = readIcon.outerHTML;
                    }
                } catch(e) {
                    results.error = e.message;
                }
                return results;
            }
            """
            
            res = page.evaluate(js_script)
            print("Yoast Scores:")
            print(res)
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
