import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Extracting Yoast bullets...")
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
            
            bullets = page.evaluate("""() => {
                const el = document.querySelector('#wpseo_meta');
                if (!el) return ["wpseo_meta not found"];
                
                // Let's expand SEO analysis section if collapsed
                const header = document.querySelector('.yoast-analysis-results__header');
                if (header) {
                    // Try to find list items
                }
                
                const results = [];
                const items = document.querySelectorAll('.yoast-analysis-result__label, .yoast-analysis-result, .yoast-assessment-list li');
                items.forEach(item => {
                    results.push(item.innerText);
                });
                return results;
            }""")
            
            print("Yoast Bullets Found:")
            for b in bullets:
                if b.strip():
                    print(f"- {b}")
                    
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
