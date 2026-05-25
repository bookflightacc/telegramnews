import requests
from bs4 import BeautifulSoup

url = "https://www.bharian.com.my/berita/kes"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)

print("STATUS:", res.status_code)

soup = BeautifulSoup(res.text, "html.parser")

all_links = []

for a in soup.find_all("a"):
    href = a.get("href")
    if href:
        all_links.append(href)

print("TOTAL RAW LINKS:", len(all_links))

print("\nSAMPLE LINKS:")
for i in all_links[:30]:
    print(i)