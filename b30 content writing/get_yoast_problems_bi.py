import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Extracting Yoast problems from businessinsider101.com...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "businessinsider101.com/wp-admin" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find the open editor tab.")
                return
            
            # Scroll down and wait for Yoast calculations
            page.locator('#wpseo_meta').scroll_into_view_if_needed()
            page.wait_for_timeout(2000)
            
            results = page.evaluate("""() => {
                const list = [];
                // Look for both free/premium Yoast selectors
                const items = document.querySelectorAll('.yoast-analysis-result, .yoast-assessment-list li, .yoast-analysis-results__layout li');
                items.forEach(item => {
                    const text = item.innerText;
                    const badge = item.querySelector('.yoast-badge, .yoast-score-icon');
                    let color = 'unknown';
                    if (badge) {
                        const classList = Array.from(badge.classList).join(' ');
                        if (classList.includes('red') || classList.includes('bad')) color = 'red';
                        else if (classList.includes('orange') || classList.includes('ok')) color = 'orange';
                        else if (classList.includes('green') || classList.includes('good')) color = 'green';
                    }
                    list.push({ text, color });
                });
                return list;
            }""")
            
            print(f"Found {len(results)} items:")
            for r in results:
                print(f"[{r['color'].upper()}] {r['text'].strip()}")
                
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
