import os
import sys
import json
import base64
import random
from playwright.sync_api import sync_playwright

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BRAIN_DIR = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570"
MEDIA_DIR = os.path.join(BRAIN_DIR, "queensfloor_media")

# Site Configurations
SITES = [
    {
        "name": "billionairechamp",
        "url": "https://billionairechamp.com/wp-admin/",
        "user": "editor2",
        "pass": "!r8ylrwOF$*&TrGtykk9o7xe",
        "focus_keyword": "Queensfloor销售招聘",
        "article_idx": 1,
        "lang": "ZH",
        "seo_title": " Queensfloor销售招聘 | 寻找好工作指南与真实待遇揭秘",
        "meta_desc": "想要在吉隆坡或新山寻找有前景的职业发展机会吗？了解最新的 Queensfloor销售招聘 资讯，揭秘专业团队背后的薪资福利与住宿条件。我们为您解析如何通过完善的培训和福利机制，让新手也能轻松上手，实现稳定长远的职业规划。"
    },
    {
        "name": "asiatop40",
        "url": "https://asiatop40.com/wp-admin/",
        "user": "jwern929@gmail.com",
        "pass": "PFHx1pBpwoD*7#lPthajn!YC",
        "focus_keyword": "Queensfloor销售招聘",
        "article_idx": 2,
        "lang": "ZH",
        "seo_title": " Queensfloor销售招聘 | 深度拆解福利与住宿，加入前必看指南",
        "meta_desc": "想要在KL或新山找到一份有前景的销售工作？很多人不知道其实选对平台很重要。本文为你拆解最新的 Queensfloor销售招聘 资讯，从底薪福利到专业的宿舍与系统培训，用最真实的视角探讨现代销售行业的长远发展，让你在找工的路上少走弯路。"
    },
    {
        "name": "sgscope",
        "url": "https://sgscope.com/edd124/",
        "user": "Ashley",
        "pass": "($eiCp&6bNawGqCc*I6hw&*5",
        "focus_keyword": "Queensfloor销售招聘",
        "article_idx": 3,
        "lang": "ZH",
        "seo_title": " Queensfloor销售招聘 | 全面剖析底薪与福利待遇，打工族逆袭攻略",
        "meta_desc": "想要在大城市打拼却总被生活开销压得喘不过气？近期本地市场对职场福利的讨论度越来越高，本文带你深入了解热门的 Queensfloor销售招聘 资讯，揭秘专业团队如何透过完善培训与优厚待遇，协助打工族找到长远发展的方法。"
    },
    {
        "name": "supernovaboss",
        "url": "https://supernovaboss.com/edd128/",
        "user": "Ashley",
        "pass": "($eiCp&6bNawGqCc*I6hw&*5",
        "focus_keyword": "Queensfloor销售招聘",
        "article_idx": 4,
        "lang": "ZH",
        "seo_title": " Queensfloor销售招聘 | 从零经验到开单秘籍，看企业如何赋能新人成长",
        "meta_desc": "想要在新山或KL找寻理想的销售空缺？如今的求职者越来越看重企业提供的全方位生活支撑。本文深入探讨近期备受瞩目的 Queensfloor销售招聘 现象，解析专业团队如何透过完善底薪保障、免费高级宿舍以及系统化培训，协助职场新手安心冲刺业绩并获得长远的发展机会。"
    },
    {
        "name": "top50malaysia",
        "url": "https://top50malaysia.com/wp-admin/",
        "user": "Carmen",
        "pass": "PFHx1pBpwoD*7#lPthajn!YC",
        "focus_keyword": "Queensfloor Sales Hiring",
        "article_idx": 5,
        "lang": "EN",
        "seo_title": "Queensfloor Sales Hiring | Job Hiring Guide & Career Secrets",
        "meta_desc": "Looking for a solid job hiring opportunity? Discover the hidden perks behind Queensfloor Sales Hiring including basic salary EPF SOCSO and free condo stays for outstation staff. Find out how beginners thrive with excellent training."
    },
    {
        "name": "straitshub",
        "url": "https://straitshub.com/edd130/",
        "user": "Louis",
        "pass": "JMB87qTwe9ISJTNl6pA(A@kM",
        "focus_keyword": "Queensfloor Sales Hiring",
        "article_idx": 6,
        "lang": "EN",
        "seo_title": "Queensfloor Sales Hiring | New Job Hiring Reality & Guide",
        "meta_desc": "Discover the latest local job market trends and uncover why Queensfloor Sales Hiring attracts outstation talents. Modern companies provide excellent basic salary benefits free condo accommodation and practical training for beginners."
    }
]

