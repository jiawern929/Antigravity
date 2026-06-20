import sys
import base64
import os
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

images = [
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781267919578.jpg",
        "name": "filken_ultra_d_70_pro.jpg",
        "title": "Filken Ultra D-Series 70 Pro 户外滤水器"
    },
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781267919582.jpg",
        "name": "filken_ultra_d_74_champion.jpg",
        "title": "Filken Ultra D 74 Champion 马六甲安装实例"
    },
    {
        "path": r"C:\Users\jiawe\\.gemini\\antigravity\\brain\\4b2e9a7e-4557-4037-ab5a-d5661b3b8570\\media__1781267919585.jpg",
        "name": "filken_ultra_d_m1_jb.jpg",
        "title": "Filken Ultra D M1 新山安装实例"
    }
]

def run():
    print("Connecting to Chrome to upload images to businessinsider101.com...")
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            context = browser.contexts[0]
            
            # Find the active businessinsider101 editor tab
            page = None
            for p_page in context.pages:
                if "businessinsider101.com/wp-admin" in p_page.url:
                    page = p_page
                    page.bring_to_front()
                    break
            
            if not page:
                print("Could not find the open editor tab for businessinsider101.com.")
                return
            
            print(f"Found active editor tab: {page.url}")
            
            # Wait for wpApiSettings to be available
            page.wait_for_function("() => window.wpApiSettings")
            
            results = []
            for img in images:
                file_path = img["path"].replace("\\\\", "\\")
                if not os.path.exists(file_path):
                    print(f"File not found: {file_path}")
                    continue
                
                print(f"Reading file: {file_path}")
                with open(file_path, "rb") as f:
                    file_data = f.read()
                
                base64_data = base64.b64encode(file_data).decode("utf-8")
                
                print(f"Uploading image: {img['name']}...")
                
                upload_js = """
                async ([base64Data, filename, title]) => {
                    // Convert base64 to ArrayBuffer
                    const binaryString = atob(base64Data);
                    const bytes = new Uint8Array(binaryString.length);
                    for (let i = 0; i < binaryString.length; i++) {
                        bytes[i] = binaryString.charCodeAt(i);
                    }
                    const arrayBuffer = bytes.buffer;
                    
                    const nonce = wpApiSettings.nonce;
                    const apiRoot = wpApiSettings.root;
                    
                    const response = await fetch(apiRoot + "wp/v2/media", {
                        method: "POST",
                        headers: {
                            "Content-Type": "image/jpeg",
                            "X-WP-Nonce": nonce,
                            "Content-Disposition": `attachment; filename="${filename}"`
                        },
                        body: arrayBuffer
                    });
                    
                    if (!response.ok) {
                        const errText = await response.text();
                        throw new Error(`Upload failed: ${response.status} ${response.statusText} - ${errText}`);
                    }
                    
                    const mediaObj = await response.json();
                    
                    // Optional: Update title/alt text of the uploaded image
                    try {
                        await fetch(apiRoot + `wp/v2/media/${mediaObj.id}`, {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-WP-Nonce": nonce
                            },
                            body: JSON.stringify({
                                title: title,
                                alt_text: "KL滤水器推荐",
                                description: "KL滤水器推荐"
                            })
                        });
                    } catch (e) {
                        console.error("Failed to update media details:", e);
                    }
                    
                    return {
                        id: mediaObj.id,
                        source_url: mediaObj.source_url
                    };
                }
                """
                
                try:
                    res = page.evaluate(upload_js, [base64_data, img["name"], img["title"]])
                    print(f"Uploaded successfully! ID: {res['id']}, URL: {res['source_url']}")
                    img["id"] = res["id"]
                    img["url"] = res["source_url"]
                    results.append(img)
                except Exception as ex:
                    print(f"Error uploading image {img['name']}: {ex}")
            
            print("\nUpload Summary:")
            for r in results:
                print(f"Name: {r['name']}")
                print(f"  ID: {r.get('id')}")
                print(f"  URL: {r.get('url')}")
                print("-" * 20)
                
        except Exception as e:
            print("Error connecting/uploading:", e)

if __name__ == "__main__":
    run()
