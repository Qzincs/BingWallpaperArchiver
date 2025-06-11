import os
import json
import requests
import sys

markets = [
    "en-US",  # USA
    "en-GB",  # UK
    "de-DE",  # Germany
    "en-CA",  # Canada
    "ja-JP",  # Japan
    "zh-CN",  # China
    "fr-FR",  # France
    "pt-BR",  # Brazil
    "it-IT",  # Italy
    "es-ES",  # Spain
    "en-IN",   # India
    "en-AU",  # Australia
    "en-NZ",  # New Zealand
]

def get_bing_wallpaper_metadata(market):
    url = f"https://services.bingapis.com/ge-apps/api/v2/bwc/hpimages?mkt={market}&theme=bing&defaultBrowser=ME&dhpSetToBing=True&dseSetToBing=True"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-200 status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for market {market}: {str(e)}")
        return None
    
def get_all_country_wallpapers():
    success_count = 0
    for market in markets:
        metadata = get_bing_wallpaper_metadata(market)
        if metadata:
            filename = f"{market}.json"
            if save_json_to_file(metadata, filename):
                success_count += 1
    
    # Return success status
    if success_count == 0:
        print("Error: Failed to fetch or save any wallpaper data")
        return False
    
    print(f"Successfully processed {success_count}/{len(markets)} markets")
    return True

def save_json_to_file(data, filename):
    images = data.get("images", [])
    path = f"data/{filename}"
    
    if not os.path.exists("data"):
        os.makedirs("data")
    
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                saved_data = json.load(file)
                existing_images = saved_data.get("images", [])
        else:
            existing_images = []
        
        existing_dates = {img.get("startdate") for img in existing_images}
        new_images = [img for img in images if img.get("startdate") not in existing_dates]
        
        all_images = existing_images + new_images
        
        all_images.sort(key=lambda img: img.get("startdate", ""), reverse=True)
        
        with open(path, "w", encoding="utf-8") as file:
            json.dump({"images": all_images}, file, ensure_ascii=False, indent=2)
        
        print(f"Saved to {path}, added {len(new_images)} new images, total: {len(all_images)}")
        return True
    
    except Exception as e:
        print(f"Error saving {filename}: {str(e)}")
        return False


def main():
    success = get_all_country_wallpapers()
    # Exit with error code if operation failed
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
