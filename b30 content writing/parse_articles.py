import sys
import os
import re
import json

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BRAIN_DIR = r"C:\Users\jiawe\.gemini\antigravity\brain\4b2e9a7e-4557-4037-ab5a-d5661b3b8570"
txt_path = os.path.join(BRAIN_DIR, "gemini_shared_conversation_text.txt")

def run():
    print(f"Reading file: {txt_path}")
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split the file by the message boundary
    parts = content.split("--- MSG BOUNDARY ---")
    print(f"Found {len(parts)} segments in the conversation file.")
    
    # We want to find segments that contain article drafts.
    # An article segment typically has "SEO标题：" or "大标题：" or "Meta description："
    articles = []
    for i, part in enumerate(parts):
        part = part.strip()
        if "SEO标题：" in part or "大标题：" in part or "SEO标题:" in part or "大标题:" in part:
            articles.append(part)
            
    print(f"Extracted {len(articles)} article drafts.")
    
    # Let's parse each article
    for idx, art in enumerate(articles, 1):
        print(f"\nParsing Article {idx}...")
        
        # Extract fields
        seo_title = ""
        h1_title = ""
        meta_desc = ""
        excerpt = ""
        
        # Regex or line-by-line parsing
        lines = art.split('\n')
        body_lines = []
        in_body = False
        
        for line in lines:
            line_str = line.strip()
            if not line_str:
                if in_body:
                    body_lines.append("")
                continue
                
            if line_str.startswith("SEO标题：") or line_str.startswith("SEO标题:"):
                seo_title = re.sub(r"^SEO标题[：:]\s*", "", line_str)
            elif line_str.startswith("大标题：") or line_str.startswith("大标题:"):
                h1_title = re.sub(r"^大标题[：:]\s*", "", line_str)
            elif line_str.startswith("Meta description：") or line_str.startswith("Meta description:"):
                meta_desc = re.sub(r"^Meta description[：:]\s*", "", line_str)
            elif line_str.startswith("Excerpt：") or line_str.startswith("Excerpt:"):
                excerpt = re.sub(r"^Excerpt[：:]\s*", "", line_str)
            else:
                # This must be the body
                # If we hit H2 headings or standard paragraphs
                in_body = True
                body_lines.append(line_str)
                
        # Reconstruct body content
        # Filter out trailing empty lines or headers that got mixed
        body_content = "\n".join(body_lines).strip()
        
        # Save parsed article
        art_data = {
            "index": idx,
            "seo_title": seo_title,
            "h1_title": h1_title,
            "meta_description": meta_desc,
            "excerpt": excerpt,
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
    run()
