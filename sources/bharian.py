# import requests

# def fetch_bharian():

#     url = "https://www.bharian.com.my/api/articles?sttl=true&page_size=5"

#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }

#     res = requests.get(url, headers=headers)
#     data = res.json()

#     articles = []

#     for item in data:

#         articles.append({
#             "title": item.get("title"),
#             "url": item.get("url") or item.get("link"),
#             "content": item.get("content", ""),
#             "source": "Bharian",

#             # ⚠️ API通常没有 image，这里先安全处理
#             "image": item.get("image") or item.get("thumbnail")
#         })

#     return articles

from core.http import safe_get

def fetch_bharian():

    url = "https://www.bharian.com.my/api/articles?sttl=true&page_size=5"

    res = safe_get(url)

    if not res:
        return []

    try:
        data = res.json()
    except:
        print("[Bharian] JSON failed fallback")
        return []

    articles = []

    if isinstance(data, list):

        for item in data:

            articles.append({
                "title": item.get("title"),
                "url": item.get("url") or item.get("link"),
                "content": "",
                "source": "Bharian",
                "image": None
            })

    return articles