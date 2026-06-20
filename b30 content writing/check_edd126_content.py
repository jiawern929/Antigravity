import urllib.request
import sys

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

url = "https://iconicmafia.com/edd126/"
try:
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        html = response.read().decode('utf-8', errors='ignore')
        print(f"Title: {html.split('<title>')[1].split('</title>')[0] if '<title>' in html else 'None'}")
        print("Body snippet (first 500 chars):")
        print(html[:500])
except Exception as e:
    print("Error:", e)
