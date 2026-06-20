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
site_url = "https://asiatop40.com/wp-admin/"
username = "jwern929@gmail.com"
password = "PFHx1pBpwoD*7#lPthajn!YC"

# Images
images = [
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781271007572.jpg",
        "name": "filken_double_stainless_filters.jpg",
        "title": "Filken 双通道不锈钢户外净水滤水系统",
        "role": "content_1"
    },
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781271007750.jpg",
        "name": "filken_grey_wall_filter.jpg",
        "title": "户外的第一道防线，专业评估安装后的净水系统过滤效果展示",
        "role": "content_2"
    },
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781271007809.jpg",
        "name": "filken_outdoor_filter_light_grey.jpg",
        "title": "依据住宅空间规划 of 专业户外滤水设备布局与安装范例",
        "role": "content_3"
    },
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781271033430.jpg",
        "name": "filken_kitchen_countertop.jpg",
        "title": "Asia Top 40 厨房净水系统设计效果展示",
        "role": "cover"
    }
]

# Post details
title = "别再盲目跟风买贵机器，手把手教你挑选最适合的KL滤水器推荐方案"
excerpt = "想要买净水机却无从下手？这份实用的选购攻略带你避开市面上的推销陷阱，一步步厘清自身需求。透过真实的KL滤水器推荐分享，帮你找到真正适合本地家庭的过滤方案，轻松解决居家水垢与异味烦恼。"
slug = "klwaterfilter2026"

# Yoast details
focus_keyword = "KL滤水器推荐"
seo_title = "KL滤水器推荐 | 新手必看防坑指南：选购全攻略"
meta_desc = "KL滤水器推荐 | 还在纠结要买哪一种净水系统？这篇文章为你整理了一份最实在的选购攻略，教你一步步避开推销陷阱，根据自家房型与生活习惯挑选对的过滤设备，保障全家喝上干净好水。"

