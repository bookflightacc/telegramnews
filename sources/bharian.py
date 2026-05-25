import requests

def fetch_bharian():

    url = "https://www.bharian.com.my/api/articles?sttl=true&page_size=5"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    articles = []

    for item in data:

        articles.append({
            "title": item.get("title"),
            "url": item.get("url") or item.get("link"),
            "content": item.get("content", ""),
            "source": "Bharian",

            # ⚠️ API通常没有 image，这里先安全处理
            "image": item.get("image") or item.get("thumbnail")
        })

    return articles