import requests

url = "https://www.bharian.com.my/api/articles?sttl=true&page_size=8"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

res = requests.get(url, headers=headers)

print("STATUS:", res.status_code)

data = res.json()

print("TYPE:", type(data))

# 如果是 list
if isinstance(data, list):
    print("TOTAL ARTICLES:", len(data))

    for i, a in enumerate(data[:5]):
        print("\n---")
        print("TITLE:", a.get("title"))
        print("URL:", a.get("url") or a.get("link"))

# 如果是 dict（备用）
else:
    print("KEYS:", data.keys())