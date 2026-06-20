import sys
import base64
import os
import time
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Site info
login_url = "https://globalstraits.com/edd132/"
admin_post_url = "https://globalstraits.com/wp-admin/post-new.php"
username = "Ashley"
password = "($eiCp&6bNawGqCc*I6hw&*5"

# Images
images = [
    {
        "path": r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\media__1781273942262.jpg",
        "name": "filken_gate_pillar_filter.jpg",
        "title": "Filken Outdoor Master Filter on Gate Pillar",
        "role": "content_1"
    },
    {
        "path": r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\media__1781273942263.jpg",
        "name": "filken_double_outdoor_filters.jpg",
        "title": "Filken Outdoor Master Filters Installation",
        "role": "content_2"
    },
    {
        "path": r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\media__1781273942274.jpg",
        "name": "filken_stainless_filter_wall.jpg",
        "title": "Filken Outdoor Stainless Steel Filter on Wall",
        "role": "content_3"
    },
    {
        "path": r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\media__1781273967017.jpg",
        "name": "holding_glass_of_clean_water.jpg",
        "title": "Person Holding a Glass of Clean Filtered Water",
        "role": "cover"
    }
]

# Post details
title = "Why Are Malaysian Families Struggling to Find the Best KL water filter Today"
excerpt = (
    "This sharing explores the common struggles faced by local families. We break down the simple facts "
    "to help you find the Best KL water filter for your specific housing needs. Say goodbye to confusing sales tactics "
    "and discover practical advice to solve your daily water headaches once and for all."
)
slug = "klwaterfilter2026"

# Yoast details
focus_keyword = "Best KL water filter"
seo_title = "Find the Best KL water filter for Your Family Home"
meta_desc = "Finding the Best KL water filter is crucial for protecting your loved ones and home appliances."

