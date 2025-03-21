import requests
import time
import json
import os
from tqdm import tqdm

BASE_URL = "http://35.200.185.69:8000"
VERSIONS = ["/v1", "/v2", "/v3"]
ENDPOINT = "/autocomplete?query="
LETTERS = "abc"
NUMBERS = "01"
CHARS = LETTERS + NUMBERS
REMAINING=[]

RESULTS_FILE = "all_names.json"
STATS_FILE = "stats.json"

all_names = {v: [] for v in VERSIONS}

stats = {
    version: {
        "names_found": len(all_names.get(version, [])),
        "searches_made": 0
    }
    for version in VERSIONS
}

REMAINING=list(CHARS)


def fetch_names(version, prefix):
    url = BASE_URL + version + ENDPOINT + prefix
    while True:
        try:
            response = requests.get(url)
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
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)
    print("Progress saved.")

def solve():
    while REMAINING:
        prefix = REMAINING.pop()
        for version in VERSIONS:
            stats[version]["searches_made"] += 1
            results = fetch_names(version, prefix)

            if not results:
                continue

            if len(results) < 10:
                for name in results:
                    if name not in all_names[version]:
                        all_names[version].append(name)
                        stats[version]["names_found"] += 1
            else:
                for char in CHARS:
                    next_prefix = prefix + char
                    if next_prefix not in REMAINING:
                        REMAINING.append(next_prefix)

        total_found = sum(len(v) for v in all_names.values())
        if total_found % 100 == 0:
            save_progress()
            print(f"Saved progress. Total names found so far: {total_found}")

    save_progress()
    print(f"Extraction complete.\n")
    for version in VERSIONS:
        print(f"{version}: {stats[version]['names_found']} names found in {stats[version]['searches_made']} searches.")
            

if __name__ == "__main__":
    solve()
