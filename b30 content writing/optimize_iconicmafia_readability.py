import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Image IDs
img1_id = 4859
img1_url = "https://iconicmafia.com/wp-content/uploads/2026/06/filken_gate_pillar_filter.jpg"
img2_id = 4860
img2_url = "https://iconicmafia.com/wp-content/uploads/2026/06/filken_double_outdoor_filters.jpg"
img3_id = 4861
img3_url = "https://iconicmafia.com/wp-content/uploads/2026/06/filken_stainless_filter_wall.jpg"
cover_id = 4862

# Construct optimized body HTML content
body_content = f"""<!-- wp:paragraph -->
<p>Many Malaysians actually get stuck here. Specifically, you wake up early to wash rice and the water looks slightly yellow. Additionally, you boil water for your morning coffee and find thick white scale at the bottom of your expensive kettle. We all face these exact same daily annoyances. For instance, people living in busy Kuala Lumpur or older areas in Penang and Johor Bahru share this common struggle. Consequently, finding the Best KL water filter becomes a highly stressful mission for the whole family. After all, you just want a simple and reliable solution for your kitchen. Yet you get completely confused by all the complicated machines displayed at the shopping mall. As a result, every promoter claims they have the greatest technology in the world. We understand this daily pain perfectly well. Nobody wants to spend their precious weekend worrying about dirty tap water. You want to spend time with your family, not scrubbing white stains off your kitchen sink.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img1_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://iconicmafia.com/edd126/?attachment_id={img1_id}"><img src="{img1_url}" alt="Best KL water filter" class="wp-image-{img1_id}"/></a><figcaption class="wp-element-caption"><a href="https://filken.com/" target="_blank" rel="noopener">Filken</a> Outdoor Master Filter on Gate Pillar.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The Daily Frustrations of Tap Water</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>To summarize, securing clean water at home requires understanding that municipal water treatment is only the first step, as piping contamination often occurs before the water reaches your tap. Let us talk about the real headache hiding in your kitchen. For example, you turn on the bathroom tap to wash your face and the water smells strongly of chlorine. Naturally, you worry about your young kids drinking that water every single day. Therefore, many parents end up buying heavy cartons of mineral water from the supermarket. Ultimately, carrying those heavy water bottles up to your condo is exhausting and terrible for your back.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>In addition, boiling the tap water takes too much time and energy. Besides, boiling only kills the living germs anyway. It never removes the physical rust, fine sand, and weird chemical smells. Therefore, you need a proper physical machine to trap the dirt before it enters your drinking cup. Dealing with water issues should not feel like a second job. As a result, you need a permanent fix that runs quietly in the background.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img2_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://iconicmafia.com/edd126/?attachment_id={img2_id}"><img src="{img2_url}" alt="Best KL water filter" class="wp-image-{img2_id}"/></a><figcaption class="wp-element-caption">Filken Outdoor Master Filters Installation.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why Your Old House Pipes Need the Best KL water filter</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The main issue usually hides right under our busy streets. However, our government treatment plants actually do an excellent job cleaning the water. The big trouble starts when that clean water travels through miles of old rusty pipes. For instance, many mature residential areas use underground pipes that are decades old. These neglected pipes slowly break down and rust over time. Consequently, they release tiny rust particles and brown sand into the community water supply.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>When you hear your neighbors discussing the newest KL water filter 2026 models, they are trying to solve this exact problem. Therefore, you simply cannot escape the dirt inside those aging community pipes. The dirt travels straight into your house water tank. As a result, it settles at the bottom and creates a thick layer of mud over the years. This invisible threat makes a proper home purification system absolutely necessary. In fact, you cannot rely on your eyes to judge water safety. Sometimes the water looks crystal clear but still carries a heavy chemical taste.</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img3_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://iconicmafia.com/edd126/?attachment_id={img3_id}"><img src="{img3_url}" alt="Best KL water filter" class="wp-image-{img3_id}"/></a><figcaption class="wp-element-caption">Filken Outdoor Stainless Steel Filter.</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Solving Water Issues for Condos and Landed Homes</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Your specific house type creates another layer of daily frustration. Imagine living in a nice high rise condo in the city. For starters, you suffer from low water pressure during the evening peak hours when everyone takes a shower. Moreover, your building management also strictly forbids you from installing any big filter tanks outside your door. As a result, you are forced to hunt for a small indoor unit that actually works well. Consequently, you often ask friends for a reliable KL water filter recommend option that fits inside tiny kitchen cabinets. You can click here to check out our <a href="https://iconicmafia.com/edd126/?attachment_id={img1_id}">Filken outdoor water filter installation gallery</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>On the other hand, if you own a landed house in Johor Bahru or Melaka, you have a huge physical advantage. Specifically, you can easily install an outdoor master filter right next to your main water meter. This brilliant setup stops the thick yellow mud from ever entering your indoor pipes. Therefore, it protects your expensive washing machines and bathroom heaters. If you skip the outdoor tank, your white shirts turn yellowish after just a few washes. Consequently, every home requires a specific approach to end these daily annoyances. Buying the wrong system means you waste money and still suffer from the same old water problems.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">The Hidden Pain of Expensive Filter Replacements</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Buying the machine is only the beginning of your financial worries. In addition, we hear so many painful complaints about crazy maintenance fees from local homeowners. For instance, you visit a weekend electrical fair and buy a very cheap machine on impulse. Six months later, the machine starts beeping loudly to warn you. Therefore, you call the service company to change the inside cartridge. The repair guy quotes you a price that almost equals the cost of a brand new machine. As a result, this hidden cost traps many innocent families in a bad contract. People naturally delay changing the cartridge because it is just too expensive. Consequently, the dirty old cartridge then breeds harmful bacteria right inside your kitchen area. You end up drinking water that is much worse than normal tap water. You must always ask about the yearly maintenance fees before paying any deposit.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Therefore, smart buyers calculate the long term costs to avoid this painful trap completely. Ideally, a good system should be easy and affordable to maintain over the next ten years. When looking for the Best KL water filter 2026 option, always ask the salesman about the exact price of the yearly replacement filters. Consequently, you need to know the true cost of ownership.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Getting Real Help for Your Best KL water filter Setup</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Walking into a crowded showroom often feels like entering a noisy battlefield. Indeed, aggressive salesmen surround you immediately from all sides. Usually, they use scary scientific terms to push the most expensive model on you. In fact, they do not care if you only need basic drinking water for two working adults. Instead, they just want to close a big sale and earn their high commission.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>In this kind of situation, professional water filter teams like Filken Malaysia usually play a more neutral, administrative, or supportive role. Specifically, they will visit your house to check your sink space and test your pipe pressure first. They listen closely to your actual daily struggles before suggesting any Best KL water filter 2026 setup. Therefore, having an honest consultant completely removes all the stress from your shopping experience. You get practical advice based on your actual kitchen layout and daily habits. As a result, they handle the messy installation work so you can just relax and enjoy the clean water. Good customer service makes a massive difference when dealing with home appliances. For more detailed instructions on setting up this device, please refer to the official <a href="https://filken.com/">Filken Website</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Final Thoughts on Securing Clean Water Everyday</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Dealing with poor water quality is extremely annoying and totally unnecessary today. After all, you already work hard all day at the office or running your business. You should not have to worry about yellow tap water ruining your evening cooking routine. Therefore, stop buying endless plastic water bottles from the grocery store every weekend. Instead, start looking into a proper home purification system to protect your entire family. Additionally, always measure your kitchen space carefully and calculate the yearly maintenance costs first.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Finally, find a reliable local team to handle the complicated pipe installation work safely. We sincerely hope this honest sharing helps you finally find the Best KL water filter for your home. You deserve to enjoy a clean, safe, and refreshing glass of water anytime you want. Therefore, protect your loved ones today and say goodbye to those frustrating water headaches forever. A good water system is the best investment you can make for your daily health and peace of mind.</p>
<!-- /wp:paragraph -->"""

def run():
    print("Connecting to Chrome to update Gutenberg with readability improvements...")
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
            page.bring_to_front()
            
            # Reset Blocks with new HTML
            page.evaluate("""(html) => {
                const blocks = wp.blocks.parse(html);
                wp.data.dispatch('core/editor').resetBlocks(blocks);
            }""", body_content)
            print("Content blocks updated.")
            page.wait_for_timeout(2000)
            
            # Click Save Draft
            print("Saving Draft...")
            save_button = page.locator('button:has-text("保存草稿"), button:has-text("Save draft"), button:has-text("Save Draft"), button.editor-post-save-draft').first
            save_button.click()
            page.wait_for_timeout(8000)
            print("Draft saved.")
            
            # Take new screenshot of Yoast
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
