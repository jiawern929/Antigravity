import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    url = "https://dushitoutiao.com/klwaterfilter2026/"
    resource_id = "sc-domain:dushitoutiao.com"
    gsc_url = f"https://search.google.com/search-console/inspect?resource_id={resource_id}&id={url}"
    
    print(f"Opening GSC URL: {gsc_url}")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            page = context.new_page()
            
            page.goto(gsc_url, wait_until="load", timeout=90000)
            print("Page loaded. Waiting for GSC URL inspection to finish...")
            
            # GSC showing "Retrieving data from Google Index" overlay
            # Let's wait up to 30 seconds for GSC to load the inspection results
            page.wait_for_timeout(15000)
            
            # Check if there is "Request Indexing" button
            # In English: "Request Indexing". In Chinese: "请求编入索引"
            # Selector could be button:has-text("Request Indexing") or button:has-text("请求编入索引")
            request_btn = None
            for selector in [
                'div[role="button"]:has-text("Request Indexing")',
                'div[role="button"]:has-text("请求编入索引")',
                'div[button]:has-text("Request Indexing")',
                'div:has-text("Request Indexing")',
                'span:has-text("Request Indexing")',
                'span:has-text("请求编入索引")'
            ]:
                try:
                    el = page.locator(selector).first
                    if el.is_visible():
                        request_btn = el
                        print(f"Found request button using selector: {selector}")
                        break
                except Exception:
                    pass
            
            if not request_btn:
                # Let's print out all divs/spans containing text like "indexing" or "索引"
                text_elements = page.evaluate("""() => {
                    const els = document.querySelectorAll('div, span, button');
                    return Array.from(els)
                        .filter(el => el.innerText && (el.innerText.includes('Request') || el.innerText.includes('索引') || el.innerText.includes('Index')))
                        .map(el => ({ tag: el.tagName, text: el.innerText.substring(0, 100), class: el.className }));
                }""")
                print("Potential elements:")
                for te in text_elements[:15]:
                    print(te)
                    
            if request_btn:
                print("Clicking 'Request Indexing' button...")
                request_btn.click()
                print("Waiting for indexing popup/dialog (could take up to 2 minutes)...")
                
                # Wait for the "Submitting request" dialog and then the confirmation
                # Let's wait in increments and take screenshots
                for i in range(6):
                    page.wait_for_timeout(20000)
                    print(f"Waited {20 * (i+1)} seconds...")
                    
                    # Check if "Indexing requested" or "已请求编入索引" is present
                    has_completed = page.evaluate("""() => {
                        return document.body.innerText.includes('Indexing requested') || 
                               document.body.innerText.includes('已请求编入索引') ||
                               document.body.innerText.includes('Dismiss') ||
                               document.body.innerText.includes('知道了');
                    }""")
                    if has_completed:
                        print("Indexing request submitted successfully!")
                        break
            
            screenshot_path = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\dushitoutiao_indexing.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to: {screenshot_path}")
            page.close()
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
