import urllib.request
import urllib.error

urls = [
    "https://iconicmafia.com/edd126/wp-login.php",
    "https://iconicmafia.com/wp-login.php",
    "https://iconicmafia.com/edd126/",
    "https://iconicmafia.com/"
]

for url in urls:
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"URL: {url} | Status: {response.status}")
    except urllib.error.HTTPError as e:
        print(f"URL: {url} | HTTP Error: {e.code} {e.reason}")
    except Exception as e:
        print(f"URL: {url} | Error: {e}")
