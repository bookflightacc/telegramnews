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

import requests

def fetch_bharian():

    url = "https://www.bharian.com.my/api/articles?sttl=true&page_size=5"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        print("Bharian blocked:", res.status_code)
        return []

    try:
        data = res.json()
    except Exception:
        print("Bharian not JSON")
        return []

    articles = []

    # -------------------------
    # CASE 1: direct list
    # -------------------------
    if isinstance(data, list):
        items = data

    # -------------------------
    # CASE 2: dict wrapper
    # -------------------------
    elif isinstance(data, dict):
        items = data.get("data") or data.get("articles") or []

    else:
        return []

    # -------------------------
    # FINAL SAFE LOOP
    # -------------------------
    for item in items:

        if not isinstance(item, dict):
            continue

        articles.append({
            "title": item.get("title"),
            "url": item.get("url") or item.get("link"),
            "content": "",
            "source": "Bharian",
            "image": item.get("image")
        })

    return articles