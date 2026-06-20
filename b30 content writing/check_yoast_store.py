import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking Yoast SEO Redux store...")
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
            
            js_script = """
            () => {
                const getYoastScore = () => {
                    // Yoast stores its state in various locations depending on the version
                    // Let's print out what wp.data registries we can find
                    const stores = wp.data.getSelectors ? Object.keys(wp.data.select('core')) : [];
                    
                    const score = {};
                    try {
                        // In some versions, Yoast has its own store
                        const yoastStore = wp.data.select('yoast-seo');
                        if (yoastStore) {
                            score.yoastStoreExists = true;
                            // check available selectors
                            score.selectors = Object.keys(yoastStore);
                        }
                    } catch(e) {
                        score.yoastStoreError = e.message;
                    }
                    
                    try {
                        // Let's get the active score from Yoast's DOM indicator or analysis
                        const scoreIcon = document.querySelector('.yoast-assessment-tab__score');
                        if (scoreIcon) {
                            score.domScoreAria = scoreIcon.getAttribute('aria-label');
                            score.domScoreClass = scoreIcon.className;
                        }
                        
                        // Let's check the Yoast metabox header score
                        const seoTabLink = document.querySelector('#yoast-seo-tab-seo');
                        if (seoTabLink) {
                            score.seoTabLinkHTML = seoTabLink.outerHTML;
                        }
                        
                        const scoreContainer = document.querySelector('.wpseo-score-icon-container');
                        if (scoreContainer) {
                            score.scoreContainerHTML = scoreContainer.outerHTML;
                        }
                    } catch(e) {
                        score.domError = e.message;
                    }
                    
                    return score;
                };
                
                return getYoastScore();
            }
            """
            
            res = page.evaluate(js_script)
            print("Yoast Store Details:")
            print(res)
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
