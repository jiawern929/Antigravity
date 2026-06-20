import urllib.request
import json
import sys

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    with urllib.request.urlopen("http://127.0.0.1:9222/json") as response:
        tabs = json.loads(response.read().decode())
        for tab in tabs:
            title = tab.get('title', '').encode('utf-8', errors='replace').decode('utf-8')
            url = tab.get('url', '').encode('utf-8', errors='replace').decode('utf-8')
            print(f"ID: {tab.get('id')}")
            print(f"Title: {title}")
            print(f"URL: {url}")
            print(f"Type: {tab.get('type')}")
            print("-" * 40)
except Exception as e:
    print(f"Error connecting to Chrome: {e}")

