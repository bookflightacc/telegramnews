import requests
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Accept": "application/json,text/html,*/*",
    "Connection": "keep-alive"
}

def safe_get(url, retries=3, timeout=10):

    for i in range(retries):
        try:
            res = requests.get(url, headers=HEADERS, timeout=timeout)

            if res.status_code == 200:
                return res

            print(f"[HTTP WARN] {url} -> {res.status_code}")

        except Exception as e:
            print(f"[HTTP ERROR] {url} -> {e}")

        time.sleep(2)

    return None
