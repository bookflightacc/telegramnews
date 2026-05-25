import requests

def fetch_sinchew():
    url = "https://www.sinchew.com.my/hot-post-list/?taxid=-1"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.sinchew.com.my/hot-posts"
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    articles = []

    items = data.get("zero", [])

    for item in items:
        title = item.get("post_title")
        url = item.get("the_permalink")

        articles.append({
    		"title": title,
    		"url": url,
    		"content": "",
    		"source": "Sinchew",
    		"image": item.get("image")   # ✔ 必须有
        })
    return articles