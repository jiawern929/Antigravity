import re

with open("wpseo_meta.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find the section id="wpseo-meta-section-readability"
sec_match = re.search(r'id="wpseo-meta-section-readability".*?>(.*?)</div>\s*<div\s+role="tabpanel"', html, re.DOTALL)
if not sec_match:
    # Try finding it until the end of the meta section
    sec_match = re.search(r'id="wpseo-meta-section-readability".*?>(.*)', html, re.DOTALL)

if not sec_match:
    print("Readability section HTML block not found.")
else:
    section_html = sec_match.group(1)
    # Find all list items <li>...</li>
    items = re.findall(r'<li[^>]*>(.*?)</li>', section_html, re.DOTALL)
    print(f"Found {len(items)} list items:")
    for idx, item in enumerate(items):
        # Determine color
        color = "unknown"
        svg_match = re.search(r'<svg[^>]*class="([^"]*)"[^>]*fill="([^"]*)"', item)
        if not svg_match:
            svg_match = re.search(r'<svg[^>]*class="([^"]*)"', item)
        if not svg_match:
            svg_match = re.search(r'fill="([^"]*)"', item)
            
        if svg_match:
            # Let's inspect the groups
            groups_text = " ".join(svg_match.groups())
            if "bad" in groups_text or "red" in groups_text:
                color = "red"
            elif "ok" in groups_text or "orange" in groups_text:
                color = "orange"
            elif "good" in groups_text or "green" in groups_text:
                color = "green"
            elif "#d30" in groups_text or "#d30a0a" in groups_text:
                color = "red"
            elif "#ee7c1b" in groups_text or "#e67e22" in groups_text:
                color = "orange"
            elif "#7ad03a" in groups_text or "#008a00" in groups_text or "#7ad03a" in groups_text:
                color = "green"
        
        # Strip html tags from item
        text = re.sub(r'<[^>]*>', '', item)
        text = re.sub(r'\s+', ' ', text).strip()
        print(f"{idx+1}. [{color.upper()}] {text}")