def run():
    print("Connecting to Chrome for globalstraits.com automation...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Find any open globalstraits tab or create one
            page = None
            for p_page in context.pages:
                if "globalstraits.com" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                page = context.new_page()
                print("Created new tab for globalstraits.com")
            
            # Navigate to custom login
            print(f"Navigating to login page: {login_url}")
            try:
                page.goto(login_url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print("Page load timed out but continuing:", e)
            page.wait_for_timeout(3000)
            
            # Check if login form is present
            if page.locator('#user_login').is_visible():
                print("Logging in to globalstraits.com...")
                page.locator('#user_login').fill(username)
                page.locator('#user_pass').fill(password)
                page.locator('#wp-submit').click()
                print("Login submitted. Waiting for redirect...")
                page.wait_for_timeout(8000)
                
            if "wp-admin" not in page.url:
                print("Not in wp-admin, navigating directly...")
                try:
                    page.goto("https://globalstraits.com/wp-admin/", wait_until="domcontentloaded", timeout=45000)
                except Exception:
                    pass
                page.wait_for_timeout(3000)
                
            # Navigate to the editor page
            print(f"Navigating to: {admin_post_url}")
            try:
                page.goto(admin_post_url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print("Editor page load timed out but continuing:", e)
                
            print("Waiting for Gutenberg to load...")
            page.wait_for_function("() => window.wp && window.wp.data && window.wp.data.dispatch", timeout=30000)
            print("Gutenberg loaded.")
            
            # Upload images via REST API fetch
            print("Uploading images to globalstraits.com media library...")
            uploaded_images = {}
            for img in images:
                file_path = img["path"]
                if not os.path.exists(file_path):
                    print(f"File not found: {file_path}")
                    continue
                
                print(f"Reading file: {file_path}")
                with open(file_path, "rb") as f:
                    file_data = f.read()
                base64_data = base64.b64encode(file_data).decode("utf-8")
                
                upload_js = """
                async ([base64Data, filename, title]) => {
                    const binaryString = atob(base64Data);
                    const bytes = new Uint8Array(binaryString.length);
                    for (let i = 0; i < binaryString.length; i++) {
                        bytes[i] = binaryString.charCodeAt(i);
                    }
                    const arrayBuffer = bytes.buffer;
                    
                    const nonce = wpApiSettings.nonce;
                    const apiRoot = wpApiSettings.root;
                    
                    const response = await fetch(apiRoot + "wp/v2/media", {
                        method: "POST",
                        headers: {
                            "Content-Type": "image/jpeg",
                            "X-WP-Nonce": nonce,
                            "Content-Disposition": `attachment; filename="${filename}"`
                        },
                        body: arrayBuffer
                    });
                    
                    if (!response.ok) {
                        const errText = await response.text();
                        throw new Error(`Upload failed: ${response.status} ${response.statusText} - ${errText}`);
                    }
                    
                    const mediaObj = await response.json();
                    
                    // Update media metadata
                    try {
                        await fetch(apiRoot + `wp/v2/media/${mediaObj.id}`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-WP-Nonce": nonce
                            },
                            body: JSON.stringify({
                                title: title,
                                alt_text: "Best KL water filter",
                                description: "Best KL water filter"
                            })
                        });
                    } catch (e) {
                        console.error(e);
                    }
                    
                    return {
                        id: mediaObj.id,
                        source_url: mediaObj.source_url
                    };
                }
                """
                
                res = page.evaluate(upload_js, [base64_data, img["name"], img["title"]])
                print(f"Uploaded {img['role']}! ID: {res['id']}, URL: {res['source_url']}")
                uploaded_images[img["role"]] = {
                    "id": res["id"],
                    "url": res["source_url"],
                    "title": img["title"]
                }
                
            img1_id = uploaded_images["content_1"]["id"]
            img1_url = uploaded_images["content_1"]["url"]
            img2_id = uploaded_images["content_2"]["id"]
            img2_url = uploaded_images["content_2"]["url"]
            img3_id = uploaded_images["content_3"]["id"]
            img3_url = uploaded_images["content_3"]["url"]
            cover_id = uploaded_images["cover"]["id"]
            
            # Construct body HTML content with optimization
            body_content = f"""<!-- wp:paragraph -->
<p>Many young working adults in Kuala Lumpur rush home after a long day at the busy office. Specifically, you wake up early to wash rice and the water looks slightly yellow. Additionally, you boil water for your morning coffee and find thick white scale at the bottom of your expensive kettle. We all face these exact same daily annoyances. For instance, people living in busy Kuala Lumpur or older areas in Penang and Johor Bahru share this common struggle. Consequently, finding the Best KL water filter becomes a highly stressful mission for the whole family. After all, you just want a simple and reliable solution for your kitchen. Yet you get completely confused by all the complicated machines displayed at the shopping mall. As a result, every promoter claims they have the greatest technology in the world. We understand this daily pain perfectly well. Nobody wants to spend their precious weekend worrying about dirty tap water. You want to spend time with your family, not scrubbing white stains off your kitchen sink.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img1_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://globalstraits.com/edd132/?attachment_id={img1_id}"><img src="{img1_url}" alt="Best KL water filter" class="wp-image-{img1_id}"/></a><figcaption class="wp-element-caption"><a href="https://filken.com/" target="_blank" rel="noopener">Filken</a> Outdoor Master Filter on Gate Pillar.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The Reality Behind Clean Municipal Water</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>To summarize, securing clean water at home requires understanding that municipal water treatment is only the first step, as piping contamination often occurs before the water reaches your tap. Let us talk about the real headache hiding in your kitchen. For example, you turn on the bathroom tap to wash your face and the water smells strongly of chlorine. Naturally, you worry about your young kids drinking that water every single day. Therefore, many parents end up buying heavy cartons of mineral water from the supermarket. Ultimately, carrying those heavy water bottles up to your condo is exhausting and terrible for your back.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>In addition, boiling the tap water takes too much time and energy. Besides, boiling only kills the living germs anyway. It never removes the physical rust, fine sand, and weird chemical smells. Therefore, you need a proper physical machine to trap the dirt before it enters your drinking cup. Dealing with water issues should not feel like a second job. As a result, you need a permanent fix that runs quietly in the background.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img2_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://globalstraits.com/edd132/?attachment_id={img2_id}"><img src="{img2_url}" alt="Best KL water filter" class="wp-image-{img2_id}"/></a><figcaption class="wp-element-caption">Filken Outdoor Master Filters Installation.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why Condominium Owners Need the Best KL water filter 2026</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Young couples living in high-rise condominiums face very unique challenges every single day. For starters, they often struggle with terribly low water pressure during the evening rush hour. Everyone in the whole building is taking a shower at the exact same time after work. Furthermore, building management usually has very strict renovation rules for all residents. Condo owners cannot simply install a huge master water tank in the shared hallway outside their door.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>As a result, they are forced to find smart and compact indoor solutions instead. This is exactly why searching for the Best KL water filter 2026 model becomes a top priority for them. Consequently, they need a small machine that fits perfectly under their narrow kitchen sink. Some families prefer a slim countertop dispenser that provides instant hot water for their morning coffee. Ultimately, they want a system that looks highly modern but works powerfully without taking up any precious cooking space on the counter.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img3_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://globalstraits.com/edd132/?attachment_id={img3_id}"><img src="{img3_url}" alt="Best KL water filter" class="wp-image-{img3_id}"/></a><figcaption class="wp-element-caption">Filken Outdoor Stainless Steel Filter.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Solving Yellow Water Issues for Landed House Families</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Families living in landed properties experience entirely different daily struggles compared to condo residents. Specifically, a large family in a Johor Bahru terrace house might get yellow muddy water directly from the main road gate. This muddy water enters the washing machine and completely ruins expensive white school uniforms. It also slowly damages the bathroom water heaters over a few years. You can click here to check out our <a href="https://globalstraits.com/edd132/?attachment_id={img1_id}">Filken outdoor water filter installation gallery</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>For these specific households, installing a small indoor purifier is simply not enough to solve the root problem. Therefore, they must install a heavy-duty outdoor sand filter right next to their main water meter. This large outdoor cylinder acts as a strong protective shield for the entire house. It stops the thick mud from ever entering the indoor piping system. Many smart homeowners today choose to combine an outdoor filter with an indoor drinking purifier. Consequently, this comprehensive two-step approach completely ends their daily water headaches.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Understanding the Real Cost of a KL water filter 2026 System</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Many local families make a huge financial mistake during weekend electrical roadshows at the mall. For instance, a young father might see a massive discount banner and buy a cheap purification machine on pure impulse. Shortly after, he brings it home happily thinking he saved a lot of money. Six months later, the machine indicator lights up to signal a filter change. As a result, he calls the service center and receives a massive shock from the customer service agent. The replacement cartridge actually costs almost as much as a brand new machine.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>This hidden maintenance fee traps many innocent families every single year. Therefore, they naturally delay changing the filter to save their monthly household expenses. The old and dirty cartridge quickly becomes a breeding ground for dangerous bacteria. Consequently, the family ends up drinking water that is much worse than direct tap water. Smart buyers always calculate the yearly maintenance costs accurately before paying any initial deposit. Ultimately, a reliable KL water filter 2026 setup must be highly affordable to maintain in the long run.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Getting Honest Advice for Your Best KL water filter Setup</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Walking into a crowded shopping mall exhibition often feels extremely overwhelming for ordinary working people. Indeed, aggressive brand promoters surround them immediately from all sides trying to close a sale. Usually, these salesmen use scary scientific words to push the most expensive models available on the floor. Furthermore, they rarely listen to what the family actually needs for their daily lifestyle.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>A small family of three definitely does not need a heavy-duty corporate machine meant for fifty people. Instead, they just want clean and safe drinking water for their daily home cooked meals. In this kind of situation, professional water filter teams like Filken Malaysia usually play a more neutral, administrative, or supportive role. Specifically, they take the necessary time to visit the house and check the exact pipe water pressure. Additionally, they inspect the available kitchen cabinet space carefully. Specifically, they listen to the daily drinking habits of the family members before suggesting any specific equipment. Therefore, having an honest consultant removes all the unnecessary stress from the buying process. For more detailed instructions on setting up this device, please refer to the official <a href="https://filken.com/">Filken Website</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Final Thoughts on Protecting Your Loved Ones Daily</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Dealing with poor water quality is extremely frustrating for busy working parents in Malaysia. After all, they already face enough stress at the office every single day. Specifically, they should not have to worry about yellow tap water ruining their evening family cooking routine. Consequently, carrying heavy plastic water bottles from the supermarket every weekend is also terrible for their backs. Therefore, families should actively start looking into a proper home purification system.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>To protect their long term health, they must measure their kitchen space correctly and calculate the yearly maintenance fees accurately. Find a reliable technical team to handle the pipe installation safely to avoid future leaks. We sincerely hope this sharing helps local families finally find the Best KL water filter for their living space. Every home deserves a clean, safe, and refreshing glass of water without any hidden worries.</p>
<!-- /wp:paragraph -->"""
            
            # Set post content, title, excerpt and featured image
            print("Populating content, title, and excerpt...")
            page.evaluate("""([title, html, excerpt, coverId]) => {
                const blocks = wp.blocks.parse(html);
                wp.data.dispatch('core/editor').resetBlocks(blocks);
                
                wp.data.dispatch('core/editor').editPost({
                    title: title,
                    excerpt: excerpt,
                    featured_media: coverId
                });
            }""", [title, body_content, excerpt, cover_id])
            
            page.wait_for_timeout(2000)
            
            # Set Yoast and slug
            print("Populating Yoast SEO metadata and slug...")
            page.evaluate("""([title, desc, kw, slug]) => {
                wp.data.dispatch('core/editor').editPost({
                    slug: slug,
                    meta: {
                        _yoast_wpseo_title: title,
                        _yoast_wpseo_metadesc: desc,
                        _yoast_wpseo_focuskw: kw
                    }
                });
            }""", [seo_title, meta_desc, focus_keyword, slug])
            
            page.wait_for_timeout(2000)
            
            # Sync with Yoast UI inputs
            print("Syncing Yoast UI inputs natively in DOM...")
            js_script = """
            ([kw, title, desc]) => {
                const setReactInput = (selector, value) => {
                    const el = document.querySelector(selector);
                    if (!el) {
                        console.log("Element not found: " + selector);
                        return false;
                    }
                    
                    if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                        const prototype = el.tagName === 'INPUT' ? window.HTMLInputElement.prototype : window.HTMLTextAreaElement.prototype;
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(prototype, "value").set;
                        nativeInputValueSetter.call(el, value);
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                    } else {
                        el.innerText = value;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                    console.log("Set value for: " + selector);
                    return true;
                };
                
                const setKw = setReactInput('#focus-keyword-input-metabox', kw);
                const setTitle = setReactInput('#yoast-google-preview-title-metabox', title);
                const setDesc = setReactInput('#yoast-google-preview-description-metabox', desc);
                
                return { setKw, setTitle, setDesc };
            }
            """
            
            res = page.evaluate(js_script, [focus_keyword, seo_title, meta_desc])
            print(f"DOM input setting result: {res}")
            page.wait_for_timeout(2000)
            
            # Save Draft
            print("Saving Draft...")
            save_button = page.locator('button:has-text("保存草稿"), button:has-text("Save draft"), button:has-text("Save Draft"), button.editor-post-save-draft').first
            save_button.click()
            page.wait_for_timeout(8000)
            print("Draft saved.")
            
            # Scroll Yoast meta into view and take screenshot
            try:
                page.locator('#wpseo_meta').scroll_into_view_if_needed(timeout=5000)
                page.wait_for_timeout(2000)
            except Exception:
                pass
                
            screenshot_path = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\yoast_result_globalstraits.png"
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"Screenshot saved to: {screenshot_path}")
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
