import sys
import json
from playwright.sync_api import sync_playwright

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

targets = [
    {"name": "dushitoutiao", "domain": "dushitoutiao.com", "slug": "klwaterfilter2026", "url": "https://dushitoutiao.com/klwaterfilter2026/"},
    {"name": "businessinsider101", "domain": "businessinsider101.com", "slug": "klwaterfilter2026", "url": "https://businessinsider101.com/klwaterfilter2026/"},
    {"name": "asiatop40", "domain": "asiatop40.com", "slug": "klwaterfilter2026", "url": "https://asiatop40.com/industry-insights/klwaterfilter2026/"},
    {"name": "top50malaysia", "domain": "top50malaysia.com", "slug": "klwaterfilter2026", "url": "https://top50malaysia.com/klwaterfilter2026/"},
    {"name": "iconicmafia", "domain": "iconicmafia.com", "slug": "klwaterfilter2026", "url": "https://iconicmafia.com/klwaterfilter2026/"},
    {"name": "globalstraits", "domain": "globalstraits.com", "slug": "klwaterfilter2026", "url": "https://globalstraits.com/klwaterfilter2026/"},
    {"name": "onasianews", "domain": "onasianews.com", "slug": "klwaterfilter2026", "url": "https://onasianews.com/klwaterfilter2026/"},
    {"name": "billionairechamp", "domain": "billionairechamp.com", "slug": "kl-water-filter-recommendation-2026", "url": "https://billionairechamp.com/industry-insight/kl-water-filter-recommendation-2026/"},
    {"name": "huawennews", "domain": "huawennews.com", "slug": "kl-water-filter-recommendation", "url": "https://huawennews.com/kl-water-filter-recommendation/"}
]

def run():
    print("Connecting to Chrome CDP at port 9222...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            results = []
            for target in targets:
                name = target["name"]
                domain = target["domain"]
                slug = target["slug"]
                url = target["url"]
                
                print(f"Checking {domain} (slug: {slug})...")
                page = context.new_page()
                try:
                    # Navigate to wp-admin to ensure we are in a domain-matching context with cookies
                    admin_url = f"https://{domain}/wp-admin/"
                    page.goto(admin_url, wait_until="domcontentloaded", timeout=45000)
                    page.wait_for_timeout(2000)
                    
                    # Fetch post details from REST API
                    api_fetch_js = f"""
                    async () => {{
                        try {{
                            const response = await fetch('/wp-json/wp/v2/posts?slug={slug}');
                            if (!response.ok) return {{ error: 'API_ERROR', status: response.status }};
                            const data = await response.json();
                            if (data && data.length > 0) {{
                                return {{
                                    title: data[0].title.rendered,
                                    link: data[0].link
                                }};
                            }}
                            // Try another endpoint or custom query
                            return {{ error: 'NOT_FOUND' }};
                        }} catch (e) {{
                            return {{ error: 'FETCH_ERROR', message: e.message }};
                        }}
                    }}
                    """
                    
                    res = page.evaluate(api_fetch_js)
                    if res and "title" in res:
                        # Decode HTML entities if any (e.g. &#8211; -> –, &amp; -> &)
                        # We can do this in Python using html.unescape
                        import html
                        title = html.unescape(res["title"])
                        link = res["link"]
                        print(f"  FOUND: {title} -> {link}")
                        results.append({"url": link, "title": title})
                    else:
                        # Fallback: parse the title from the post edit page if slug can be searched on edit.php
                        print(f"  REST API returned: {res}. Searching edit.php...")
                        search_url = f"https://{domain}/wp-admin/edit.php?s={slug}"
                        page.goto(search_url, wait_until="domcontentloaded", timeout=45000)
                        page.wait_for_timeout(2000)
                        
                        post_info = page.evaluate("""() => {
                            const row = document.querySelector('tr.type-post');
                            if (!row) return null;
                            const titleEl = row.querySelector('.row-title');
                            const viewLinkEl = row.querySelector('.row-actions .view a') || row.querySelector('.row-actions .view_post a') || row.querySelector('a.row-title');
                            return {
                                title: titleEl ? titleEl.innerText.trim() : '',
                                url: viewLinkEl ? viewLinkEl.getAttribute('href') : ''
                            };
                        }""")
                        
                        if post_info and post_info["title"]:
                            title = post_info["title"].split(" — ")[0].strip()
                            link = post_info["url"] if post_info["url"] else url
                            print(f"  FOUND VIA SEARCH: {title} -> {link}")
                            results.append({"url": link, "title": title})
                        else:
                            print(f"  FAILED to find post details for {domain}")
                            results.append({"url": url, "title": "ERROR_NOT_FOUND"})
                except Exception as e:
                    print(f"  Error processing {domain}: {e}")
                    results.append({"url": url, "title": f"ERROR: {str(e)}"})
                finally:
                    page.close()
            
            print("\n" + "="*50)
            print("FINAL REPORT:")
            print("="*50)
            for r in results:
                print(f"《{r['title']}》")
                print(r["url"])
            print("="*50)
            
            browser.close()
        except Exception as e:
            print("Error connecting to CDP:", e)

if __name__ == "__main__":
    run()
