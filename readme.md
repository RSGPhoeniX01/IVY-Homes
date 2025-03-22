# Autocomplete API By IVY Homes

## Overview
This project is made to explore and extract data from an autocomplete API endpoint.

### Endpoint Provided:
http://35.200.185.69:8000/v3/autocomplete?query=<string>


## Initial Exploration
- I started by making requests to the given endpoint with simple single characters like `a, b, c, d`, etc.
- I noticed that for each request, the response included three main details: version, count, and results.
- Changing the version in the URL to `v2, v3, v4, v5, v0` give responses only from versions `v1, v2, and v3`. No data was found for other versions.
- The API returned a maximum of 10 results for each query. If fewer than 10 results were received, that meant no further results were available for that prefix. If 10 results came in, there could be more results so need to explore deeper strings.

## My First Approach (Brute Force)
- I used characters from `a-z` and numbers from `0-9` to form query strings.
- If the response returned less than 10 results, I saved those names as they were complete. and no further searching for that prefix
- If I got exactly 10 results, I explored further by appending more characters to that prefix and continued searching.
- This brute force approach checked all possibilities and was inefficient.

## Drawbacks
- After observation:
  - `v1` contains only alphabets.
  - `v2` contains alphabets and numbers.
  - `v3` contains alphabets, numbers, and special characters (`+`, `-`, `.`).
- Searching blindly among all possibilities wasted a lot of time and API calls.

## Modified Approach (Optimal Searching)
- I created three separate lists to keep track of unexplored strings for each version.
- When a version finished exploring all its strings, it was removed from further searching.
- This approach saved time and avoided unnecessary API calls, (reducing time lapse in the rate limit which is 100 instructions per minute).

### Drawback of the Modified Approach
- The process still took a long time to complete.
- To prevent data loss if interrupted (due to network issues or laptop sleep), I saved the state to files to allow resuming from where it left off.

## Final Solution
- The URL was divided into four parts:
  1. Base URL: `http://35.200.185.69:8000`
  2. Versions: `v1, v2, v3`
  3. Endpoint: `/autocomplete?query=`
  4. Query strings:
     - `v1`: alphabets only
     - `v2`: alphabets and numbers
     - `v3`: alphabets, numbers, and special characters (`+`, `-`, `.`) (but not used `+` as it matches with all characters)

- Before execution, the program checks if progress files exist:
  - `all_names.json` to store found names version-wise.
  - `stats.json` to keep track of searches made and number of names found.
  - `remaining.json` to track unexplored prefixes.

- The script iterates through each version:
  - Constructs the complete URL.
  - If 10 results are returned, it appends all possible next characters to the current string and adds these to the `remaining` list (if not already present) for deeper exploration.
  - If fewer than 10 results are found, the names are saved under their respective version in `all_names` (if not already present). The count of names found for that version is also incremented in `stats`, and the exploration for that prefix is then stopped.

- Progress is saved after every 100 names to avoid data loss.
- i.e `all-names` stored in file `all_names.json`, `REMAININg` stored in `REMAINING.json` & `stats` in `stats.json`

## Key Observations & Findings
- The API returns a maximum of 10 results at a time.
- There is a rate limit of 100 instructions per minute.
- Only three versions are available: `v1`, `v2`, and `v3`.
- `v1` names consist of only alphabets.
- `v2` names consist of alphabets and numbers.
- `v3` names consist of alphabets, numbers, and some special characters (`+`, `-`, `.`).
- Some special characters (like `+`, `#`, `&`) can match with other characters and cause loops. These are avoided.

## Results
**v1:**
- Names found: 18042
- Searches made:

**v2:**
- Names found: 13648
- Searches made:

**v3:**
- Names found: 11165
- Searches made:

Total names found: 42855