def run():
    print("Connecting to Chrome for asiatop40.com automation...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Find the active asiatop40 tab or create one
            page = None
            for p_page in context.pages:
                if "asiatop40.com" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                page = context.new_page()
                print("Created new tab for asiatop40.com")
            
            # Navigate to wp-admin
            print(f"Navigating to: {site_url}")
            try:
                page.goto(site_url, wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print("Initial page load timed out but continuing:", e)
            page.wait_for_timeout(3000)
            
            # Check if redirected to login page
            if "wp-login.php" in page.url:
                print("Logging in to asiatop40.com...")
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
                
            print(f"Navigating to new post page...")
            try:
                page.goto("https://asiatop40.com/wp-admin/post-new.php", wait_until="domcontentloaded", timeout=45000)
            except Exception as e:
                print("New post page load timed out but continuing:", e)
                
            print("Waiting for Gutenberg to load...")
            page.wait_for_function("() => window.wp && window.wp.data && window.wp.data.dispatch", timeout=30000)
            print("Gutenberg loaded.")
            
            # Upload images via JS Fetch
            print("Uploading images to asiatop40.com media library...")
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
                                alt_text: "KL滤水器推荐",
                                description: "KL滤水器推荐"
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
                
            # Build body HTML content with uploaded IDs
            img1_id = uploaded_images["content_1"]["id"]
            img1_url = uploaded_images["content_1"]["url"]
            img2_id = uploaded_images["content_2"]["id"]
            img2_url = uploaded_images["content_2"]["url"]
            img3_id = uploaded_images["content_3"]["id"]
            img3_url = uploaded_images["content_3"]["url"]
            cover_id = uploaded_images["cover"]["id"]
            
            body_content = f"""<!-- wp:paragraph -->
<p>KL滤水器推荐 | 很多住在巴生谷一带的朋友，最近都在烦恼到底该怎么挑选适合家里的净水设备。每次打开社交媒体，各种五花八门的牌子和广告一直跳出来，看多了反而越看越懵，完全不知道该怎么选。其实，买净水设备最怕就是花大钱买错东西。为了让大家少走弯路，我们整理了一份非常实在的KL滤水器推荐攻略。简单说，这篇文章不会跟你讲一堆深奥难懂的科学原理，而是从我们每天煮饭、泡茶、喝水的生活习惯出发，一步步带你厘清到底该怎样根据自己的情况，去挑一台真正好用的净水机。</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>我们都知道马来西亚各地的水质情况其实不太一样，就算同样是在雪隆区，不同花园或住宅区的水管老化程度也有很大的差别。很多从新山或槟城搬来吉隆坡打拼的上班族，或者刚在本地买房的小家庭，常常会发现家里的白钢水槽总是有一层黄黄的水垢，或者偶尔还会闻到轻微的漂白水味。遇到这种情况，大家的直觉反应可能就是赶紧去买个便宜的过滤网装在水龙头上。不过说真的，那种简易的过滤方式只能算是治标不治本，要想让全家人每天都安心喝水，还是得稍微花点心思，系统性地规划一下居家的净水方案。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">认清自家的水质痛点与日常用水习惯</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>很多人都会在刚好要装修新房子的时候，顺便把净水系统一起搞定，这确实是个非常好的时机。但在盲目搜寻吉隆坡滤水器之前，你应该先坐下来问问自己，平时家里到底有几口人需要喝水？大家是习惯喝室温水，还是长辈经常需要热水泡茶，亦或是半夜需要起来给小宝宝冲泡奶粉？如果你家里刚好有婴儿，那带有精准温度控制的智能机器肯定能帮你省下很多苦等热水变凉的折磨时间。另外，你也要多留意一下社区平时的自来水有没有明显的异味，或者偶尔遇到修水管制水后恢复供水时，那股黄泥水的状况严不严重。只有事先摸清楚这些日常生活的细节，你才不会在销售员面前乱了阵脚，买了一大堆其实平时根本用不到的复杂功能。关于这款产品的更多实机安装图，可以点击查看我们的 <a href="https://asiatop40.com/?attachment_id={img1_id}">Filken 户外滤水器安装图集</a>。</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img1_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://asiatop40.com/?attachment_id={img1_id}"><img src="{img1_url}" alt="KL滤水器推荐" class="wp-image-{img1_id}"/></a><figcaption class="wp-element-caption"><a href="https://filken.com/" target="_blank" rel="noopener">Filken</a> 双通道不锈钢户外净水滤水系统。</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">为什么大马家庭的净水系统列表中总有不同的技术？</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>相反的，UF 技术依靠的是水管本身的水压来进行物理过滤，能够保留水中的微量元素，出来的水喝起来也比较顺口。对于大多数住在市区、水质没有严重重金属污染的普通家庭来说，这种技术其实已经非常足够了。所以，不要盲目去追随别人推荐的吉隆坡滤水器，而是要先停下来想想，你到底想解决家里水槽上的水垢问题，还是想追求极致的纯净水体验。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">房型与水压决定你的家庭滤水系统怎么装</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>买净水器不是只要机器好就万事大吉，你的居住环境其实有着绝对的决定权。举个很实际的例子，如果你住在管理森严的高级 Condo，不仅厨房的台面空间有限，管理层通常也绝不允许你在屋外的走廊安装任何大型设备。这时候，你就必须把目光锁定在那些体积小巧、可以直接隐藏在洗碗槽下方或者不占空间的款式，只要管线拉得漂亮，一样能达到非常好的净化效果。</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img2_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://asiatop40.com/?attachment_id={img2_id}"><img src="{img2_url}" alt="KL滤水器推荐" class="wp-image-{img2_id}"/></a><figcaption class="wp-element-caption">户外的第一道防线，专业评估安装后的净水系统过滤效果展示。</figcaption></figure>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p>而如果你住在宽敞的排屋或者半独立洋房，恭喜你，你的选择就多得多了。很多懂行的人都会采用“双管齐下”的策略，也就是在户外的总水表旁边先安装一个大型的砂石过滤器，先把粗大的泥沙和铁锈挡在屋外，保护家里的洗衣机和热水器不受黄水侵害；接着在厨房再装一台供人喝的直饮机。简单说，顺着自家房型的物理条件去规划，才能发挥出设备的最佳效能。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">别忽略滤芯更换这笔长期的隐形开销</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>买净水设备最容易掉进的陷阱之一，就是大家往往只看眼前的机器标价，却完全忘记去计算后期的保养费用。市面上有很多KL 滤水器在做大型促销时，整台机器卖得特别便宜，感觉真的买到赚到。但是等到半年或一年后，机器提示需要更换内部滤芯时，你才会惊讶地发现原厂专属滤芯的价格竟然高得吓人。所以，当你在做功课挑选过滤设备时，一定要非常直接地问清楚，每年换滤芯的总费用大概是多少，是不是每次都需要支付额外的人工费找专人上门来换，还是它的设计非常人性化，简单到你可以自己动手去完成。只有把这笔每年必花的长期账目算清楚，你才能真正买得毫无压力，不然以后因为心疼滤芯钱而一直拖延更换，反而会喝进更多细菌，得不偿失。</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{img3_id},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="https://asiatop40.com/?attachment_id={img3_id}"><img src="{img3_url}" alt="KL滤水器推荐" class="wp-image-{img3_id}"/></a><figcaption class="wp-element-caption">依据住宅空间规划的专业户外滤水设备布局与安装范例。</figcaption></figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading">避开硬核推销，专业评估才是定海神针</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>当你搞清楚了自己的核心需求和家庭预算后，最后一步也是最关键的一步，就是找一家靠谱的本地商家来进行实地的现场评估。特别是很多房龄较高的老旧公寓，水压通常都不太稳定，有时候高高兴兴买了一台高级的机器回去，接上去却发现水流小得可怜，连平时洗菜洗米都嫌慢。一个专业的团队绝对不只是为了卖东西给你，他们更应该在安装前亲自帮你测试家里的实际水压，看看你的橱柜内部格局到底适不适合走线。在这种情况下，像 <a href="https://filken.com/" target="_blank" rel="noopener">Filken</a> 这样的专业滤水团队，通常会扮演较中立、行政或协助的角色。他们会根据你的居住环境、厨房条件和真实预算给出务实的配置建议，而不是不管三七二十一就拼命推销利润最高的型号给你。这种踏实且负责任的协助态度，才是保障以后机器不出问题的关键所在。如果您想了解更多关于这款设备的技术参数，可以访问 <a href="https://filken.com/">Filken 官方网站</a> 进行查询。</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">总结：看懂核心知识，轻松掌握 KL滤水器推荐 的精髓</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>买一台适合的净水机，其实就像是为家里挑选一个陪伴全家人的健康好帮手，这件事情真的急不得。只要你照着这篇攻略 of 思路，先彻底搞懂自己和家人的用水习惯，确认好住宅类型的物理限制，再把未来的耗材保养费用老老实实地算进预算里，最后找个专业且愿意帮忙评估的售后团队协助把关。只要踏踏实实地做到这几个步骤，你就能轻轻松松避开市面上的选购雷区。希望这份扎实且步骤分明的KL滤水器推荐内容，能真正帮到正在苦恼挑选设备的你，让你的每一分钱都能花在刀刃上，往后的每一天都能安心、放心地喝上一口干净清甜的好水。</p>
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
            
            # Publish directly
            print("Publishing post directly...")
            publish_toggle = page.locator('button:has-text("Publish"), button:has-text("发布"), button.editor-post-publish-panel__toggle').first
            publish_toggle.scroll_into_view_if_needed()
            publish_toggle.click()
            page.wait_for_timeout(2000)
            
            confirm_publish = page.locator('.editor-post-publish-panel__header button:has-text("Publish"), .editor-post-publish-panel__header button:has-text("发布"), button.editor-post-publish-button').first
            confirm_publish.click()
            
            print("Waiting for publish process to complete...")
            page.wait_for_timeout(6000)
            
            post_url = page.evaluate("() => wp.data.select('core/editor').getPermalink()")
            print(f"SUCCESS! Post published successfully.")
            print(f"Published URL: {post_url}")
            
        except Exception as e:
            print("Error during execution:", e)

if __name__ == "__main__":
    run()
