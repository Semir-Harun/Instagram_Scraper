#!/usr/bin/env python3
"""
Instagram Scraper - Example Usage

This script demonstrates various ways to use the Instagram scraper
with different command-line options and features.
"""

import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and display results."""
    print(f"\n🔍 {description}")
    print(f"📝 Command: {command}")
    print("=" * 60)
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    """Run example Instagram scraper commands."""
    print("🚀 Instagram Scraper - Example Usage Demo")
    print("=" * 60)
    
    examples = [
        {
            "command": "python instagram_scraper.py --help",
            "description": "Display help and all available options"
        },
        {
            "command": "python instagram_scraper.py nasa",
            "description": "Basic scraping - JSON output only"
        },
        {
            "command": "python instagram_scraper.py natgeo --csv",
            "description": "Scrape with CSV export"
        },
        {
            "command": "python instagram_scraper.py nasa --download-pic",
            "description": "Scrape with profile picture download"
        },
        {
            "command": "python instagram_scraper.py nasa --csv --download-pic --output-dir ./results",
            "description": "Full featured scraping with custom output directory"
        },
        {
            "command": "python instagram_scraper.py nasa --headless",
            "description": "Headless mode (browser runs in background)"
        }
    ]
    
    print("📋 Available Example Commands:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['description']}")
    
    print("\n" + "=" * 60)
    choice = input("Enter example number to run (1-6) or 'all' to run all: ").strip()
    
    if choice.lower() == 'all':
        for example in examples:
            if not run_command(example["command"], example["description"]):
                print("❌ Command failed, continuing...")
            time.sleep(2)  # Brief pause between commands
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        example = examples[int(choice) - 1]
        run_command(example["command"], example["description"])
    else:
        print("❌ Invalid choice!")
        sys.exit(1)
    
    print("\n✅ Example demonstration complete!")
    print("\n📁 Check the following directories for output:")
    print("   - ./data/          (JSON files)")
    print("   - ./screenshots/   (Profile pictures)")
    print("   - ./results/       (Custom output directory)")

if __name__ == "__main__":
    main()