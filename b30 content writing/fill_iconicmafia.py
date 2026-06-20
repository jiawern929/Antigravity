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
login_url = "https://iconicmafia.com/edd126/"
admin_post_url = "https://iconicmafia.com/wp-admin/post-new.php"
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
title = "Why Malaysian Families Struggle to Find the Best KL water filter Today"
excerpt = (
    "Many Malaysians actually get stuck here when dealing with daily kitchen chores. "
    "You turn on the tap and the water smells like heavy bleach. Washing white clothes becomes a nightmare due to sudden muddy water. "
    "This honest sharing explores our common daily frustrations. We break down simple facts to help you find the Best KL water filter for your home. "
    "Say goodbye to confusing sales talks. Let us help you choose the right setup to end your water headaches."
)
slug = "klwaterfilter2026"

# Yoast details
focus_keyword = "Best KL water filter"
seo_title = "Find the Best KL water filter to End Muddy Water"
meta_desc = (
    "Are you tired of yellow tap water and heavy kettle scale? Finding the Best KL water filter is crucial for your family. "
    "We explore local water problems to help you pick the perfect system. Avoid costly mistakes and protect your health today."
)

def run():
    print("Connecting to Chrome for iconicmafia.com automation...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Find any open iconicmafia tab
            page = None
            for p_page in context.pages:
                if "iconicmafia.com" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                page = context.new_page()
                print("Created new tab for iconicmafia.com")
            
            # Log in using the custom login URL
            print(f"Navigating to login page: {login_url}")
            try:
                page.goto(login_url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print("Page load timed out but continuing:", e)
            page.wait_for_timeout(3000)
            
            # Check if login form is present
            if page.locator('#user_login').is_visible():
                print("Logging in to iconicmafia.com...")
                page.locator('#user_login').fill(username)
                page.locator('#user_pass').fill(password)
                page.locator('#wp-submit').click()
                print("Login submitted. Waiting for redirect...")
                page.wait_for_timeout(8000)
            else:
                print("Already logged in or login form not visible. Checking current URL...")
                
            if "wp-admin" not in page.url:
                print("Not in wp-admin, navigating directly...")
                try:
                    page.goto("https://iconicmafia.com/wp-admin/", wait_until="domcontentloaded", timeout=45000)
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
            print("Uploading images to iconicmafia.com media library...")
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
            
            # Construct body HTML content
            body_content = f"""<!-- wp:paragraph -->
<p>Many Malaysians actually get stuck here. You wake up early to wash rice and the water looks slightly yellow. You boil water for your morning coffee and find thick white scale at the bottom of your expensive kettle. We all face these exact same daily annoyances. People living in busy Kuala Lumpur or older areas in Penang and Johor Bahru share this common struggle. Finding the Best KL water filter becomes a highly stressful mission for the whole family. You just want a simple and reliable solution for your kitchen. Yet you get completely confused by all the complicated machines displayed at the shopping mall. Every promoter claims they have the greatest technology in the world. We understand this daily pain perfectly well. Nobody wants to spend their precious weekend worrying about dirty tap water. You want to spend time with your family, not scrubbing white stains off your kitchen sink.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>To summarize, securing clean water at home requires understanding that municipal water treatment is only the first step, as piping contamination often occurs before the water reaches your tap. Let us talk about the real headache hiding in your kitchen. You turn on the bathroom tap to wash your face and the water smells strongly of chlorine. You worry about your young kids drinking that water every single day. Many parents end up buying heavy cartons of mineral water from the supermarket. Carrying those heavy water bottles up to your condo is exhausting and terrible for your back. Boiling the tap water takes too much time and energy. Besides, boiling only kills the living germs anyway. It never removes the physical rust, fine sand, and weird chemical smells. You need a proper physical machine to trap the dirt before it enters your drinking cup. Dealing with water issues should not feel like a second job. You need a permanent fix that runs quietly in the background.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img1_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://iconicmafia.com/edd126/?attachment_id={img1_id}"><img src="{img1_url}" alt="Best KL water filter" class="wp-image-{img1_id}"/></a><figcaption class="wp-element-caption"><a href="https://filken.com/" target="_blank" rel="noopener">Filken</a> Outdoor Master Filter on Gate Pillar.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why Your Old House Pipes Need the Best KL water filter</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The main issue usually hides right under our busy streets. Our government treatment plants actually do an excellent job cleaning the water. The big trouble starts when that clean water travels through miles of old rusty pipes. Many mature residential areas use underground pipes that are decades old. These neglected pipes slowly break down and rust over time. They release tiny rust particles and brown sand into the community water supply. When you hear your neighbors discussing the newest KL water filter 2026 models, they are trying to solve this exact problem. You simply cannot escape the dirt inside those aging community pipes. The dirt travels straight into your house water tank. It settles at the bottom and creates a thick layer of mud over the years. This invisible threat makes a proper home purification system absolutely necessary. You cannot rely on your eyes to judge water safety. Sometimes the water looks crystal clear but still carries a heavy chemical taste.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img2_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://iconicmafia.com/edd126/?attachment_id={img2_id}"><img src="{img2_url}" alt="Best KL water filter" class="wp-image-{img2_id}"/></a><figcaption class="wp-element-caption">Filken Outdoor Master Filters Installation.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Solving Water Issues for Condos and Landed Homes</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Your specific house type creates another layer of daily frustration. Imagine living in a nice high rise condo in the city. You suffer from low water pressure during the evening peak hours when everyone takes a shower. Your building management also strictly forbids you from installing any big filter tanks outside your door. You are forced to hunt for a small indoor unit that actually works well. You often ask friends for a reliable KL water filter recommend option that fits inside tiny kitchen cabinets. You can click here to check out our <a href="https://iconicmafia.com/edd126/?attachment_id={img1_id}">Filken outdoor water filter installation gallery</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>On the other hand, if you own a landed house in Johor Bahru or Melaka, you have a huge physical advantage. You can easily install an outdoor master filter right next to your main water meter. This brilliant setup stops the thick yellow mud from ever entering your indoor pipes. It protects your expensive washing machines and bathroom heaters. If they skip the outdoor tank, their white shirts turn yellowish after just a few washes. Every home requires a specific approach to end these daily annoyances. Buying the wrong system means you waste money and still suffer from the same old water problems.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img3_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://iconicmafia.com/?attachment_id={img3_id}"><img src="{img3_url}" alt="Best KL water filter" class="wp-image-{img3_id}"/></a><figcaption class="wp-element-caption">Filken Outdoor Stainless Steel Filter.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The Hidden Pain of Expensive Filter Replacements</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Buying the machine is only the beginning of your financial worries. We hear so many painful complaints about crazy maintenance fees from local homeowners. You visit a weekend electrical fair and buy a very cheap machine on impulse. Six months later, the machine starts beeping loudly to warn you. You call the service company to change the inside cartridge. The repair guy quotes you a price that almost equals the cost of a brand new machine. This hidden cost traps many innocent families in a bad contract. People naturally delay changing the cartridge because it is just too expensive. The dirty old cartridge then breeds harmful bacteria right inside your kitchen area. You end up drinking water that is much worse than normal tap water. You must always ask about the yearly maintenance fees before paying any deposit.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Smart buyers calculate the long term costs to avoid this painful trap completely. A good system should be easy and affordable to maintain over the next ten years. When looking for the Best KL water filter 2026 option, always ask the salesman about the exact price of the yearly replacement filters. You need to know the true cost of ownership.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Getting Real Help for Your Best KL water filter Setup</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Walking into a crowded showroom often feels like entering a noisy battlefield. Aggressive salesmen surround you immediately from all sides. They use scary scientific terms to push the most expensive model on you. They do not care if you only need basic drinking water for two working adults. They just want to close a big sale and earn their high commission.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>In this kind of situation, professional water filter teams like Filken Malaysia usually play a more neutral, administrative, or supportive role. They will visit your house to check your sink space and test your pipe pressure first. They listen closely to your actual daily struggles before suggesting any Best KL water filter 2026 setup. Having an honest consultant completely removes all the stress from your shopping experience. You get practical advice based on your actual kitchen layout and daily habits. They handle the messy installation work so you can just relax and enjoy the clean water. Good customer service makes a massive difference when dealing with home appliances. For more detailed instructions on setting up this device, please refer to the official <a href="https://filken.com/">Filken Website</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Final Thoughts on Securing Clean Water Everyday</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Dealing with poor water quality is extremely annoying and totally unnecessary today. You already work hard all day at the office or running your business. You should not have to worry about yellow tap water ruining your evening cooking routine. Stop buying endless plastic water bottles from the grocery store every weekend. Start looking into a proper home purification system to protect your entire family. Always measure your kitchen space carefully and calculate the yearly maintenance costs first. Find a reliable local team to handle the complicated pipe installation work safely. We sincerely hope this honest sharing helps you finally find the Best KL water filter for your home. You deserve to enjoy a clean, safe, and refreshing glass of water anytime you want. Protect your loved ones today and say goodbye to those frustrating water headaches forever. A good water system is the best investment you can make for your daily health and peace of mind.</p>
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
                
            screenshot_path = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\yoast_result_iconicmafia.png"
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"Screenshot saved to: {screenshot_path}")
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