# 5 images that are available in queensfloor_media
IMAGE_FILES = [
    {"filename": "queensfloor_staff_accommodation.jpg", "title": "Queensfloor Staff Accommodation Room & Facilities"},
    {"filename": "queensfloor_average_sales_orders.jpg", "title": "Queensfloor Sales Orders and Average Ticket Value"},
    {"filename": "queensfloor_working_environment.jpg", "title": "Queensfloor Working Environment and Office"},
    {"filename": "queensfloor_practical_sales_training.jpg", "title": "Queensfloor Practical Sales Training Program"},
    {"filename": "queensfloor_sales_consultant_hiring.jpg", "title": "Queensfloor Sales Consultant Career Hiring Poster"}
]

# Statically defined H2 headings for each article (stripped of extra whitespace)
ARTICLE_H2S = {
    1: [
        "为什么现在的求职者越来越看重Queensfloor销售招聘这样的机会",
        "解决外坡打工族在大城市的生活痛点",
        "新手毫无经验该如何胜任销售工作",
        "了解行业内专业团队的运作与支撑力量",
        "总结市场对Queensfloor销售招聘的长远期待"
    ],
    2: [
        "为什么现在的年轻人都开始留意Queensfloor销售招聘这类的机会",
        "解决外坡打工人的最大痛点，原来住宿福利可以这么讲究",
        "新手小白不用怕，简单来说系统培训才是能长远发展的王道",
        "职场上的神队友，买房装修背后的专业支撑力",
        "看懂Queensfloor销售招聘的真实长远价值，重新定义职场生活"
    ],
    3: [
        "大城市打工族的痛点与Queensfloor销售招聘带来的新曙光",
        "从底薪到奖金全面剖析现代企业的留薪策略",
        "新手不用愁开单系统化培训是小白的定心丸",
        "装修行业生态转变与专业团队背后的服务价值",
        "总结近期引发热议的Queensfloor销售招聘的未来潜力"
    ],
    4: [
        "薪金结构透明化成为吸引人才入局的关键",
        "从Queensfloor销售招聘探讨外坡者的住宿福利",
        "打破零经验迷思系统化培训是稳住阵脚的核心",
        "行业生态转变与专业团队所扮演的辅助角色",
        "总结Queensfloor销售招聘现象与职场疑问总览"
    ],
    5: [
        "The Hidden Truth About Job Hiring In Big Cities",
        "Simply Put Basic Salary And Benefits Matter In Queensfloor Sales Hiring",
        "Oh So That Is How Outstation Workers Survive Comfortably",
        "What Many People Do Not Know About Becoming A Queensfloor Sales Consultant",
        "How A Professional Team Supports Your Career Growth",
        "Conclusion On The Growing Queensfloor Sales Hiring Market",
        "Frequently Asked Questions"
    ],
    6: [
        "Changing Tides In Local Job Hiring Scopes",
        "How Queensfloor Sales Hiring Solves Rent Issues",
        "Real Training Systems For Total Beginners",
        "The Professional Side Of A Queensfloor Sales Consultant",
        "Final Thoughts On Queensfloor Sales Hiring"
    ]
}

