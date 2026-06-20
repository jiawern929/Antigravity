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
login_url = "https://onasianews.com/edd133/"
admin_post_url = "https://onasianews.com/wp-admin/post-new.php"
username = "Ashley"
password = "($eiCp&6bNawGqCc*I6hw&*5"

# Images
images = [
    {
        "path": r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\media__1781290964634.jpg",
        "name": "filken_white_wall_filter.jpg",
        "title": "Filken Outdoor Master Filter Installation on White Wall",
        "role": "content_1"
    },
    {
        "path": r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\media__1781290964637.jpg",
        "name": "filken_grey_wall_water_meter.jpg",
        "title": "Filken Outdoor Filter System on Grey Wall",
        "role": "content_2"
    },
    {
        "path": r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\media__1781290977984.jpg",
        "name": "three_glasses_water_comparison.jpg",
        "title": "Three Glasses showing Dirty, Cloudy, and Clean Water",
        "role": "cover"
    }
]

# Post details
title = "Why Many Local Homes Upgrade to the Best KL water filter Before Renovations"
excerpt = (
    "This news report explores the current reality of local community pipes. "
    "We explain simple concepts to help you find the Best KL water filter for your property type. "
    "Forget about confusing sales pitches and complicated technical details. Discover practical home upgrade "
    "advice to secure clean drinking water for your beloved family today."
)
slug = "klwaterfilter2026"

# Yoast details
focus_keyword = "Best KL water filter"
seo_title = "Find Best KL water filter | Stop Dirty Tap Water"
meta_desc = "Finding the Best KL water filter is highly essential for families today. Aging pipes in local neighborhoods cause hidden dirty water issues daily."

