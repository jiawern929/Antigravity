import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to browser to check Yoast status...")
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
            
            # Wait for some time to let Yoast analyze
            page.wait_for_timeout(3000)
            
            # Dump the analysis results
            results = page.evaluate("""() => {
                const results = [];
                // Find all list items inside the Yoast Analysis section
                const items = document.querySelectorAll('.yoast-analysis-results__layout li');
                items.forEach(item => {
                    const text = item.innerText;
                    const badge = item.querySelector('.yoast-badge');
                    let color = 'unknown';
                    if (badge) {
                        if (badge.classList.contains('yoast-badge--red')) color = 'red';
                        else if (badge.classList.contains('yoast-badge--orange')) color = 'orange';
                        else if (badge.classList.contains('yoast-badge--green')) color = 'green';
                        else if (badge.classList.contains('yoast-badge--score-icon')) {
                            // Check the class or style
                            const classList = Array.from(badge.classList).join(' ');
                            if (classList.includes('bad') || classList.includes('red')) color = 'red';
                            else if (classList.includes('ok') || classList.includes('orange')) color = 'orange';
                            else if (classList.includes('good') || classList.includes('green')) color = 'green';
                        }
                    }
                    results.append({ text, color });
                });
                
                // Also get the main Yoast SEO score icon status
                const seoTab = document.querySelector('.yoast-assessment-tab__score');
                let overall = 'unknown';
                if (seoTab) {
                    overall = seoTab.getAttribute('aria-label') || seoTab.className;
                }
                
                return { items: Array.from(items).map(el => el.innerText), overall };
            }""")
            
            print(f"Overall SEO Assessment score: {results['overall']}")
            print("\nAnalysis items:")
            for item in results['items']:
                print(f"- {item}")
                
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
