import os
import sys
from html.parser import HTMLParser

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

html_path = r"C:\Users\jiawe\.gemini\antigravity\scratch\bi_yoast_dump.html"

if not os.path.exists(html_path):
    print("File not found.")
    exit(1)

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

class YoastParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_li = False
        self.current_li_text = []
        self.li_classes = []
        
    def handle_starttag(self, tag, attrs):
        if tag == "li":
            self.in_li = True
            self.current_li_text = []
            for attr, val in attrs:
                if attr == "class":
                    self.li_classes = val
                    
    def handle_endtag(self, tag):
        if tag == "li" and self.in_li:
            text = "".join(self.current_li_text).strip()
            if text:
                print(f"Bullet: {text}")
                print(f"Classes: {self.li_classes}")
                print("-" * 50)
            self.in_li = False
            
    def handle_data(self, data):
        if self.in_li:
            self.current_li_text.append(data)

parser = YoastParser()
parser.feed(html_content)
