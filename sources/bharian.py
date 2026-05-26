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
from urllib.parse import urljoin

def get_bharian_image(item):
    for key in ["field_article_images_filtered", "field_article_images"]:
        images = item.get(key)

        if isinstance(images, list) and images:
            image_url = images[0].get("url")
            if image_url:
                return urljoin("https://www.bharian.com.my", image_url)

    for key in [
        "field_image_socialmedia",
        "field_image_listing_featured_v2",
        "field_image_listing_v2",
        "field_image_listing_featured",
        "field_image_portrait",
        "field_image_three_wide_col",
        "image",
        "thumbnail",
    ]:
        image_url = item.get(key)
        if image_url:
            return urljoin("https://www.bharian.com.my", image_url)

    return None

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
            "image": get_bharian_image(item)
        })

    return articles