import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Dumping Yoast status details...")
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
            
            # Click on the Yoast SEO tab if it's there
            try:
                page.locator('.yoast-assessment-tab__link').first.click()
                page.wait_for_timeout(1000)
            except:
                pass
                
            # Get text from the Yoast SEO assessment results header
            html_content = page.evaluate("""() => {
                // Return some interesting Yoast elements to inspect
                const results = [];
                const bullets = document.querySelectorAll('.yoast-issue-counter, .yoast-assessment-tab, .yoast-analysis-result');
                const list = [];
                bullets.forEach(b => {
                    list.push({
                        text: b.innerText,
                        className: b.className,
                        ariaLabel: b.getAttribute('aria-label')
                    });
                });
                return list;
            }""")
            
            for item in html_content:
                print(f"Text: {item['text']} | Class: {item['className']} | Label: {item['ariaLabel']}")
                
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
