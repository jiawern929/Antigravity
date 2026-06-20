import sys
import base64
import os
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Site info
site_url = "https://top50malaysia.com/wp-admin/"
username = "Carmen"
password = "PFHx1pBpwoD*7#lPthajn!YC"

# Images to upload
images = [
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781271007572.jpg",
        "name": "filken_double_stainless_filters.jpg",
        "title": "Filken Double Stainless Steel Outdoor Filters",
        "role": "content_1"
    },
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781271007750.jpg",
        "name": "filken_grey_wall_filter.jpg",
        "title": "Filken Outdoor Master Filter Installation on Grey Wall",
        "role": "content_2"
    },
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781271007809.jpg",
        "name": "filken_outdoor_filter_light_grey.jpg",
        "title": "Filken Outdoor Filter Installation on Light Grey Wall",
        "role": "content_3"
    },
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781271033430.jpg",
        "name": "filken_kitchen_countertop.jpg",
        "title": "Top 50 Malaysia Modern Kitchen Countertop Filtration",
        "role": "cover"
    }
]

# Post details
title = "Why Are Homeowners Searching for the Best KL water filter Before Renovating Their Kitchen?"
excerpt = "Upgrading your home involves more than just beautiful new floors. What many people do not know is that the quality of your daily drinking water is just as important. In this knowledge sharing piece from Queensfloor, we break down the reality of tap water in the Klang Valley. We will help you understand the simple facts behind home filtration systems. Say goodbye to confusing technical terms. Discover practical tips to choose the right setup for your condo or landed property and keep your family safe from hidden pipe dirt."
slug = "klwaterfilter2026"

# Yoast details
focus_keyword = "Best KL water filter"
seo_title = "Best KL water filter | Stop Drinking Dirty Tap Water Today"
# Natural Meta Description as requested by the user (no keyword stuffing)
meta_desc = "Are you drinking safe tap water at home? Many people ignore the hidden dirt in old pipes. As flooring experts, we share our insights on finding the Best KL water filter to protect your family's health and your newly renovated kitchen. Read our guide for local homeowners today."

