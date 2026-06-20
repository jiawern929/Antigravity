import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Extracting Yoast Readability text...")
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
            
            # Click the Readability tab to ensure it is active
            page.evaluate("""() => {
                const tabs = document.querySelectorAll('.yoast-assessment-tabs li, .yoast-assessment-tab');
                tabs.forEach(tab => {
                    if (tab.innerText && (tab.innerText.includes('Readability') || tab.innerText.includes('可读性'))) {
                        tab.click();
                        console.log("Clicked readability tab");
                    }
                });
            }""")
            page.wait_for_timeout(2000)
            
            # Let's search for any red or orange bullets under the readability section
            readability_data = page.evaluate("""() => {
                const results = [];
                // Look for elements in the Yoast panel
                const lists = document.querySelectorAll('.yoast-assessment-list, [class*="assessment-list"]');
                lists.forEach((list, idx) => {
                    const items = list.querySelectorAll('li');
                    const listItems = [];
                    items.forEach(li => {
                        const badge = li.querySelector('.yoast-badge');
                        let score = 'unknown';
                        if (badge) {
                            const cls = Array.from(badge.classList).join(' ');
                            if (cls.includes('red') || cls.includes('bad')) score = 'red';
                            else if (cls.includes('orange') || cls.includes('ok')) score = 'orange';
                            else if (cls.includes('green') || cls.includes('good')) score = 'green';
                        }
                        listItems.push({ text: li.innerText, score: score });
                    });
                    results.push({ listIndex: idx, items: listItems });
                });
                return results;
            }""")
            
            print("Readability lists found:", len(readability_data))
            for r in readability_data:
                print(f"List {r['listIndex']}:")
                for item in r['items']:
                    print(f"  [{item['score'].upper()}] {item['text']}")
                    
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
