import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking Yoast SEO score details...")
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
            
            # Check the Yoast sidebar score or meta box score
            score_data = page.evaluate("""() => {
                const getScore = (selector) => {
                    const el = document.querySelector(selector);
                    if (!el) return null;
                    return {
                        className: el.className,
                        text: el.innerText,
                        ariaLabel: el.getAttribute('aria-label')
                    };
                };
                
                // Let's look for Yoast SEO score indicators
                const scoreIndicators = [];
                // Look for SVG or span with class containing 'yoast' or 'seo' score
                const badges = document.querySelectorAll('[class*="yoast"], [class*="seo"]');
                badges.forEach(b => {
                    if (b.className && typeof b.className === 'string' && (b.className.includes('score') || b.className.includes('badge') || b.className.includes('assessment'))) {
                        scoreIndicators.push({
                            tag: b.tagName,
                            class: b.className,
                            text: b.innerText ? b.innerText.substring(0, 100) : '',
                            ariaLabel: b.getAttribute('aria-label')
                        });
                    }
                });
                
                return {
                    scoreIndicators: scoreIndicators.slice(0, 20)
                };
            }""")
            
            print("Score indicators found:")
            for ind in score_data['scoreIndicators']:
                print(ind)
                
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