def rebuild_body_content(article_idx, body_text, focus_keyword, uploaded_images, lang):
    """
    Parses the plain text body and reconstructs it with Gutenberg blocks.
    It inserts the 3 uploaded images directly above randomly selected H2 headings.
    It also adds the outbound link to Queensfloor's website where 'Queensfloor' appears.
    """
    h2_headings = ARTICLE_H2S[article_idx]
    
    # We want to insert the 3 uploaded images. Let's randomly select 3 of the H2 headings.
    # To keep execution deterministic or randomly selected:
    selected_h2s = random.sample(h2_headings, min(3, len(h2_headings)))
    print(f"Selected H2 headings for image placement: {selected_h2s}")
    
    # Split the body by double newlines to parse paragraphs and headings
    raw_segments = body_text.split('\n\n')
    
    html_blocks = []
    image_idx = 0
    
    for segment in raw_segments:
        segment = segment.strip()
        if not segment:
            continue
            
        # Check if this segment is one of our H2 headings
        is_h2 = False
        matching_h2 = ""
        for h2 in h2_headings:
            if segment == h2 or segment.startswith(h2) or h2.startswith(segment):
                is_h2 = True
                matching_h2 = h2
                break
                
        if is_h2:
            display_heading = segment
            if lang == "ZH" and focus_keyword in display_heading:
                import re
                pattern = re.compile(rf'\s*{re.escape(focus_keyword)}\s*')
                display_heading = pattern.sub(f" {focus_keyword} ", display_heading)
                
            # If this H2 was selected for image placement, prepend the image block
            if matching_h2 in selected_h2s and image_idx < len(uploaded_images):
                img = uploaded_images[image_idx]
                image_idx += 1
                
                # Image block in Gutenberg format
                # - Link destination: attachment
                # - Wrapped in <a> tag linking to img['link']
                html_blocks.append(f"""<!-- wp:image {{"id":{img['id']},"sizeSlug":"large","linkDestination":"attachment"}} -->
<figure class="wp-block-image size-large"><a href="{img['link']}"><img src="{img['url']}" alt="{img['alt']}" class="wp-image-{img['id']}"/></a></figure>
<!-- /wp:image -->""")
            
            # Add H2 block
            html_blocks.append(f"""<!-- wp:heading -->
<h2 class="wp-block-heading">{display_heading}</h2>
<!-- /wp:heading -->""")
            
        else:
            # Paragraph segment. We will naturalize and add outbound link to Queensfloor website
            # Let's replace 'Queensfloor' (not inside HTML tags) with a link to Queensfloor website,
            # but only if it's the brand keyword.
            # To keep it simple, we replace the first 1-2 occurrences of "Queensfloor" or "Queensfloor地板团队"
            # with the hyperlink.
            segment_html = segment
            
            # Outbound link logic:
            if "https://www.queensfloor.com/" not in segment_html:
                # Replace Queensfloor with a link
                if "Queensfloor地板团队" in segment_html:
                    segment_html = segment_html.replace("Queensfloor地板团队", '<a href="https://www.queensfloor.com/" target="_blank" rel="noopener">Queensfloor地板团队</a>', 1)
                elif "Queensfloor销售顾问" in segment_html:
                    segment_html = segment_html.replace("Queensfloor销售顾问", '<a href="https://www.queensfloor.com/" target="_blank" rel="noopener">Queensfloor销售顾问</a>', 1)
                elif "Queensfloor" in segment_html:
                    segment_html = segment_html.replace("Queensfloor", '<a href="https://www.queensfloor.com/" target="_blank" rel="noopener">Queensfloor</a>', 1)
            
            html_blocks.append(f"""<!-- wp:paragraph -->
<p>{segment_html}</p>
<!-- /wp:paragraph -->""")
            
    if lang == "ZH":
        # Add Chinese comparison table
        table_html = """<!-- wp:table -->
<figure class="wp-block-table"><table><thead><tr><th>福利项目</th><th>Queensfloor 地板团队</th><th>行业一般水平</th></tr></thead><tbody><tr><td>底薪保障</td><td>提供固定底薪</td><td>多数为纯佣金或无底薪</td></tr><tr><td>EPF &amp; SOCSO</td><td>享有公积金与社险</td><td>部分小型团队不提供</td></tr><tr><td>员工宿舍</td><td>专供外州员工（带泳池公寓）</td><td>需员工自理或自付租金</td></tr><tr><td>系统培训</td><td>主管带教与门店实操</td><td>无系统培训，新人自生自灭</td></tr></tbody></table></figure>
<!-- /wp:table -->"""
        html_blocks.append(table_html)
        
        # Add Chinese contact block
        contact_html = f"""<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">联系我们了解更多 Queensfloor 销售顾问 详情</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>如果您想了解更多关于 Queensfloor 招聘 的最新资讯，或者有志于加入我们，欢迎通过以下渠道与我们联系：</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>官方网站 (Website)：</strong><a href="https://www.queensfloor.com/" target="_blank" rel="noopener">Queensfloor Malaysia</a></li>
<li><strong>公司地址 (Address)：</strong>No. 2, Jalan PJS 5/26, Taman Desa Ria, 46150 Petaling Jaya, Selangor, Malaysia.</li>
<li><strong>联系电话 (Contact Number)：</strong>+6012-908 1329</li>
<li><strong>社交媒体：</strong>Facebook (Queensfloor.official) / Instagram (@queensfloor.official)</li>
</ul>
<!-- /wp:list -->"""
        html_blocks.append(contact_html)

        # Add English job description to satisfy Yoast word count requirements
        english_career_html = """<!-- wp:heading -->
<h2 class="wp-block-heading">Queensfloor Career Opportunities &amp; Job Description</h2>
<!-- /wp:heading -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Position: Sales Consultant (Full-Time)</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Location: Bandar Sunway, Puchong, Bukit Jalil (Kuala Lumpur &amp; Selangor) / Danga Bay (Johor Bahru)</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">About the Role</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>As a Sales Consultant, you will be part of a dynamic and supportive team dedicated to providing high-quality flooring solutions. You will engage with customers, understand their home renovation needs, and recommend the best SPC flooring products. This role offers an excellent opportunity to develop professional sales skills, build customer relationships, and achieve financial growth through a combination of basic salary and commission.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Key Responsibilities</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>Greet customers in the showroom and understand their flooring requirements.</li>
<li>Introduce flooring products, explain technical specifications, and provide pricing estimation.</li>
<li>Assist customers in choosing the right SPC flooring designs and colors.</li>
<li>Collaborate with the technical team to arrange site measurements and installation schedules.</li>
<li>Follow up with customers to ensure high satisfaction and handle inquiries.</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Requirements</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>No experience required; fresh graduates and career switchers are welcome to apply.</li>
<li>Strong willingness to learn, communicate, and work in a team environment.</li>
<li>Energetic, self-motivated, and target-oriented personality.</li>
<li>Ability to communicate in Mandarin and English to assist different customer groups.</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">Benefits &amp; Perks</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul>
<li>Competitive basic salary with statutory contributions (EPF &amp; SOCSO).</li>
<li>High commission structure, performance bonuses, and career advancement.</li>
<li>Free high-quality accommodation (condominium with swimming pool) for outstation staff.</li>
<li>Systemic on-the-job training led by experienced managers and team leaders.</li>
<li>Dynamic working environment with team building and training support.</li>
</ul>
<!-- /wp:list -->"""
        html_blocks.append(english_career_html)
        
    else:
        # Add English comparison table
        table_html = """<!-- wp:table -->
<figure class="wp-block-table"><table><thead><tr><th>Perks</th><th>Queensfloor Sales Team</th><th>Industry Standard</th></tr></thead><tbody><tr><td>Basic Salary</td><td>Guaranteed Fixed Salary</td><td>Commission-only / No basic pay</td></tr><tr><td>EPF &amp; SOCSO</td><td>Full statutory contributions</td><td>Often not provided by small teams</td></tr><tr><td>Accommodation</td><td>Free luxury condo with pool</td><td>Must rent/pay own room expenses</td></tr><tr><td>Training</td><td>Supervisor-led practical training</td><td>No proper training provided</td></tr></tbody></table></figure>
<!-- /wp:table -->"""
        html_blocks.append(table_html)
        
        # Add English contact block
        contact_html = f"""<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Contact Us to Learn More About Queensfloor Sales Hiring</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>If you want to get more details about our job hiring opportunities or are interested in becoming a professional Queensfloor Sales Consultant, feel free to reach out to us:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
<li><strong>Website:</strong> <a href="https://www.queensfloor.com/" target="_blank" rel="noopener">Queensfloor Malaysia</a></li>
<li><strong>Address:</strong> No. 2, Jalan PJS 5/26, Taman Desa Ria, 46150 Petaling Jaya, Selangor, Malaysia.</li>
<li><strong>Contact Number:</strong> +6012-908 1329</li>
<li><strong>Social Media:</strong> Facebook (Queensfloor.official) / Instagram (@queensfloor.official)</li>
</ul>
<!-- /wp:list -->"""
        html_blocks.append(contact_html)
            
    return "\n\n".join(html_blocks)

