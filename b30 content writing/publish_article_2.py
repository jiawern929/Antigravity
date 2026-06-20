import os
import sys
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Configure UTF-8 encoding for Windows console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Site info (Site #2: huawennews)
site = {
    "name": "huawennews",
    "url": "https://huawennews.com/brandnews3007/?loggedout=true&wp_lang=en_US",
    "user": "jwern929@gmail.com",
    "pass": "PFHx1pBpwoD*7#lPthajn!YC"
}

# Post details (Same article for the 2nd domain)
title = "频密制水与管线老化夹击？深入探讨巴生谷家庭都在搜的 KL滤水器推荐 方案"
content = """<p>（吉隆坡，12日讯）近年来，巴生谷一带的社区频密面临水管维修或突发性制水，每当恢复供水时，水龙头流出的浊水总是让不少家庭主妇感到无奈。随着人们对健康生活的要求不断提高，饮用水的安全隐患已经成为了本地社区热议的话题。很多街坊邻居在茶余饭后，都在互相打听到底市面上哪一种设备最靠谱。为了探究这个现象，我们走访了多个新旧住宅区，整理出一份贴近真实生活的 KL滤水器推荐 报道，希望能用最平实的话语，帮你理清目前市面上的净水趋势，不再被花俏的广告词牵着鼻子走。</p>

<p>其实，很多民众都不太清楚，自来水厂处理出来的水虽然完全符合安全标准，但在输送到我们家里的过程中，往往会经历各种二次污染。像是吉隆坡很多发展了三四十年的老社区，地下水管早已老化甚至生锈。不仅是雪隆区，就连新山或槟城的一些老城区，也同样面临着类似的水管老化挑战。很多人都会以为只要把水煮沸就万无一失，但简单来说，高温只能杀菌，对于溶解在水里的重金属、铁锈泥沙以及肉眼看不见的化学残留物，其实根本无能为力。这种长期的水质隐忧，直接催生了本地家庭对净水设备的强劲需求。</p>

<h2>频密制水与水压波动推高吉隆坡滤水器需求</h2>
<p>很多住在老式公寓或密集住宅区的居民都会抱怨，一到晚上下班高峰期，家里的水压就会明显变小。一旦遇上附近路段爆水管或者进行例行维修，水供恢复后的那一两小时，水槽底下经常会积满黄黄的沉淀物，不仅洗菜不安心，用来洗白衣服更是一场灾难。这也是为什么近两年来，吉隆坡滤水器 的整体搜索量和销量一直居高不下。大家已经渐渐明白，单靠水龙头上那个简陋的滤水网根本起不了什么大作用，多数家庭越来越倾向于在家中安装一套更完善的净水系统。</p>

<p>但是，面对市场上琳琅满目的选择，反而让很多人不知所措。很多人会误以为，只要掏钱把最贵、最新的全能机型搬回家，就能解决所有的水质问题。其实这是一个非常普遍的消费迷思。我们在采访本地社区的资深水电师傅时，他们都异口同声地表示，挑选设备最重要的是因地制宜。如果你住的楼层水压本来就弱，却硬装上一台需要极高水压才能顺利运作的高密度净水器，最后受苦的只会是每天等着接水煮饭的自己。</p>

<h2>结合生活习惯与房型找出理想的 KL 滤水器</h2>
<p>在探讨如何挑选最刚好的设备时，你必须先把焦点放回全家人的真实生活习惯上。打个比方，如果你是一个经常需要出差的单身上班族，平时大多数时间都在外头解决三餐，那么在厨房台面上加装一台免安装的轻便型设备就非常足够了。相反的，如果你是一个三代同堂的大家庭，每天光是煮汤、泡茶、半夜冲泡奶粉就需要消耗大量的水，那么一台具备智能温控、出水量又大又稳定的 KL 滤水器，绝对能大幅减轻你在厨房里的家务负担，提升整个家庭的喝水体验。</p>

<p>此外，房屋的格局类型也直接决定了你的过滤系统该怎么布局。住在排屋（Landed）的朋友通常拥有更多的空间优势，可以直接在庭院的主水管处先安置一个户外的第一道防线，把黄泥和粗大杂质彻底挡在门外，这样连带屋内的直饮机滤芯寿命也会跟着延长。而对于住在高级 Condo 的住户来说，受限于管理层的严苛装潢规定以及非常有限的厨房台面空间，寻找体积小巧且能隐藏在厨下、不破坏原有设计的吉隆坡滤水器推荐方案，才是最符合现实生活状况的明智之举。</p>

<h2>看破行销话术背后的隐藏保养开销</h2>
<p>本地的新闻报道偶尔也会揭露一些不良的家电销售手法，最常见的就是利用极低的机器价格来吸引顾客上钩，这也就是俗称的“剃须刀模式”。很多人在大型展销会上看到价格极具吸引力的净水配套，一时冲动就签下了单子。但往往在半年或一年后，当售后人员提醒需要上门更换专属滤芯时，那笔高昂的材料和人工维护费才让人如梦初醒。所以说，保障家人的饮用水安全是一场长期的拔河，买得起机器，更要算清楚往后养不养得起。</p>

<p>我们在整理民意资料时发现，很多民众在买机器时根本没有主动过问后续的耗材价格。不管是普通的碳芯、超滤膜还是高精度的反渗透膜，都有其严格的使用寿命限制。如果因为嫌换滤芯太贵而一拖再拖，滤网里面滋生堆积的细菌反而会让水质变得比没过滤前还要糟糕。因此，大家在网络上参考各种攻略时，一定要把每年的固定保养费一毛不差地算进家庭的年度开销预算里，这才是精明消费者该有的基本功。</p>

<h2>售后服务与安装前的专业评估不可或缺</h2>
<p>说真的，哪怕你买的是市面上评价最顶级的机器，如果师傅的安装手法不当，最后也会引发一连串的麻烦。很多本地社团论坛上都有类似的翻车经验分享：安装人员上门后没做好水压测试，管线拉得乱七八糟，最后甚至导致木制橱柜漏水发霉。所以，前期的现场实地勘测和专业评估，其实比耀眼的品牌光环来得更重要。一个负责任的团队在接下工作后，首先要做的应该是全面了解你的居住条件，看看洗碗槽下方有没有预留电源，或者墙壁水管的走向到底适不适合安装特定的型号。</p>

<p>在这种情况下，像Filken 这样的专业滤水团队，通常会扮演较中立、行政或协助的角色。他们不会一见面就急着疯狂推销那些华而不实的高端机型，而是会依据你现有的厨房环境、家人的实际每日用水量以及你设定的心理预算，给出一个最务实、最贴地的规划建议。这种不带压迫感的沟通方式，不仅减少了顾客在面对众多型号时的选择困难，也从根本上杜绝了因为瞎买乱装而引发的后续客诉，让消费者在付钱时感到更加安心与踏实。</p>

<h2>总结：回归饮水本质，理性看待 KL滤水器推荐</h2>
<p>简单说到底，居家饮用水的品质关乎每个家庭成员的切身健康，这绝对不是一件可以随便将就的小事。面对老旧水管带来的二次污染隐患，我们需要做的不是盲目追求市场上最昂贵的净水科技，而是冷静地坐下来分析自家的真实痛点。希望这篇贴近本地民生视角的报道，能让你在面对铺天盖地的行销资讯时保持清醒的头脑。下次当你在网络上参考各种 KL滤水器推荐 时，记得多留意后续的保养费用 and 安装评估的细节，理性做出对比，最终必定能为全家人找到那个最靠谱、最长久的健康好水守卫。</p>
"""

excerpt = "面对老旧水管带来的水质隐忧，挑选净水系统成了许多本地家庭的必修课。这篇报道带你直击巴生谷社区的真实用水痛点，透过客观的趋势分析与选购准则，帮你理清思路，找到真正贴合居家生活习惯的净水方案。"
slug = "kl-water-filter-recommendations-2026"
yoast_title = "告别老旧管线隐患，2026最新KL滤水器推荐与本地水质趋势全解析"
yoast_desc = "居住在巴生谷一带的你，是否经常面对自来水偏黄或带有漂白水异味的困扰？随着社区管线老化，越来越多家庭开始重视饮用水 of 二次污染问题。本文透过本地新闻视角的真实走访，为你全面剖析不同住宅类型的净水痛点，并提供最中立客观的KL滤水器推荐。无论你是住公寓还是有地房，都能从中找到避开隐藏开销、保障全家饮用水安全的专业核心结论与实用建议。"

def inject_banner(driver, text):
    try:
        driver.execute_script(f"""
            var existing = document.getElementById('ai-progress-banner');
            if (existing) {{
                document.getElementById('ai-banner-text').innerText = {repr(text)};
            }} else {{
                var banner = document.createElement('div');
                banner.id = 'ai-progress-banner';
                banner.innerHTML = `
                  <div style="
                    position: fixed;
                    top: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: rgba(30, 41, 59, 0.95);
                    backdrop-filter: blur(8px);
                    color: white;
                    padding: 14px 28px;
                    border-radius: 12px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
                    z-index: 9999999;
                    font-family: system-ui, sans-serif;
                    font-size: 16px;
                    font-weight: 600;
                    border: 1px solid rgba(255,255,255,0.15);
                    display: flex;
                    align-items: center;
                    gap: 12px;
                  ">
                    <span style="
                      width: 10px;
                      height: 10px;
                      background: #10B981;
                      border-radius: 50%;
                      display: inline-block;
                      animation: pulse 1.5s infinite;
                    "></span>
                    <span id="ai-banner-text">{text}</span>
                  </div>
                  <style>
                    @keyframes pulse {{
                      0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
                      70% {{ transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }}
                      100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
                    }}
                  </style>
                `;
                document.body.appendChild(banner);
            }}
        """)
    except Exception:
        pass

def highlight_element(driver, element_id, text_to_set_banner=""):
    if text_to_set_banner:
        inject_banner(driver, text_to_set_banner)
    try:
        driver.execute_script(f"""
            var el = document.getElementById('{element_id}');
            if (el) {{
                el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                el.style.outline = '4px dashed #3B82F6';
                el.style.boxShadow = '0 0 20px #3B82F6';
                el.style.transition = 'all 0.5s ease';
            }}
        """)
    except Exception:
        pass

def publish():
    name = site["name"]
    login_url = site["url"]
    username = site["user"]
    password = site["pass"]
    
    print(f"\n" + "="*50)
    print(f"STARTING VISUAL STEPPED PUBLISH FOR SITE: {name}")
    print(f"URL: {login_url}")
    print("="*50)
    
    user_data_dir = os.path.abspath('chrome_temp_profile')
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={name}")
    
    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"Failed to launch Chrome for {name}: {e}")
        return
        
    try:
        print("Step 1: Navigating to website...")
        driver.get(login_url)
        time.sleep(5)
        
        try:
            # Inject banner to explain step 1
            inject_banner(driver, "AI Step 1/5: Loading Login Page...")
            time.sleep(3)
            
            # Step 2: Highlight Username and type
            print("Step 2: Entering username...")
            highlight_element(driver, "user_login", "AI Step 2/5: Highlighting and typing Username...")
            time.sleep(2)
            username_field = driver.find_element(By.ID, "user_login")
            username_field.clear()
            for char in username:
                username_field.send_keys(char)
                time.sleep(0.05) # Type like a human
            time.sleep(2)
            
            # Step 3: Highlight Password and type
            print("Step 3: Entering password...")
            highlight_element(driver, "user_pass", "AI Step 3/5: Highlighting and typing Password...")
            time.sleep(2)
            password_field = driver.find_element(By.ID, "user_pass")
            password_field.clear()
            for char in password:
                password_field.send_keys(char)
                time.sleep(0.05)
            time.sleep(2)
            
            # Step 4: Highlight Submit Button and click
            print("Step 4: Submitting login...")
            highlight_element(driver, "wp-submit", "AI Step 4/5: Clicking the Login button...")
            time.sleep(2)
            driver.find_element(By.ID, "wp-submit").click()
            print("Login submitted. Waiting for dashboard redirect...")
            time.sleep(8)
        except Exception as err:
            print(f"Login elements not found or already logged in: {err}")
            
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
        # Inject progress banner on the admin page
        inject_banner(driver, "AI Step 5/5: Logged in! Fetching API tokens and publishing...")
        time.sleep(3)
        
        if "wp-admin" not in current_url:
            base_url = login_url.split('?')[0]
            if not base_url.endswith('/'):
                base_url += '/'
            if "wp-admin" not in base_url:
                admin_url = f"{base_url}wp-admin/"
            else:
                admin_url = base_url
                
            print(f"Navigating to admin dashboard: {admin_url}")
            driver.get(admin_url)
            time.sleep(4)
            inject_banner(driver, "AI Step 5/5: Fetching API tokens and publishing...")
            time.sleep(2)
            current_url = driver.current_url
            
        if "wp-admin" not in current_url:
            print("Login verification failed. Not in WordPress admin.")
            return
            
        # Extract REST API nonce
        nonce = None
        api_root = None
        try:
            nonce = driver.execute_script("return wpApiSettings.nonce;")
            api_root = driver.execute_script("return wpApiSettings.root;")
        except Exception:
            pass
            
        if not nonce:
            html = driver.page_source
            match = re.search(r'"nonce"\s*:\s*"([a-zA-Z0-9]+)"', html)
            if match:
                nonce = match.group(1)
                base_admin = current_url.split('wp-admin')[0]
                api_root = f"{base_admin}wp-json/"
                
        if not nonce:
            print("Could not retrieve WordPress API nonce.")
            inject_banner(driver, "Error: Could not retrieve WordPress API Nonce!")
            time.sleep(5)
            return
            
        print(f"API Nonce: {nonce}")
        
        # Publish
        inject_banner(driver, "AI: Submitting article content and SEO data to REST API...")
        time.sleep(2)
        
        js_code = f"""
        var callback = arguments[arguments.length - 1];
        fetch("{api_root}wp/v2/posts", {{
            method: "POST",
            headers: {{
                "Content-Type": "application/json",
                "X-WP-Nonce": "{nonce}"
            }},
            body: JSON.stringify({{
                title: {repr(title)},
                content: {repr(content)},
                excerpt: {repr(excerpt)},
                slug: "{slug}",
                status: "publish",
                meta: {{
                    _yoast_wpseo_title: {repr(yoast_title)},
                    _yoast_wpseo_metadesc: {repr(yoast_desc)}
                }}
            }})
        }})
        .then(res => {{
            if (!res.ok) {{
                return res.text().then(text => {{ throw new Error(text); }});
            }}
            return res.json();
        }})
        .then(data => callback({{success: true, data: data}}))
        .catch(err => callback({{success: false, error: err.message}}));
        """
        
        result = driver.execute_async_script(js_code)
        
        if result.get("success"):
            post_data = result.get("data")
            post_link = post_data.get("link")
            print(f"\nSUCCESS! Post created: {post_link}")
            
            # Show SUCCESS banner on user's screen!
            inject_banner(driver, f"SUCCESS! Article Published! Redirecting in 3s...")
            time.sleep(3)
            
            # Navigate to the published post to show it to them in their browser window!
            driver.get(post_link)
            inject_banner(driver, "Done! Here is your published article. Closing in 8s...")
            time.sleep(8)
        else:
            err_msg = result.get("error")
            print(f"\nFAILED to publish: {err_msg}")
            inject_banner(driver, f"Error publishing: {err_msg}")
            time.sleep(10)
            
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(5)
    finally:
        driver.quit()

if __name__ == "__main__":
    publish()
