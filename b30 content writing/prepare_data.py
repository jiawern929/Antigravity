import os
import sys
import re
import json
import shutil

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BRAIN_DIR = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570"
txt_path = os.path.join(BRAIN_DIR, "gemini_shared_conversation_text.txt")

# Image mappings
IMAGES_MAP = {
    "media__1781685122676.jpg": "queensfloor_staff_accommodation.jpg",
    "media__1781685122679.jpg": "queensfloor_average_sales_orders.jpg",
    "media__1781685122687.jpg": "queensfloor_working_environment.jpg",
    "media__1781685122695.jpg": "queensfloor_practical_sales_training.jpg",
    "media__1781685122706.jpg": "queensfloor_sales_consultant_hiring.jpg"
}

def rename_images():
    print("Renaming raw images...")
    media_dir = os.path.join(BRAIN_DIR, "queensfloor_media")
    os.makedirs(media_dir, exist_ok=True)
    
    for old_name, new_name in IMAGES_MAP.items():
        old_path = os.path.join(BRAIN_DIR, old_name)
        new_path = os.path.join(media_dir, new_name)
        if os.path.exists(old_path):
            shutil.copy2(old_path, new_path)
            print(f"Copied & Renamed: {old_name} -> {new_name}")
        else:
            print(f"Warning: Raw image {old_path} not found.")

def parse_articles():
    print(f"Reading conversation text from: {txt_path}")
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = content.split("--- MSG BOUNDARY ---")
    print(f"Found {len(parts)} segments in the file.")
    
    articles_data = []
    
    for i, part in enumerate(parts):
        part_strip = part.strip()
        if not part_strip:
            continue
            
        is_article = False
        lang = "ZH"
        
        # Check if Chinese article
        if ("SEO标题：" in part_strip or "SEO标题:" in part_strip) and ("大标题：" in part_strip or "大标题:" in part_strip):
            is_article = True
            lang = "ZH"
        # Check if English article
        elif "SEO Title:" in part_strip and "Big Title:" in part_strip:
            is_article = True
            lang = "EN"
            
        if is_article:
            articles_data.append((part_strip, lang, i))
            
    print(f"Identified {len(articles_data)} article drafts.")
    
    # Parse each article draft
    for idx, (art_text, lang, part_idx) in enumerate(articles_data, 1):
        print(f"\nParsing Article {idx} (Lang: {lang}, Part Index: {part_idx})...")
        
        seo_title = ""
        h1_title = ""
        meta_desc = ""
        excerpt = ""
        body_lines = []
        in_body = False
        
        lines = art_text.split('\n')
        for line in lines:
            line_str = line.strip()
            if not line_str:
                if in_body:
                    body_lines.append("")
                continue
                
            # Check Chinese headers
            if line_str.startswith("SEO标题：") or line_str.startswith("SEO标题:"):
                seo_title = re.sub(r"^SEO标题[：:]\s*", "", line_str)
            elif line_str.startswith("大标题：") or line_str.startswith("大标题:"):
                h1_title = re.sub(r"^大标题[：:]\s*", "", line_str)
            elif line_str.startswith("Meta description：") or line_str.startswith("Meta description:"):
                meta_desc = re.sub(r"^Meta description[：:]\s*", "", line_str)
            elif line_str.startswith("Excerpt：") or line_str.startswith("Excerpt:"):
                excerpt = re.sub(r"^Excerpt[：:]\s*", "", line_str)
            # Check English headers
            elif line_str.startswith("SEO Title:"):
                seo_title = re.sub(r"^SEO Title:\s*", "", line_str)
            elif line_str.startswith("Big Title:"):
                h1_title = re.sub(r"^Big Title:\s*", "", line_str)
            elif line_str.startswith("Meta Description:"):
                meta_desc = re.sub(r"^Meta Description:\s*", "", line_str)
            elif line_str.startswith("Excerpt:"):
                excerpt = re.sub(r"^Excerpt:\s*", "", line_str)
            else:
                in_body = True
                body_lines.append(line_str)
                
        # Reconstruct body content
        body_content = "\n".join(body_lines).strip()
        
        art_data = {
            "index": idx,
            "language": lang,
            "seo_title": seo_title.strip(),
            "h1_title": h1_title.strip(),
            "meta_description": meta_desc.strip(),
            "excerpt": excerpt.strip(),
            "body": body_content
        }
        
        art_path = os.path.join(BRAIN_DIR, f"article_{idx:02d}.json")
        with open(art_path, 'w', encoding='utf-8') as f:
            json.dump(art_data, f, indent=4, ensure_ascii=False)
            
        print(f"Saved Article {idx} to: {art_path}")
        print(f"  SEO Title: {seo_title}")
        print(f"  H1 Title: {h1_title}")
        print(f"  Body length: {len(body_content)} chars")

if __name__ == "__main__":
    rename_images()
    parse_articles()
