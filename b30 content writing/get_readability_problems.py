import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to browser to get Yoast Readability analysis...")
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
            page.bring_to_front()
            
            # Click the Readability tab in Yoast SEO metabox if visible
            # In Yoast UI, the tabs are buttons or links
            page.evaluate("""() => {
                const tabs = document.querySelectorAll('.yoast-assessment-tabs button, .yoast-assessment-tab');
                tabs.forEach(tab => {
                    if (tab.innerText && (tab.innerText.includes('Readability') || tab.innerText.includes('可读性'))) {
                        tab.click();
                    }
                });
            }""")
            page.wait_for_timeout(2000)
            
            # Read readability bullets
            bullets = page.evaluate("""() => {
                const results = [];
                // Look for readability assessment results
                // Usually inside .yoast-analysis-results__layout or .yoast-assessment-list
                const items = document.querySelectorAll('.yoast-assessment-list li');
                items.forEach(item => {
                    const text = item.innerText;
                    const badge = item.querySelector('.yoast-badge');
                    let color = 'unknown';
                    if (badge) {
                        const classList = Array.from(badge.classList).join(' ');
                        if (classList.includes('bad') || classList.includes('red')) color = 'red';
                        else if (classList.includes('ok') || classList.includes('orange')) color = 'orange';
                        else if (classList.includes('good') || classList.includes('green')) color = 'green';
                    }
                    results.push({ text, color });
                });
                return results;
            }""")
            
            print("Readability items:")
            for b in bullets:
                print(f"[{b['color'].upper()}] {b['text']}")
                
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