def run():
    print("Connecting to Chrome for onasianews.com automation...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Find any open onasianews tab or create one
            page = None
            for p_page in context.pages:
                if "onasianews.com" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                page = context.new_page()
                print("Created new tab for onasianews.com")
            
            # Navigate to custom login
            print(f"Navigating to login page: {login_url}")
            try:
                page.goto(login_url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print("Page load timed out but continuing:", e)
            page.wait_for_timeout(3000)
            
            # Check if login form is present
            if page.locator('#user_login').is_visible():
                print("Logging in to onasianews.com...")
                page.locator('#user_login').fill(username)
                page.locator('#user_pass').fill(password)
                page.locator('#wp-submit').click()
                print("Login submitted. Waiting for redirect...")
                page.wait_for_timeout(8000)
                
            if "wp-admin" not in page.url:
                print("Not in wp-admin, navigating directly...")
                try:
                    page.goto("https://onasianews.com/wp-admin/", wait_until="domcontentloaded", timeout=45000)
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
            print("Uploading images to onasianews.com media library...")
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
            cover_id = uploaded_images["cover"]["id"]
            
            # Construct body HTML content
            body_content = f"""<!-- wp:paragraph -->
<p>(KUALA LUMPUR, 11 June) - Residents across the Klang Valley currently face a growing daily frustration with sudden muddy tap water. Specifically, recent frequent water pipe repairs cause dirty water to flow straight into community residential tanks. As a result, many busy working parents notice yellowish stains ruining their white laundry and expensive kitchen sinks.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>To summarize, securing clean water at home requires understanding that municipal water treatment is only the first step, as piping contamination often occurs before the water reaches your tap. Consequently, this sudden rise in water issues forces many local families to urgently search for the Best KL water filter to protect their homes. Indeed, they realize that relying purely on boiling water is no longer a safe practice for their young children. This report investigates the current community water situation and explores practical home solutions for everyday citizens. We aim to highlight the ongoing trends in home appliance upgrades and share practical insights for new property owners.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The core issue actually hides deep beneath our busy main roads. However, government water treatment plants always release highly clean and safe water. The major contamination happens during the long transport journey to our housing areas. Specifically, many mature neighborhoods in Penang, Johor Bahru, and the capital city still use decades old underground metal pipes. These aging community pipes rust quietly and break down over many years. Consequently, they release tiny rust flakes and brown sand into the main water supply continuously.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Therefore, many senior citizens still strongly believe that boiling the tap water is totally enough to ensure safety. They assume the high heat will automatically destroy everything bad inside the boiling pot. Boiling only kills the living bacteria successfully. It never removes the physical rust, the dangerous heavy metals, or the strong chlorine smell. Ultimately, families eventually realize they definitely need a physical machine barrier to block the dirt permanently.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img1_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://onasianews.com/edd133/?attachment_id={img1_id}"><img src="{img1_url}" alt="Best KL water filter" class="wp-image-{img1_id}"/></a><figcaption class="wp-element-caption"><a href="https://filken.com/" target="_blank" rel="noopener">Filken</a> Outdoor Master Filter Installation on White Wall.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Understanding the Urgent Need for the Best KL water filter</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Many local homeowners share similar bad experiences during their weekend routines. Specifically, they wake up early to wash their cars or clean their car porches. Suddenly, the hose sprays thick brown mud everywhere. This frustrating scene happens very often after the local water council fixes a broken community pipe nearby. You can click here to check out our <a href="https://onasianews.com/edd133/?attachment_id={img1_id}">Filken outdoor water filter installation gallery</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The sudden water pressure change pushes all the trapped underground dirt straight into private homes. That is exactly why finding the Best KL water filter is no longer a luxury choice but an absolute daily necessity. People want a permanent physical barrier to block the annoying mud. They want to drink a simple glass of water without smelling strong bleaching chemicals. Consequently, they refuse to let dirty water ruin their newly renovated kitchens and expensive bathroom fittings.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img2_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://onasianews.com/edd133/?attachment_id={img2_id}"><img src="{img2_url}" alt="Best KL water filter" class="wp-image-{img2_id}"/></a><figcaption class="wp-element-caption">Filken Outdoor Filter System on Grey Wall.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How Condominiums and Landed Homes Tackle the Problem</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Property types strongly influence how residents upgrade their home purification systems today. High rise condo management teams usually enforce very strict renovation rules for all building residents. They strictly ban owners from placing huge water tanks in the public walking corridors outside their units. Therefore, apartment owners must install very compact indoor machines instead. They usually hide these small systems smartly underneath their narrow kitchen sinks. Meanwhile, corporate offices face another set of unique daily challenges. A busy office pantry in the city center needs a heavy duty machine that can serve fifty employees every single day without breaking down.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Landed house owners in suburban areas face completely different challenges altogether. Specifically, they receive the muddy water directly from the main road gate. They must install heavy duty outdoor filters to stop the thick mud immediately. This crucial outdoor setup successfully protects their indoor washing machines and expensive bathroom water heaters from permanent rust damage. Combining a large outdoor tank with a small indoor drinking dispenser forms the ultimate protection plan for many local families today.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The Rising Trend of Finding a KL water filter recommend</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Social media community groups now feature endless discussions about improving domestic water quality. Young couples frequently post questions seeking a reliable KL water filter recommend option for their newly renovated homes. They read countless online reviews and feel totally overwhelmed by the massive amount of technical jargon.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Some online influencers aggressively promote ultrafiltration technology because it keeps the natural minerals intact without using any electricity. Other companies heavily market reverse osmosis systems for creating the purest drinking water possible.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Consumers often get lost comparing these different technical features during their weekend shopping trips. The current consumer trend shows people moving away from overly complicated smart machines. Instead, they simply prefer a practical setup that matches their daily cooking and drinking habits perfectly without causing extra stress. Ultimately, they want reliable equipment that provides clean water quietly in the background.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Checking Hidden Costs for Any KL water filter 2026 Model</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A major issue highlighted by consumer groups recently involves hidden maintenance fees. Shoppers often visit weekend electrical roadshows and purchase very cheap machines on pure impulse. The massive discount banners easily distract them from checking the long term hidden commitments.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Six months later, the machine indicator warns them to replace the internal cartridge immediately. They call the service center and discover a very shocking truth. The replacement cartridge actually costs almost as much as buying a brand new machine entirely.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Many families naturally delay changing the filter to save their monthly household expenses. The old and dirty cartridge quickly becomes a dangerous breeding ground for harmful bacteria. The family ends up drinking water that is much worse than direct tap water. Smart buyers must always calculate the precise yearly maintenance costs before paying any initial deposit. You must ensure your chosen KL water filter 2026 model remains highly affordable to maintain over the next ten years. A good purification system should protect your wallet just as much as it protects your physical health.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Getting Neutral Advice for the Best KL water filter Setup</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Visiting a crowded shopping mall exhibition often brings unnecessary stress to ordinary working people. Aggressive brand promoters instantly surround them from all sides trying to close a fast sale. These salesmen often push the most expensive models without checking the actual pipe water pressure of the house. They ignore the real daily lifestyle needs of the family entirely.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>In this kind of situation, professional water filter teams like Filken Malaysia usually play a more neutral, administrative, or supportive role. Specifically, they take proper time to visit the actual house and measure the exact kitchen cabinet space. Additionally, they test the pipe flow accurately before suggesting any specific equipment. Having an honest technical consultant removes all the stress from the home upgrade process. Customers feel much safer knowing they are buying a system tailored to their actual property conditions. For more details on this model, please visit the official <a href="https://filken.com/">Filken Website</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Final Thoughts on the Best KL water filter Journey</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Upgrading your home appliances should always bring joy and peace of mind to your family. The growing demand for clean water clearly reflects our rising local living standards. You no longer need to tolerate yellowish tap water ruining your evening dinner routines. Take the right steps to measure your kitchen space carefully and calculate the long term maintenance fees accurately. Find a responsible technical team to handle the messy pipe installation work safely. We sincerely hope this news report helps you navigate the confusing market confidently. You can finally secure the Best KL water filter for your beloved home. Enjoying a clean, safe, and refreshing glass of water is a basic necessity every family truly deserves.</p>
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
                
            screenshot_path = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\yoast_result_onasianews.png"
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"Screenshot saved to: {screenshot_path}")
            
        except Exception as e:
            print("Error occurred:", e)

if __name__ == "__main__":
    run()
