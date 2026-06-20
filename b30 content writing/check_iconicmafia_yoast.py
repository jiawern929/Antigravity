import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking Yoast SEO score for iconicmafia...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "iconicmafia.com" in p_page.url:
                    page = p_page
                    break
            
            if not page:
                print("Could not find iconicmafia.com tab.")
                return
            
            print(f"Found page: {page.url}")
            
            js_script = """
            () => {
                const score = {};
                try {
                    const scoreContainer = document.querySelector('.wpseo-score-icon-container');
                    if (scoreContainer) {
                        score.scoreContainerHTML = scoreContainer.outerHTML;
                    }
                } catch(e) {
                    score.domError = e.message;
                }
                return score;
            }
            """
            
            res = page.evaluate(js_script)
            print("Yoast Store Details:")
            print(res)
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
