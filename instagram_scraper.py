"""
Instagram Profile Scraper

A professional tool to scrape public Instagram profile data using Selenium.
Uses your logged-in Chrome profile for authentication.

Author: Semir Harun
"""

import argparse
import csv
import json
import os
import sys
import time
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


def load_driver(profile_path: Optional[str] = None, headless: bool = False) -> webdriver.Chrome:
    """
    Initialize Chrome driver with user profile for Instagram login session.
    
    Args:
        profile_path: Path to Chrome user data directory
        headless: Run browser in headless mode (default: False)
        
    Returns:
        Chrome WebDriver instance
    """
    chrome_options = Options()
    
    # Default Chrome profile path for Windows
    if profile_path is None:
        import getpass
        username = getpass.getuser()
        profile_path = rf"C:\Users\{username}\AppData\Local\Google\Chrome\User Data"
    
    chrome_options.add_argument(f"user-data-dir={profile_path}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    if headless:
        chrome_options.add_argument("--headless")
    
    try:
        # Use WebDriverManager for automatic ChromeDriver management
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Execute script to hide automation indicators
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    except Exception as e:
        print(f"❌ Error initializing Chrome driver: {e}")
        print("💡 Make sure Chrome is installed and try again")
        sys.exit(1)


def scrape_profile(driver: webdriver.Chrome, username: str) -> Dict:
    """
    Scrape Instagram profile data for given username.
    
    Args:
        driver: Chrome WebDriver instance
        username: Instagram username to scrape
        
    Returns:
        Dictionary containing profile data
    """
    url = f"https://www.instagram.com/{username}/"
    
    try:
        print(f"🔍 Navigating to: {url}")
        driver.get(url)
        
        # Wait for page to load
        wait = WebDriverWait(driver, 10)
        
        # Check if profile exists (look for error page)
        try:
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
        except TimeoutException:
            return {
                "success": False,
                "error": "Failed to load profile page",
                "username": username
            }
        
        # Check for "Sorry, this page isn't available" error
        if "Sorry, this page isn't available" in driver.page_source:
            return {
                "success": False,
                "error": "Profile not found or private",
                "username": username
            }
        
        time.sleep(3)  # Additional wait for dynamic content
        
        # Extract profile data
        profile_data = {
            "success": True,
            "username": username,
            "profile_url": url,
            "scraped_at": datetime.now().isoformat(),
            "name": None,
            "bio": None,
            "followers": None,
            "following": None,
            "posts": None,
            "website": None,
            "profile_pic_url": None
        }
        
        try:
            # Get profile name
            name_element = driver.find_element(By.XPATH, "//h2[contains(@class, 'x1lliihq')]")
            profile_data["name"] = name_element.text.strip()
        except NoSuchElementException:
            print("⚠️  Could not find profile name")
        
        try:
            # Get bio/description
            bio_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'x1lliihq') and contains(@class, 'x193iq5w')]//span")
            if bio_elements:
                profile_data["bio"] = bio_elements[0].text.strip()
        except NoSuchElementException:
            print("⚠️  Could not find bio")
        
        try:
            # Get follower/following/posts count
            stat_elements = driver.find_elements(By.XPATH, "//a[contains(@href, f'/{username}/')]//span")
            if len(stat_elements) >= 3:
                profile_data["posts"] = stat_elements[0].text.strip()
                profile_data["followers"] = stat_elements[1].text.strip()
                profile_data["following"] = stat_elements[2].text.strip()
        except (NoSuchElementException, IndexError):
            print("⚠️  Could not find follower/following stats")
        
        try:
            # Get website link
            website_element = driver.find_element(By.XPATH, "//a[contains(@class, 'x1i10hfl') and starts-with(@href, 'http')]")
            profile_data["website"] = website_element.get_attribute("href")
        except NoSuchElementException:
            print("⚠️  No website link found")
        
        try:
            # Get profile picture URL
            img_element = driver.find_element(By.XPATH, f"//img[@alt=\"{username}'s profile picture\" or @alt='Profile photo']")
            profile_data["profile_pic_url"] = img_element.get_attribute("src")
        except NoSuchElementException:
            print("⚠️  Could not find profile picture")
        
        # Fallback: Try meta tags for basic info
        if not profile_data["name"] or not profile_data["bio"]:
            try:
                meta_desc = driver.find_element(By.XPATH, "//meta[@name='description']")
                desc_content = meta_desc.get_attribute("content")
                if desc_content and not profile_data["bio"]:
                    profile_data["bio"] = desc_content
            except NoSuchElementException:
                pass
        
        print("✅ Successfully scraped profile data")
        return profile_data
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "username": username
        }


def download_profile_picture(profile_pic_url: str, username: str, output_dir: str = "screenshots") -> Optional[str]:
    """
    Download profile picture from URL.
    
    Args:
        profile_pic_url: URL of the profile picture
        username: Instagram username
        output_dir: Directory to save pictures
        
    Returns:
        Path to downloaded file or None if failed
    """
    if not profile_pic_url:
        return None
        
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{username}_profile.jpg"
    filepath = os.path.join(output_dir, filename)
    
    try:
        response = requests.get(profile_pic_url, stream=True, timeout=10)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"📸 Profile picture saved to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"⚠️  Failed to download profile picture: {e}")
        return None


