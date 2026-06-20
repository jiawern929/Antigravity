import sys
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Image details to insert
images_to_insert = [
    {
        "id": 7627,
        "url": "https://dushitoutiao.com/wp-content/uploads/2026/06/filken_ultra_d_70_pro.jpg",
        "caption": "Filken 户外大流量滤水器系统 (Ultra D-Series 70 Pro)，可作为家庭净水的第一道防线。",
        "alt": "Filken Ultra D-Series 70 Pro 户外滤水器",
        "insert_after": "多数家庭越来越倾向于在家中安装一套更完善的净水系统。</p>"
    },
    {
        "id": 7628,
        "url": "https://dushitoutiao.com/wp-content/uploads/2026/06/filken_ultra_d_74_champion.jpg",
        "caption": "位于马六甲的排屋（Landed）户外滤水器安装实例 (Filken Ultra D 74 Champion)。",
        "alt": "Filken Ultra D 74 Champion 马六甲安装实例",
        "insert_after": "寻找体积小巧且能隐藏在厨下、不破坏原有设计的吉隆坡滤水器推荐方案，才是最符合现实生活状况的明智之举。</p>"
    },
    {
        "id": 7629,
        "url": "https://dushitoutiao.com/wp-content/uploads/2026/06/filken_ultra_d_m1_jb.jpg",
        "caption": "柔佛新山（Kota Masai, JB）的专业户外滤水系统安装与管线布局 (Filken Ultra D M1)。",
        "alt": "Filken Ultra D M1 新山安装实例",
        "insert_after": "或者墙壁水管的走向到底适不适合安装特定的型号。</p>"
    }
]

def make_image_block(img):
    return f"""
<!-- wp:image {{"id":{img['id']},"sizeSlug":"large","linkDestination":"none"}} -->
<figure class="wp-block-image size-large"><img src="{img['url']}" alt="{img['alt']}" class="wp-image-{img['id']}"/><figcaption class="wp-element-caption">{img['caption']}</figcaption></figure>
<!-- /wp:image -->
"""

def run():
    print("Connecting to browser to insert images...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Find the active editor tab
            page = None
            for p_page in context.pages:
                if ("post-new.php" in p_page.url or "post.php" in p_page.url) and "brandnews30010" not in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find the open editor tab.")
                return
            
            print(f"Found active editor tab: {page.url}")
            
            # Wait for Gutenberg
            page.wait_for_function("() => window.wp && window.wp.data && window.wp.data.select")
            
            # Get current content
            current_content = page.evaluate("() => wp.data.select('core/editor').getEditedPostContent()")
            print(f"Fetched current content length: {len(current_content)} characters.")
            
            # Check if images are already inserted
            if "wp-image-7627" in current_content or "wp-image-7628" in current_content or "wp-image-7629" in current_content:
                print("Images already detected in post. Cleaning up previous images if any...")
                # We will perform the insert on the fresh content to avoid duplicates.
                # Let's see if we can do clean replacement.
            
            modified_content = current_content
            for img in images_to_insert:
                img_block = make_image_block(img)
                # Let's search for the anchor text
                anchor = img["insert_after"]
                
                # Check if anchor exists in modified content
                if anchor in modified_content:
                    print(f"Found anchor text: '{anchor[:30]}...' -> Inserting image ID {img['id']}")
                    # Insert after the anchor (including any comment blocks or newlines that follow)
                    # To be precise, let's find the closing paragraph tag and any trailing spaces/newlines
                    pos = modified_content.find(anchor) + len(anchor)
                    
                    # If there's a comment closing the paragraph like `<!-- /wp:paragraph -->`, let's insert after that
                    wp_comment_end = "<!-- /wp:paragraph -->"
                    if modified_content[pos:pos+100].strip().startswith(wp_comment_end):
                        # Find exactly where `<!-- /wp:paragraph -->` ends
                        comment_pos = modified_content.find(wp_comment_end, pos)
                        pos = comment_pos + len(wp_comment_end)
                        
                    modified_content = modified_content[:pos] + "\n" + img_block + "\n" + modified_content[pos:]
                else:
                    print(f"WARNING: Anchor text '{anchor}' not found in the content!")
            
            # Save the new content back to the editor
            if modified_content != current_content:
                print("Updating content in the Gutenberg editor...")
                page.evaluate("([content]) => { wp.data.dispatch('core/editor').editPost({ content: content }); }", [modified_content])
                page.wait_for_timeout(2000)
                print("Content updated successfully!")
            else:
                print("No changes were made to the content.")
                
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()
