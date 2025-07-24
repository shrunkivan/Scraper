import json
import time
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# Configuration
REPO_DIR = "C:\\Users\\ivand\\Desktop\\Skull\\Shrunk Internship\\Scraper"
COMPETITIONS = {
    "VFL": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647967-0&pool=1&a=LADDER",
    "VFLW": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647968-0&pool=1&a=LADDER",
    "SANFL": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647969-0&pool=1&a=LADDER",
    "SANFLW": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647970-0&pool=1&a=LADDER",
    "SANFL_Reserves": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647971-0&pool=1&a=LADDER",
    "WAFL": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647972-0&pool=1&a=LADDER",
    "WAFLW": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647973-0&pool=1&a=LADDER",
    "WAFL_Reserves": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647974-0&pool=1&a=LADDER",
    "U18_National": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647975-0&pool=1&a=LADDER",
    "U18_Talent_League": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647976-0&pool=1&a=LADDER",
    "U18_SANFL": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647977-0&pool=1&a=LADDER",
    "U18_WAFL": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647978-0&pool=1&a=LADDER",
    "U16_Talent_League": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647979-0&pool=1&a=LADDER",
    "U16_SANFL": "https://websites.mygameday.app/comp_info.cgi?c=0-118-0-647980-0&pool=1&a=LADDER"
}

def fetch_ladder(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    service = Service()

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)
    time.sleep(5)  # Allow page to load

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    table = soup.find('table', class_='tableClass stats-table ranked')
    if not table:
        print(f"❌ Ladder table not found at {url}")
        return []

    data = []
    for row in table.find_all('tr', class_=['odd', 'even']):
        cols = row.find_all('td')
        if len(cols) < 12:
            continue
        data.append({
            "POS": cols[0].text.strip(),
            "TEAM": cols[1].text.strip(),
            "P": int(cols[2].text.strip()),
            "W": int(cols[3].text.strip()),
            "L": int(cols[4].text.strip()),
            "D": int(cols[5].text.strip()),
            "B": int(cols[6].text.strip()),
            "F": int(cols[7].text.strip()),
            "AGST": int(cols[8].text.strip()),
            "PCT": float(cols[9].text.strip()),
            "PTS": int(cols[11].text.strip())
        })

    return data

def save_to_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Saved ladder to {path}")

def git_commit_and_push(repo_dir, filename, competition):
    subprocess.run(["git", "-C", repo_dir, "add", filename], check=True)
    subprocess.run(["git", "-C", repo_dir, "commit", "-m", f"Update {competition} ladder"], check=True)
    subprocess.run(["git", "-C", repo_dir, "push"], check=True)
    print(f"✅ Git commit and push completed for {competition}.")

if __name__ == "__main__":
    for competition, url in COMPETITIONS.items():
        output_path = os.path.join(REPO_DIR, f"{competition}ladder.json")
        ladder_data = fetch_ladder(url)
        
        if ladder_data:
            save_to_json(ladder_data, output_path)
            git_commit_and_push(REPO_DIR, f"{competition}ladder.json", competition)
        else:
            print(f"❌ Failed to retrieve {competition} ladder data.")