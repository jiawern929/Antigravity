import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to Chrome and clicking Yoast SEO tab...")
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
            
            # Locate and click the SEO tab inside Yoast
            # Based on HTML: <button class="...">SEO</button>
            print("Locating Yoast SEO tab button...")
            seo_tab = page.locator('#wpseo_meta button:has-text("SEO")').first
            if seo_tab.is_visible():
                seo_tab.click()
                print("Clicked SEO tab. Waiting for content update...")
                page.wait_for_timeout(2000)
            else:
                print("SEO tab button is not visible. Let's try alternative selector.")
                seo_tab_alt = page.locator('.yoast-assessment-tab button, button:has-text("SEO")').first
                if seo_tab_alt.is_visible():
                    seo_tab_alt.click()
                    print("Clicked SEO tab (alt). Waiting...")
                    page.wait_for_timeout(2000)
                else:
                    print("Could not find any SEO tab button.")
            
            # Save the new innerHTML
            html = page.evaluate("() => document.getElementById('wpseo_meta') ? document.getElementById('wpseo_meta').innerHTML : 'not found'")
            with open("C:\\Users\\jiawe\\.gemini\\antigravity\\scratch\\bi_yoast_dump.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("New HTML dumped.")
            
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
