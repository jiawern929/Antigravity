import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Checking Yoast SEO layout in Gutenberg...")
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
            
            # Click the Yoast icon in the top toolbar to expand the Yoast sidebar (if it exists)
            page.evaluate("""() => {
                const buttons = document.querySelectorAll('button');
                buttons.forEach(b => {
                    const label = b.getAttribute('aria-label') || '';
                    if (label.includes('Yoast') || b.className.includes('yoast')) {
                        b.click();
                        console.log("Clicked Yoast button:", label);
                    }
                });
            }""")
            page.wait_for_timeout(3000)
            
            # Now let's dump the text of the entire sidebar if visible
            sidebar_content = page.evaluate("""() => {
                const sidebar = document.querySelector('.sidebar, .interface-sidebar, .edit-post-sidebar');
                if (sidebar) {
                    // Let's find all buttons and headings in the sidebar
                    const elements = sidebar.querySelectorAll('button, h2, h3, h4, span, li, p');
                    const details = [];
                    elements.forEach(el => {
                        const txt = el.innerText ? el.innerText.trim() : '';
                        if (txt.length > 2 && txt.length < 150) {
                            details.push({
                                tag: el.tagName,
                                class: el.className,
                                text: txt
                            });
                        }
                    });
                    return { found: true, details: details.slice(0, 50) };
                }
                return { found: false };
            }""")
            
            print("Sidebar found:", sidebar_content['found'])
            if sidebar_content['found']:
                for item in sidebar_content['details']:
                    print(f"[{item['tag']}] {item['class']}: {item['text']}")
                    
            # Let's also check if there is a Yoast metabox at the bottom
            metabox_content = page.evaluate("""() => {
                const metabox = document.querySelector('#wpseo_meta');
                if (metabox) {
                    const elements = metabox.querySelectorAll('button, span, li, p');
                    const details = [];
                    elements.forEach(el => {
                        const txt = el.innerText ? el.innerText.trim() : '';
                        if (txt.length > 2 && txt.length < 150) {
                            details.push({
                                tag: el.tagName,
                                class: el.className,
                                text: txt
                            });
                        }
                    });
                    return { found: true, details: details.slice(0, 50) };
                }
                return { found: false };
            }""")
            
            print("\nMetabox found:", metabox_content['found'])
            if metabox_content['found']:
                for item in metabox_content['details']:
                    print(f"[{item['tag']}] {item['class']}: {item['text']}")
                    
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