def save_to_json(data: Dict, username: str, output_dir: str = "data") -> str:
    """
    Save profile data to JSON file.
    
    Args:
        data: Profile data dictionary
        username: Instagram username
        output_dir: Directory to save files
        
    Returns:
        Path to saved file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"profile_{username}.json"
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Profile data saved to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return ""


def save_to_csv(data: Dict, username: str, output_dir: str = "data") -> str:
    """
    Save profile data to CSV file.
    
    Args:
        data: Profile data dictionary
        username: Instagram username
        output_dir: Directory to save files
        
    Returns:
        Path to saved file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"profile_{username}.csv"
    filepath = os.path.join(output_dir, filename)
    
    try:
        # Flatten the data for CSV
        csv_data = []
        if data.get("success"):
            csv_data.append({
                "username": data.get("username", ""),
                "name": data.get("name", ""),
                "bio": data.get("bio", "").replace('\n', ' '),  # Replace newlines
                "followers": data.get("followers", ""),
                "following": data.get("following", ""),
                "posts": data.get("posts", ""),
                "website": data.get("website", ""),
                "profile_url": data.get("profile_url", ""),
                "profile_pic_url": data.get("profile_pic_url", ""),
                "scraped_at": data.get("scraped_at", "")
            })
        
        if csv_data:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
                writer.writeheader()
                writer.writerows(csv_data)
            
            print(f"📊 CSV data saved to: {filepath}")
            return filepath
        else:
            print("❌ No data to save to CSV")
            return ""
            
    except Exception as e:
        print(f"❌ Error saving CSV file: {e}")
        return ""
    """
    Save profile data to JSON file.
    
    Args:
        data: Profile data dictionary
        username: Instagram username
        output_dir: Directory to save files
        
    Returns:
        Path to saved file
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"profile_{username}.json"
    filepath = os.path.join(output_dir, filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Profile data saved to: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return ""


def print_profile_summary(data: Dict) -> None:
    """Print a formatted summary of the profile data."""
    if not data.get("success"):
        print(f"❌ Failed to scrape profile: {data.get('error', 'Unknown error')}")
        return
    
    print("\n" + "="*50)
    print("📸 INSTAGRAM PROFILE SUMMARY")
    print("="*50)
    print(f"👤 Username: @{data.get('username', 'N/A')}")
    print(f"📝 Name: {data.get('name', 'N/A')}")
    print(f"📄 Bio: {data.get('bio', 'N/A')}")
    print(f"📊 Posts: {data.get('posts', 'N/A')}")
    print(f"👥 Followers: {data.get('followers', 'N/A')}")
    print(f"🔗 Following: {data.get('following', 'N/A')}")
    print(f"🌐 Website: {data.get('website', 'N/A')}")
    print(f"🔗 Profile URL: {data.get('profile_url', 'N/A')}")
    print("="*50)


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="📸 Instagram Profile Scraper - Extract public profile data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python instagram_scraper.py nasa
  python instagram_scraper.py nasa --csv --download-pic
  python instagram_scraper.py nasa --headless --output-dir ./results
        """
    )
    
    parser.add_argument("username", help="Instagram username to scrape")
    parser.add_argument("--csv", action="store_true", help="Also save data as CSV")
    parser.add_argument("--download-pic", action="store_true", help="Download profile picture")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--output-dir", default="data", help="Output directory for data files")
    parser.add_argument("--screenshots-dir", default="screenshots", help="Directory for profile pictures")
    parser.add_argument("--chrome-profile", help="Custom Chrome profile path")
    
    return parser.parse_args()


def main():
    """Main function to run the Instagram scraper."""
    # Fix Windows encoding issues
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    
    args = parse_arguments()
    
    username = args.username.strip().lower()
    
    if not username:
        print("❌ Username cannot be empty!")
        sys.exit(1)
    
    print(f"🚀 Starting Instagram scraper for: @{username}")
    print("🔧 Loading Chrome driver...")
    
    driver = None
    try:
        # Initialize driver
        driver = load_driver(profile_path=args.chrome_profile, headless=args.headless)
        
        # Scrape profile
        profile_data = scrape_profile(driver, username)
        
        # Save data
        if profile_data.get("success"):
            # Always save JSON
            save_to_json(profile_data, username, args.output_dir)
            
            # Save CSV if requested
            if args.csv:
                save_to_csv(profile_data, username, args.output_dir)
            
            # Download profile picture if requested
            if args.download_pic and profile_data.get("profile_pic_url"):
                download_profile_picture(
                    profile_data["profile_pic_url"], 
                    username, 
                    args.screenshots_dir
                )
            
            print_profile_summary(profile_data)
        else:
            print(f"❌ Failed to scrape profile: {profile_data.get('error')}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        
    finally:
        if driver:
            print("🔒 Closing browser...")
            driver.quit()


if __name__ == "__main__":
    main()