def run():
    print("Connecting to Chrome for top50malaysia.com automation...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Find the active tab or create one
            page = None
            for p_page in context.pages:
                if "top50malaysia.com" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                page = context.new_page()
                print("Created new tab for top50malaysia.com")
            
            # Navigate to wp-admin
            print(f"Navigating to: {site_url}")
            try:
                page.goto(site_url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print("Initial page load timed out but continuing:", e)
            page.wait_for_timeout(3000)
            
            # Check if login is needed
            if "wp-login.php" in page.url:
                print("Logging in to top50malaysia.com...")
                page.locator('#user_login').fill(username)
                page.locator('#user_pass').fill(password)
                page.locator('#wp-submit').click()
                print("Login submitted. Waiting...")
                page.wait_for_timeout(8000)
                
            if "wp-admin" not in page.url:
                print("Not in wp-admin, trying to load it directly...")
                try:
                    page.goto(site_url, wait_until="domcontentloaded", timeout=45000)
                except Exception:
                    pass
                
            print("Navigating to new post page...")
            try:
                page.goto("https://top50malaysia.com/wp-admin/post-new.php", wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print("New post page load timed out but continuing:", e)
                
            print("Waiting for Gutenberg to load...")
            page.wait_for_function("() => window.wp && window.wp.data && window.wp.data.dispatch", timeout=30000)
            print("Gutenberg loaded.")
            
            # Upload images via JS Fetch
            print("Uploading images to top50malaysia.com media library...")
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
                    
                    // Update media meta (alt text)
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
            
            # Construct body content with:
            # - Images placed ABOVE H2 headings
            # - Summary sentence in the beginning of the second paragraph
            # - Text internal link to Image 1's attachment page
            # - Text outbound link to filken.com
            
            body_content = f"""<!-- wp:paragraph -->
<p>Hello everyone. We are from the Queensfloor team. We spend our days helping local homeowners install beautiful new SPC flooring. We travel all across Kuala Lumpur, Johor Bahru, and Melaka. Because we spend so much time talking to families in their homes, we hear a lot about their daily struggles. Lately, many customers ask us about kitchen upgrades. They want to protect their new floors and cabinets from water damage. They also notice yellow stains on their expensive stainless steel sinks. They always ask us what the Best KL water filter is. Simply put, finding a good filtration system is just as crucial as picking waterproof flooring. We decided to write this friendly guide. We want to share what we have learned about water issues in local homes. We hope this helps you make a smarter choice for your family.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>To summarize, securing clean water at home requires understanding that municipal water treatment is only the first step, as piping contamination often occurs before the water reaches your tap. What many people do not know is that the water leaving our treatment plants is actually very clean. It meets all the required safety standards. The real trouble starts during the long journey to your house. Many older residential areas have very rusty underground pipes. As water travels through these aging lines, it picks up tiny mud particles. It also carries rust and heavy metals along the way. When you finally turn on your kitchen tap to wash vegetables, you get all that hidden dirt. We often hear aunties say that boiling water is enough. Oh, so that is how it is. Boiling your water will kill the bacteria. However, it will never remove the rust, sand, and chemical smells. You definitely need a proper physical barrier. A good machine stops the dirt before you drink it.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img1_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://top50malaysia.com/?attachment_id={img1_id}"><img src="{img1_url}" alt="Best KL water filter" class="wp-image-{img1_id}"/></a><figcaption class="wp-element-caption"><a href="https://filken.com/" target="_blank" rel="noopener">Filken</a> Double Stainless Steel Outdoor Filters.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Finding the Best KL water filter for Condos and Landed Homes</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Your house type actually dictates what kind of machine you can buy. If you live in a high rise apartment in the city center, the management usually has very strict rules. You cannot simply install huge water tanks in the shared hallway outside your unit. You must look for compact indoor models. These machines can fit perfectly under your kitchen sink or sit neatly on your countertop. On the other hand, if you own a landed house, you have a huge physical advantage. You can easily install an outdoor master filter right next to your main water meter. This brilliant setup stops the thick yellow mud from ever entering your indoor pipes. It protects your expensive washing machine. It keeps your water heater clean. Most importantly, it stops muddy water leaks from ruining our beautiful SPC floors. This two step approach is highly popular among homeowners today. You can click here to check out our <a href="https://top50malaysia.com/?attachment_id={img1_id}">Filken outdoor water filter installation gallery</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img2_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://top50malaysia.com/?attachment_id={img2_id}"><img src="{img2_url}" alt="Best KL water filter" class="wp-image-{img2_id}"/></a><figcaption class="wp-element-caption">Filken Outdoor Master Filter Installation on Grey Wall.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The Hidden Costs Behind Every KL water filter 2026 Model</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Many buyers only look at the initial price tag when visiting weekend electrical roadshows. They see a massive discount banner and immediately swipe their credit cards. But the truth is, buying a purification machine is exactly like buying a car. You absolutely must pay for regular maintenance. Inside every purifier, there are hidden cartridges. You must change these cartridges every few months. Some famous brands sell the main machine very cheaply. However, they charge a very high price for replacement parts later on. You must calculate the yearly maintenance cost before making any final decision. Do not let cheap upfront prices fool your wallet in the long run. If the replacement parts are too expensive, you might delay changing them. Delaying the change is very dangerous. Bacteria will grow inside the old cartridge. You will end up drinking water that is dirtier than normal tap water.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img3_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://top50malaysia.com/?attachment_id={img3_id}"><img src="{img3_url}" alt="Best KL water filter" class="wp-image-{img3_id}"/></a><figcaption class="wp-element-caption">Filken Outdoor Filter Installation on Light Grey Wall.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why Good Installation Matters for the Best KL water filter</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Let us talk about another critical thing that people always overlook during renovations. You can buy the most expensive model in the whole world. However, a bad installation job will ruin everything completely. We have seen this disaster many times while laying new floors in older kitchens. A sloppy plumber might connect the pipes very poorly. This causes hidden leaks behind your walls. The water slowly damages the bottom of your expensive wooden cabinets. Eventually, it reaches the floor and causes a huge mess. Moreover, water pressure in Malaysia can be very unstable. A good technician must test your house water pressure first. If the pressure is too low, the water will barely drip out of your expensive new machine. You need experts who really understand local building structures. They must do the job right the first time.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Seeking Honest Advice for Your Kitchen Upgrade</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Navigating this crowded market can feel very overwhelming for normal people. You just want clean water for your family. Yet, salesmen keep pushing you to buy features you do not even need. They use complicated scientific words to confuse you. In this kind of situation, professional water filter teams like Filken Malaysia usually play a more neutral, administrative, or supportive role. They will visit your home and check your available cabinet space. They will test your pipe water flow. Then, they recommend a KL water filter 2026 setup that actually works for your daily lifestyle. They do not force the most expensive unit on you blindly. Having an honest consultant helps you avoid very costly mistakes. It ensures your kitchen remains beautiful and highly functional for many years. For more technical details about this filtration system, please visit the official <a href="https://filken.com/">Filken Malaysia Website</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">A Final Thought on the Best KL water filter Journey</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Upgrading your living space is always an exciting and rewarding journey. As a dedicated flooring company, we love seeing a basic house transform into a warm and comfortable home. We really hope our Best KL water filter 2026 guide gives you a much clearer picture of what to look out for. Stop relying on boiling alone. Start looking into proper filtration methods to secure your health. Remember to check your house type and calculate the yearly cartridge replacement costs. Always hire a responsible and experienced installation team. We want you to protect your family from dirty tap water today. Take the right steps now. You will enjoy total peace of mind in your newly renovated dream house.</p>
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
            print("Syncing Yoast UI inputs...")
            for selector, value in [
                ('#yoast-google-preview-title-metabox', seo_title),
                ('#yoast-google-preview-description-metabox', meta_desc),
                ('#focus-keyword-input-metabox', focus_keyword)
            ]:
                try:
                    el = page.locator(selector)
                    if el.is_visible():
                        el.click()
                        page.keyboard.press("Control+A")
                        page.keyboard.press("Backspace")
                        el.fill("")
                        page.keyboard.insert_text(value)
                except Exception as e:
                    print(f"Sync error for {selector}:", e)
                    
            page.wait_for_timeout(1000)
            
            # Save Draft
            print("Saving Draft...")
            save_button = page.locator('button:has-text("保存草稿"), button:has-text("Save draft"), button:has-text("Save Draft"), button.editor-post-save-draft')
            if save_button.is_visible():
                save_button.click()
                page.wait_for_timeout(5000)
                print("Draft saved.")
            
            # Take a screenshot for review
            page.locator('#wpseo_meta').scroll_into_view_if_needed()
            page.wait_for_timeout(2000)
            screenshot_path = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\yoast_result_top50.png"
            page.screenshot(path=screenshot_path, full_page=False)
            print(f"Screenshot saved to: {screenshot_path}")
            
        except Exception as e:
            print("Error during execution:", e)

if __name__ == "__main__":
    run()
