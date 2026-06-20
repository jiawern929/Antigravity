import os
import json
import glob

def get_chrome_profiles():
    user_data_dir = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
    print(f"Searching for Chrome profiles in: {user_data_dir}")
    
    if not os.path.exists(user_data_dir):
        print("Chrome User Data directory not found.")
        return
    
    profiles = []
    
    # Standard profile directories are 'Default' or 'Profile *'
    search_patterns = [
        os.path.join(user_data_dir, 'Default'),
        *glob.glob(os.path.join(user_data_dir, 'Profile *'))
    ]
    
    for profile_dir in search_patterns:
        if not os.path.isdir(profile_dir):
            continue
            
        pref_path = os.path.join(profile_dir, 'Preferences')
        profile_folder = os.path.basename(profile_dir)
        profile_name = "Unknown"
        
        if os.path.exists(pref_path):
            try:
                with open(pref_path, 'r', encoding='utf-8') as f:
                    prefs = json.load(f)
                    # Extract profile name
                    profile_name = prefs.get('profile', {}).get('name', 'Default Profile')
            except Exception as e:
                profile_name = f"Could not parse Preferences ({e})"
        
        profiles.append({
            'folder': profile_folder,
            'name': profile_name,
            'path': profile_dir
        })
        
    print("\nFound Profiles:")
    for idx, p in enumerate(profiles):
        print(f"[{idx}] Name: {p['name']} (Folder: {p['folder']})")
        
    return profiles

if __name__ == "__main__":
    get_chrome_profiles()