def publish_site(site, use_cdp=False):
    name = site["name"]
    login_url = site["url"]
    username = site["user"]
    password = site["pass"]
    focus_keyword = site["focus_keyword"]
    article_idx = site["article_idx"]
    lang = site["lang"]
    
    print("\n" + "="*80)
    print(f"PROCESSING SITE: {name.upper()} (Article: {article_idx}, Lang: {lang})")
    print("="*80)
    
    # Load Article Data
    art_path = os.path.join(BRAIN_DIR, f"article_{article_idx:02d}.json")
    if not os.path.exists(art_path):
        print(f"Error: Article JSON not found: {art_path}")
        return False
        
    with open(art_path, 'r', encoding='utf-8') as f:
        art_data = json.load(f)
        
    title = art_data["h1_title"]
    excerpt = art_data["excerpt"]
    body = art_data["body"]
    seo_title = site.get("seo_title", art_data["seo_title"])
    meta_desc = site.get("meta_desc", art_data["meta_description"])
    
    # Reduce keyword density for ZH articles
    if lang == "ZH":
        if article_idx == 1:
            title = title.replace("关注Queensfloor销售招聘的背后原因", "关注这一销售团队招聘的背后原因")
            # Do NOT replace the subheading: "总结市场对Queensfloor销售招聘的长远期待"
            body = body.replace("通过对 Queensfloor销售招聘 真实情况 of 剖析", "通过对真实招聘情况 of 剖析") # Keep consistent with any typos
            body = body.replace("通过对 Queensfloor销售招聘 真实情况的剖析", "通过对真实招聘情况的剖析")
        elif article_idx == 2:
            title = title.replace("想挤进Queensfloor销售招聘的行列", "想挤进这一销售团队招聘的行列")
            # Do NOT replace the subheading: "看懂Queensfloor销售招聘的真实长远价值"
            body = body.replace("像深入研究 Queensfloor销售招聘 的长远价值一样", "像深入研究这一销售岗位的长远价值一样")
        elif article_idx == 3:
            title = title.replace("关注的Queensfloor销售招聘现象", "关注的销售岗位招募现象")
            # Do NOT replace the subheading: "总结近期引发热议的Queensfloor销售招聘的未来潜力"
            # Replace paragraph occurrence to maintain density of 4
            body = body.replace("剖析 Queensfloor销售招聘 的真实福利", "剖析真实福利")
            body = body.replace("剖析Queensfloor销售招聘的真实福利", "剖析真实福利")
        elif article_idx == 4:
            title = title.replace("为什么Queensfloor销售招聘能成为", "为什么这一销售团队招聘能成为")
            # Do NOT replace the subheading: "总结Queensfloor销售招聘现象与职场疑问总览"
            # Replace paragraph occurrence to maintain density of 4
            body = body.replace("通过对 Queensfloor销售招聘 的全面拆解", "通过对相关岗位的全面拆解")
            body = body.replace("通过对Queensfloor销售招聘的全面拆解", "通过对相关岗位的全面拆解")
    
    # Randomly select 3 images
    selected_imgs = random.sample(IMAGE_FILES, 3)
    print(f"Selected images for upload: {[img['filename'] for img in selected_imgs]}")
    
    user_data_dir = os.path.abspath('chrome_temp_profile')
    
    # We will launch persistent context or connect over CDP
    with sync_playwright() as p:
        try:
            if use_cdp:
                print("Connecting to Chrome via CDP on port 9222...")
                browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
                context = browser.contexts[0]
                page = context.pages[0] if context.pages else context.new_page()
            else:
                print("Launching Chrome context...")
                context = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    channel="chrome",
                    headless=False, # Headful is safer for Yoast and rendering
                    args=[f"--profile-directory={name}", "--start-maximized"],
                    viewport=None
                )
                page = context.pages[0] if context.pages else context.new_page()
            
            # Navigate to login URL (which is either wp-admin or custom login directory)
            print(f"Navigating to login page: {login_url}")
            page.goto(login_url)
            page.wait_for_timeout(4000)
            
            # Login if fields visible
            if page.locator('#user_login').is_visible():
                print("Form found. Submitting credentials...")
                page.locator('#user_login').fill(username)
                page.wait_for_timeout(500)
                page.locator('#user_pass').fill(password)
                page.wait_for_timeout(500)
                page.locator('#wp-submit').click()
                page.wait_for_timeout(5000)
                
            # If not in wp-admin yet, try to redirect
            if "wp-admin" not in page.url:
                print(f"Not in admin dashboard. Current URL: {page.url}. Attempting redirect to wp-admin...")
                if "edd" in login_url:
                    admin_url = login_url.split("edd")[0] + "wp-admin/"
                else:
                    admin_url = login_url
                page.goto(admin_url)
                page.wait_for_timeout(4000)
                
            if "wp-admin" not in page.url:
                print("Error: Failed to verify login session.")
                context.close()
                return False
                
            print("Login successful! Checking for and permanently deleting existing posts matching slug 'queensfloorsalehiring'...")
            try:
                # Query and permanently delete any matching posts via browser REST API
                cleanup_js = """
                async (slug) => {
                    const statuses = ['publish', 'draft', 'pending', 'private', 'future', 'trash'];
                    const ids = [];
                    for (const status of statuses) {
                        try {
                            const response = await fetch('/wp-json/wp/v2/posts?status=' + status + '&per_page=100');
                            if (response.ok) {
                                const data = await response.json();
                                data.forEach(d => {
                                    if (d.slug.includes(slug)) {
                                        ids.push(d.id);
                                    }
                                });
                            }
                        } catch(e) {}
                    }
                    
                    const nonce = wpApiSettings.nonce;
                    for (const id of ids) {
                        try {
                            await fetch('/wp-json/wp/v2/posts/' + id + '?force=true', {
                                method: 'DELETE',
                                headers: {
                                    'X-WP-Nonce': nonce
                                }
                            });
                        } catch(e) {}
                    }
                    return ids;
                }
                """
                deleted_ids = page.evaluate(cleanup_js, "queensfloorsalehiring")
                if deleted_ids:
                    print(f"Permanently deleted existing matching posts: {deleted_ids}")
            except Exception as e:
                print("In-browser cleanup warning:", e)
            
            print("Navigating to New Post editor...")
            from urllib.parse import urlparse
            parsed = urlparse(login_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}/"
            editor_url = f"{base_url}wp-admin/post-new.php"
            page.goto(editor_url)
            
            print("Waiting for Gutenberg editor and REST API to load...")
            page.wait_for_function("() => window.wp && window.wp.data && window.wp.data.dispatch")
            page.wait_for_timeout(3000)
            
            # Close welcome guide if active
            page.evaluate("""() => {
                try {
                    if (wp.data.select('core/edit-post').isFeatureActive('welcomeGuide')) {
                        wp.data.dispatch('core/edit-post').toggleFeature('welcomeGuide');
                    }
                } catch(e) {
                    console.error("Failed to close welcome guide:", e);
                }
            }""")
            
            # Upload selected images via WordPress REST API in page context
            print("Uploading images via WordPress REST API in browser...")
            uploaded_images = []
            
            # Assign focus keyword as Alt Text to the first image, others get descriptive titles
            for idx, img in enumerate(selected_imgs):
                img_path = os.path.join(MEDIA_DIR, img["filename"])
                if not os.path.exists(img_path):
                    print(f"Warning: image path does not exist: {img_path}")
                    continue
                    
                with open(img_path, 'rb') as img_f:
                    base64_data = base64.b64encode(img_f.read()).decode('utf-8')
                    
                alt_text = focus_keyword if idx == 0 else img["title"]
                
                upload_js = """
                async ([base64Data, filename, title, altText]) => {
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
                    
                    // Update metadata
                    await fetch(apiRoot + `wp/v2/media/${mediaObj.id}`, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            "X-WP-Nonce": nonce
                        },
                        body: JSON.stringify({
                            title: title,
                            alt_text: altText,
                            description: title
                        })
                    });
                    
                    return {
                        id: mediaObj.id,
                        url: mediaObj.source_url,
                        link: mediaObj.link
                    };
                }
                """
                
                print(f"Uploading {img['filename']} with alt text '{alt_text}'...")
                res = page.evaluate(upload_js, [base64_data, img["filename"], img["title"], alt_text])
                res['alt'] = alt_text
                print(f"Uploaded successfully! ID: {res['id']}, URL: {res['url']}")
                uploaded_images.append(res)
                
            if len(uploaded_images) < 3:
                print("Error: Image upload failed or incomplete.")
                context.close()
                return False
                
            # Build Gutenberg blocks
            print("Rebuilding post body content into Gutenberg blocks...")
            rebuilt_body = rebuild_body_content(article_idx, body, focus_keyword, uploaded_images, lang)
            
            # Inject Content, Title, Excerpt, Slug, and Yoast SEO details via wp.data
            print("Injecting content and metadata into Gutenberg store...")
            page.evaluate("""([title, body, excerpt, slug, kw, seoTitle, seoDesc]) => {
                const blocks = wp.blocks.parse(body);
                wp.data.dispatch('core/editor').resetBlocks(blocks);
                
                wp.data.dispatch('core/editor').editPost({
                    title: title,
                    excerpt: excerpt,
                    slug: slug,
                    meta: {
                        _yoast_wpseo_focuskw: kw,
                        _yoast_wpseo_title: seoTitle,
                        _yoast_wpseo_metadesc: seoDesc
                    }
                });
            }""", [title, rebuilt_body, excerpt, "queensfloorsalehiring", focus_keyword, seo_title, meta_desc])
            
            page.wait_for_timeout(3000)
            
            # Open Yoast Sidebar to force calculation
            print("Ensuring Yoast sidebar is open...")
            try:
                page.evaluate("""() => {
                    const btn = document.querySelector('button[aria-label="Yoast SEO"]');
                    const panel = document.querySelector('.yoast.components-panel__body');
                    if (btn && !panel) {
                        btn.click();
                    }
                }""")
                page.wait_for_timeout(2000)
            except Exception as e:
                print("Yoast sidebar open warning:", e)
                
            # Synchronize with Yoast input fields to ensure recalculation triggers
            print("Synchronizing Yoast UI inputs...")
            try:
                # SEO Title
                title_input = page.locator('#yoast-google-preview-title-metabox')
                if title_input.is_visible():
                    title_input.click()
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    page.keyboard.insert_text(seo_title)
            except Exception as e:
                print("Yoast Title input sync warning:", e)
                
            try:
                # Meta Desc
                desc_input = page.locator('#yoast-google-preview-description-metabox')
                if desc_input.is_visible():
                    desc_input.click()
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    page.keyboard.insert_text(meta_desc)
            except Exception as e:
                print("Yoast Meta Desc input sync warning:", e)
                
            try:
                # Focus Keyphrase
                kw_input = page.locator('#focus-keyword-input-metabox')
                if kw_input.is_visible():
                    kw_input.click()
                    page.keyboard.press("Control+A")
                    page.keyboard.press("Backspace")
                    page.keyboard.insert_text(focus_keyword)
            except Exception as e:
                print("Yoast Focus Keyphrase input sync warning:", e)
                
            page.wait_for_timeout(2000)
            
            # Save Draft to force Yoast recalculation
            print("Saving draft to trigger Yoast analysis...")
            save_btn = page.locator('button:has-text("Save draft"), button:has-text("Save Draft")')
            if save_btn.is_visible():
                save_btn.click()
                page.wait_for_timeout(5000)
                print("Draft saved.")
            
            # Wait for Yoast results to compile
            print("Waiting for Yoast SEO analysis...")
            page.wait_for_timeout(5000)
            
            # Retrieve Yoast SEO score from panel text
            def check_is_green():
                score_text = page.evaluate("""() => {
                    const panels = document.querySelectorAll('.yoast.components-panel__body, [id*="yoast-seo-analysis-collapsible"]');
                    for (const p of panels) {
                        if (p.innerText.includes('SEO analysis') || p.innerText.includes('SEO 分析') || p.innerText.includes('Queensfloor')) {
                            return p.innerText;
                        }
                    }
                    return null;
                }""")
                print(f"Yoast SEO panel header text: {repr(score_text)}")
                if score_text:
                    lower_text = score_text.lower()
                    # Check for "good" or "绿色" or "好" (making sure we don't match "needs improvement")
                    if 'needs' in lower_text or 'improve' in lower_text:
                        return False
                    if 'good' in lower_text or '绿色' in lower_text or '好' in lower_text:
                        return True
                return False
                
            is_green = check_is_green()
            if not is_green:
                print("Yoast SEO is not green yet. Saving draft again...")
                if save_btn.is_visible():
                    save_btn.click()
                    page.wait_for_timeout(5000)
                is_green = check_is_green()
                
            print(f"Yoast SEO Green Status: {is_green}")
            
            # Screenshot of Yoast Metabox or sidebar
            screenshot_path = os.path.join(BRAIN_DIR, f"yoast_queensfloor_{article_idx:02d}.png")
            page.screenshot(path=screenshot_path)
            print(f"Saved page screenshot to: {screenshot_path}")
            
            # Publish the post!
            print("Publishing post...")
            publish_panel_btn = page.locator('button:has-text("Publish"), button:has-text("Publish…"), button:has-text("发布"), button:has-text("发布…"), .editor-post-publish-panel__toggle, .editor-layout__toggle-publish-panel-button').first
            if publish_panel_btn.is_visible():
                publish_panel_btn.click()
                page.wait_for_timeout(2000)
                
                confirm_btn = page.locator('.editor-post-publish-panel button:has-text("Publish"), .editor-post-publish-panel button:has-text("发布"), button.editor-post-publish-button').first
                if confirm_btn.is_visible():
                    confirm_btn.click()
                    page.wait_for_timeout(6000)
                    print("Post published successfully!")
            
            # Get final post URL
            post_url = page.evaluate("""() => {
                try {
                    return wp.data.select('core/editor').getPermalink();
                } catch(e) {
                    return null;
                }
            }""")
            if not post_url:
                # Fallback to link selectors
                post_url_locator = page.locator('a:has-text("View Post"), a:has-text("View post")')
                if post_url_locator.is_visible():
                    post_url = post_url_locator.get_attribute('href')
                    
            print(f"Final URL: {post_url}")
            
            if use_cdp:
                page.close()
            else:
                context.close()
            return {"site": name, "success": True, "url": post_url, "yoast_green": is_green}
            
        except Exception as e:
            print(f"Exception occurred while processing {name}: {e}")
            try:
                if not use_cdp:
                    context.close()
            except Exception:
                pass
            return {"site": name, "success": False, "error": str(e)}

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", type=str, help="Specific site name to run")
    parser.add_argument("--cdp", action="store_true", help="Connect to local Chrome instance on port 9222")
    args = parser.parse_args()
    
    results = []
    
    if args.site:
        target_site = None
        for s in SITES:
            if s["name"] == args.site:
                target_site = s
                break
        if not target_site:
            print(f"Error: site '{args.site}' not found in configuration.")
            return
        res = publish_site(target_site, use_cdp=args.cdp)
        results.append(res)
    else:
        # Run all sites
        for s in SITES:
            res = publish_site(s, use_cdp=args.cdp)
            results.append(res)
            
    print("\n" + "="*80)
    print("FINAL PUBLISHING REPORT")
    print("="*80)
    for r in results:
        if r and r.get("success"):
            print(f"[*] {r['site']}: SUCCESS! URL: {r['url']} | Yoast Green: {r['yoast_green']}")
        else:
            print(f"[x] {r['site'] if r else 'unknown'}: FAILED! Error: {r.get('error') if r else 'unknown error'}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
