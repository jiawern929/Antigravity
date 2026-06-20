import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking overall readability tab score class...")
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
            
            score = page.evaluate("""() => {
                const icon = document.querySelector('#wpseo-readability-score-icon');
                if (icon) {
                    const svg = icon.querySelector('svg');
                    return {
                        html: icon.outerHTML,
                        svgClass: svg ? svg.className.baseVal || svg.className : 'no svg'
                    };
                }
                return 'not found';
            }""")
            print(score)
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
