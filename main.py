import requests
import time
import json
import os
from tqdm import tqdm

proxies = {
    "http": "http://edcguest:edcguest@172.31.102.29:3128",
    "https": "http://edcguest:edcguest@172.31.102.29:3128"
}

BASE_URL = "http://35.200.185.69:8000"
VERSIONS = ["/v1", "/v2", "/v3"]
ENDPOINT = "/autocomplete?query="
LETTERS = "abcdefghijklmnopqrstuvwxyz"
NUMBERS = "0123456789"
SPECIAL="-."
CHARS={
    VERSIONS[0]: list(LETTERS),
    VERSIONS[1]: list(LETTERS+NUMBERS),
    VERSIONS[2]: list(LETTERS+NUMBERS+SPECIAL)
}

RESULTS_FILE = "all_names.json"
STATS_FILE = "stats.json"
REMAINING_FILE="remaining.json"

#if file exist load the previously done task
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, 'r') as f:
        all_names = json.load(f)
else:
    all_names = {v: [] for v in VERSIONS}

if os.path.exists(STATS_FILE):
    with open(STATS_FILE, 'r') as f:
        stats = json.load(f)
else:
    stats = {
        version: {
            "names_found": len(all_names.get(version, [])),
            "searches_made": 0
        }
        for version in VERSIONS
    }

if os.path.exists(REMAINING_FILE):
    with open(REMAINING_FILE, 'r') as f:
        remaining = json.load(f)
else:
    remaining={
        VERSIONS[0]: list(LETTERS),
        VERSIONS[1]: list(LETTERS+NUMBERS),
        VERSIONS[2]: list(LETTERS+NUMBERS+SPECIAL)
    }

def fetch_names(version, prefix):
    url = BASE_URL + version + ENDPOINT + prefix
    while True:
        try:
            response = requests.get(url, proxies=proxies)
            if response.status_code == 429:
                print("Rate limited. Waiting for 10s..")
                time.sleep(10)
                continue
            elif response.status_code == 404:
                print(f"Endpoint not found: {url}")
                return []
            response.raise_for_status()
            data = response.json()
            print(data)
            return data["results"]
        except Exception as e:
            print(f"Error for {url}: {e}. Retrying in 5s...")
            time.sleep(5)

def save_progress():
    with open(RESULTS_FILE, 'w') as f:
        json.dump(all_names, f, indent=2)
    with open(REMAINING_FILE, 'w') as f:
        json.dump(remaining, f, indent=2)
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)
    print("Progress saved.")

def solve():
    previous_found = 0 
    TEMP=VERSIONS.copy()
    while TEMP:
        for version in TEMP:
            if not version in remaining:
                TEMP.remove(version)
                continue
            stats[version]["searches_made"] += 1
            
            if not remaining[version] :
                del remaining[version]
                TEMP.remove(version)
                continue
            prefix=remaining[version].pop()
            
            results = fetch_names(version, prefix)
            if not results:
                continue
            if len(results) < 10:
                for name in results:
                    if name not in all_names[version]:
                        all_names[version].append(name)
                        stats[version]["names_found"] += 1
            else:
                for char in CHARS[version]:
                    next_prefix = prefix + char
                    if next_prefix not in remaining[version]:
                        remaining[version].append(next_prefix)
        total_found = sum(len(v) for v in all_names.values())
        if (total_found - previous_found) > 100 :
            previous_found = total_found
            save_progress()
            print(f"Saved progress. Total names found so far: {total_found}")
    save_progress()
    print(f"Extraction complete.\n")
    for version in VERSIONS:
        print(f"{version}: {stats[version]['names_found']} names found in {stats[version]['searches_made']} searches.")
            

if __name__ == "__main__":
    solve()
