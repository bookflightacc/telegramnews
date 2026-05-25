import requests

url = "https://www.sinchew.com.my/hot-post-list/?taxid=-1"

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.sinchew.com.my/hot-posts"
}

res = requests.get(url, headers=headers)

print("STATUS:", res.status_code)
print("CONTENT PREVIEW:\n", res.text[:500])