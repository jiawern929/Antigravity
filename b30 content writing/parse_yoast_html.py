import re

with open("wpseo_meta.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's find all occurrences of "Readability" in HTML and print surrounding context
print("Occurrences of Readability:")
for m in re.finditer(r"Readability", html, re.IGNORECASE):
    start = max(0, m.start() - 100)
    end = min(len(html), m.end() + 200)
    print(f"Match: {html[start:end]}")
    print("-" * 50)
