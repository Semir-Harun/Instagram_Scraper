from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Path to your Chrome profile (so you stay logged in)
profile_path = r"C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data"

options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_path}")

driver = webdriver.Chrome(options=options)

username = input("Enter Instagram username: ").strip()
driver.get(f"https://www.instagram.com/{username}/")

time.sleep(5)  # wait for page to load

# Get profile description
try:
    desc = driver.find_element(By.XPATH, '//meta[@name="description"]')
    print("Description:", desc.get_attribute("content"))
except:
    print("Could not find description")

# Get profile pic
try:
    pic = driver.find_element(By.XPATH, '//meta[@property="og:image"]')
    print("Profile Pic:", pic.get_attribute("content"))
except:
    print("Could not find profile pic")

driver.quit()

