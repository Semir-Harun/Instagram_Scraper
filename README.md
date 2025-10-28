# 📸 Instagram Profile Scraper# Instagram_Scraper



A Python-based automation tool to scrape public Instagram profile data using Selenium. This project uses your existing Chrome login session to bypass login and scrape visible profile data.# Instagram Profile Scraper



---A Python script to scrape an Instagram profile’s description and profile picture URL using Selenium.  

This approach uses your real Chrome browser session to bypass Instagram’s restrictions on bots.

## ⚙️ Features

---

- 🔐 Uses your logged-in Chrome profile for authentication

- 🧾 Extracts:## 🚀 Features

  - Name

  - Bio✅ Fetch Instagram profile description (followers, following, posts).  

  - Followers / Following count✅ Fetch and display the profile picture URL.  

  - Posts count✅ Works even when Instagram blocks standard HTTP requests.  

  - Website URL✅ Uses your logged-in Chrome session — no need to manually handle cookies or tokens.

  - Profile picture URL

- 💾 Saves results to JSON in `data/` folder---

- 🧪 Built with Selenium & modern Python practices

- 🛡️ Error handling and validation## 🔧 Requirements

- 📱 Professional CLI interface

- Python 3.7+

---- Google Chrome (installed & logged in to Instagram)

- ChromeDriver (automatically managed by Selenium if installed properly)

## 🧰 Tech Stack- Selenium



- Python 3.7+---

- Selenium WebDriver

- Chrome Browser + ChromeDriver## 📦 Installation

- JSON for data storage

1️⃣ Clone this repository:

---```bash

git clone https://github.com/yourusername/instagram-profile-scraper.git

## 📦 Setupcd instagram-profile-scraper



### 1. Clone the repository-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

```bash

git clone https://github.com/Semir-Harun/Instagram_Scraper#2

cd Instagram_Scraperinstall packages

```pip install -r requirements.txt

Execute Program

### 2. Install dependenciespython InstgramProfile.py <username>

```bashSample run

pip install -r requirements.txt
```

### 3. Update Chrome profile path (Optional)
By default, the scraper automatically detects your Chrome profile. If needed, you can manually specify the path in `instagram_scraper.py`:

**Windows Default:**
```
C:/Users/<your_username>/AppData/Local/Google/Chrome/User Data
```

**macOS Default:**
```
~/Library/Application Support/Google/Chrome/
```

**Linux Default:**
```
~/.config/google-chrome/
```

---

## 🚀 Usage

### Basic Usage
```bash
python instagram_scraper.py <instagram_username>
```

### Advanced Options
```bash
# Save as both JSON and CSV
python instagram_scraper.py nasa --csv

# Download profile picture
python instagram_scraper.py nasa --download-pic

# Run in headless mode (no browser window)
python instagram_scraper.py nasa --headless

# Custom output directories
python instagram_scraper.py nasa --output-dir ./results --screenshots-dir ./pics

# All features combined
python instagram_scraper.py nasa --csv --download-pic --headless --output-dir ./results
```

### Examples Script
Run the interactive examples script to see all features in action:
```bash
python examples.py
```

---

## 📄 Output

### Console Output
```
🚀 Starting Instagram scraper for: @nasa
🔧 Loading Chrome driver...
🔍 Navigating to: https://www.instagram.com/nasa/
✅ Successfully scraped profile data
💾 Profile data saved to: data/profile_nasa.json

==================================================
📸 INSTAGRAM PROFILE SUMMARY
==================================================
👤 Username: @nasa
📝 Name: NASA
📄 Bio: Explore the universe and our home planet 🌌🌎
📊 Posts: 4,424
👥 Followers: 97.2M
🔗 Following: 72
🌐 Website: https://nasa.gov
🔗 Profile URL: https://www.instagram.com/nasa/
==================================================
```

### JSON Output
Data is saved to `./data/profile_<username>.json`:

```json
{
  "success": true,
  "username": "nasa",
  "profile_url": "https://www.instagram.com/nasa/",
  "scraped_at": "2025-10-28T19:45:30.123456",
  "name": "NASA",
  "bio": "Explore the universe and our home planet 🌌🌎",
  "followers": "97.2M",
  "following": "72",
  "posts": "4,424",
  "website": "https://nasa.gov",
  "profile_pic_url": "https://instagram.com/profile_pic_url..."
}
```

---

## 📁 Project Structure

```
Instagram_Scraper/
├── instagram_scraper.py    # Main scraper script
├── data/                   # JSON output files
│   └── profile_<username>.json
├── screenshots/            # Optional: profile pictures
│   └── <username>.png
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
└── InstagramScraper/     # Legacy files (kept for reference)
    ├── Instagramprofile.py
    ├── Instagram_scraper.py
    ├── main.py
    └── Profilepic.py
```

---

## 🔧 How It Works

1. **Chrome Profile Authentication**: Uses your existing logged-in Chrome session to bypass Instagram's bot detection
2. **Selenium Navigation**: Navigates to the target Instagram profile URL
3. **Data Extraction**: Uses XPath selectors to extract profile information from the page
4. **Error Handling**: Gracefully handles missing elements, private profiles, and network issues
5. **Data Storage**: Saves structured data as JSON with timestamps

---

## ⚠️ Important Notes

### Rate Limiting
- Instagram may temporarily block requests if you scrape too aggressively
- Add delays between requests if scraping multiple profiles
- Respect Instagram's robots.txt and terms of service

### Profile Accessibility
- ✅ Works with public profiles
- ❌ Cannot scrape private profiles (unless you follow them)
- ❌ Cannot scrape profiles that have blocked you

### Chrome Requirements
- Must have Google Chrome installed
- Must be logged into Instagram in Chrome
- ChromeDriver will be automatically managed by selenium

---

## 🛠️ Troubleshooting

### Common Issues

**"ChromeDriver not found"**
```bash
# Install ChromeDriver automatically
pip install webdriver-manager
```

**"Profile not found"**
- Check if the username is correct
- Verify the profile is public
- Ensure you're logged into Instagram in Chrome

**"Could not find elements"**
- Instagram may have changed their HTML structure
- Try updating to the latest version of the scraper
- Check if Instagram is blocking the request

---

## 🧪 Testing

Test the scraper with a known public profile:

```bash
python instagram_scraper.py nasa
```

Expected behavior:
- Browser opens briefly
- Data is extracted and saved
- JSON file appears in `data/` folder

---

## 🚨 Legal Disclaimer

⚠️ **This tool is for educational purposes only.**

- Respect Instagram's Terms of Service
- Do not scrape private data without permission
- Use responsibly and ethically
- Consider Instagram's API for commercial use
- Be aware of applicable privacy laws (GDPR, CCPA, etc.)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📜 License

MIT License - see LICENSE file for details

---

## 🧑‍💻 Author

**Semir Harun**  
🔗 [GitHub Profile](https://github.com/Semir-Harun)

---

## 🔄 Version History

- **v2.0.0** - Professional refactor with modular functions, error handling, and improved UX
- **v1.0.0** - Initial release with basic scraping functionality

---

## 💡 Future Enhancements

- [ ] 📸 Download profile pictures to `screenshots/` folder
- [ ] 📊 Export data to CSV format
- [ ] 🧪 Add unit tests
- [ ] 🤖 Add GitHub Actions CI/CD
- [ ] 🔄 Batch processing for multiple usernames
- [ ] 📈 Add progress bars for long operations
- [ ] 🔍 Add post content scraping capabilities