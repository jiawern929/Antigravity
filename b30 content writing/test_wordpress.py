import xmlrpc.client

def test_xmlrpc():
    url = "https://dushitoutiao.com/brandnews30010/xmlrpc.php"
    username = "jwern929@gmail.com"
    password = "PFHx1pBpwoD*7#lPthajn!YC"
    
    print(f"Testing XML-RPC connection to {url}...")
    server = xmlrpc.client.ServerProxy(url)
    
    try:
        # Get user blogs to verify credentials
        blogs = server.wp.getUsersBlogs(username, password)
        print("Success! Connection and credentials are valid.")
        print(f"Blogs: {blogs}")
    except Exception as e:
        print(f"Failed to connect or login: {e}")

if __name__ == "__main__":
    test_xmlrpc()
