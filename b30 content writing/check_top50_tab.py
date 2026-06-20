import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run():
    print("Connecting to browser to inspect top50malaysia.com tab...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            page = None
            for p_page in context.pages:
                if "top50malaysia.com" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find top50malaysia.com tab.")
                return
            
            print(f"Found tab: {page.title()} - {page.url}")
            
            # Let's get title, blocks content, and Yoast fields
            post_data = page.evaluate("""() => {
                const title = wp.data.select('core/editor').getEditedPostAttribute('title');
                const content = wp.data.select('core/editor').getEditedPostAttribute('content');
                const excerpt = wp.data.select('core/editor').getEditedPostAttribute('excerpt');
                const slug = wp.data.select('core/editor').getEditedPostAttribute('slug');
                const meta = wp.data.select('core/editor').getEditedPostAttribute('meta') || {};
                
                return {
                    title,
                    contentLength: content ? content.length : 0,
                    excerpt,
                    slug,
                    yoast_title: meta._yoast_wpseo_title,
                    yoast_metadesc: meta._yoast_wpseo_metadesc,
                    yoast_focuskw: meta._yoast_wpseo_focuskw
                };
            }""")
            
            print(f"Title: {post_data['title']}")
            print(f"Slug: {post_data['slug']}")
            print(f"Content Length: {post_data['contentLength']}")
            print(f"Excerpt: {post_data['excerpt']}")
            print(f"Yoast Title: {post_data['yoast_title']}")
            print(f"Yoast Meta Description: {post_data['yoast_metadesc']}")
            print(f"Yoast Focus Keyword: {post_data['yoast_focuskw']}")
            
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
