import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Yoast details
focus_keyword = "Best KL water filter"
seo_title = "Best KL water filter | Stop Drinking Dirty Tap Water Today"
meta_desc = "Are you drinking safe tap water at home? Many people ignore the hidden dirt in old pipes. As flooring experts, we share our insights on finding the Best KL water filter to protect your family's health and your newly renovated kitchen. Read our guide for local homeowners today."

def run():
    print("Connecting to Chrome to fix Yoast SEO inputs natively via DOM...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "top50malaysia.com/wp-admin" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find the open editor tab.")
                return
            
            print(f"Found editor tab: {page.url}")
            
            # Use native DOM script to fill Yoast inputs
            js_script = """
            ([kw, title, desc]) => {
                const setReactInput = (selector, value) => {
                    const el = document.querySelector(selector);
                    if (!el) {
                        console.log("Element not found: " + selector);
                        return false;
                    }
                    
                    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                        // React 16+ overrides the setter, we bypass it
                        const prototype = el.tagName === 'INPUT' ? window.HTMLInputElement.prototype : window.HTMLTextAreaElement.prototype;
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(prototype, "value").set;
                        nativeInputValueSetter.call(el, value);
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                    } else {
                        // Draft.js or contenteditable
                        el.innerText = value;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                    console.log("Set value for: " + selector);
                    return true;
                };
                
                // Let's also dispatch Gutenberg metadata update just in case
                wp.data.dispatch('core/editor').editPost({
                    meta: {
                        _yoast_wpseo_title: title,
                        _yoast_wpseo_metadesc: desc,
                        _yoast_wpseo_focuskw: kw
                    }
                });
                
                const setKw = setReactInput('#focus-keyword-input-metabox', kw);
                const setTitle = setReactInput('#yoast-google-preview-title-metabox', title);
                const setDesc = setReactInput('#yoast-google-preview-description-metabox', desc);
                
                return { setKw, setTitle, setDesc };
            }
            """
            
            res = page.evaluate(js_script, [focus_keyword, seo_title, meta_desc])
            print(f"DOM input setting result: {res}")
            page.wait_for_timeout(2000)
            
            # Click Save Draft
            print("Saving Draft...")
            save_button = page.locator('button:has-text("保存草稿"), button:has-text("Save draft"), button:has-text("Save Draft"), button.editor-post-save-draft').first
            save_button.click()
            page.wait_for_timeout(5000)
            print("Draft saved successfully.")
            
            # Take screenshot
            page.locator('#wpseo_meta').scroll_into_view_if_needed()
            page.wait_for_timeout(2000)
            screenshot_path = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\yoast_result_top50.png"
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"Screenshot saved to: {screenshot_path}")
            
        except Exception as e:
            print("Error during execution:", e)

if __name__ == "__main__":
    run()
