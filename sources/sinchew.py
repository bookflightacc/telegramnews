# import requests

# def fetch_sinchew():
#     url = "https://www.sinchew.com.my/hot-post-list/?taxid=-1"

#     headers = {
#         "User-Agent": "Mozilla/5.0",
#         "Referer": "https://www.sinchew.com.my/hot-posts"
#     }

#     res = requests.get(url, headers=headers)
#     data = res.json()

#     articles = []

#     items = data.get("zero", [])

#     for item in items:
#         title = item.get("post_title")
#         url = item.get("the_permalink")

#         articles.append({
#     		"title": title,
#     		"url": url,
#     		"content": "",
#     		"source": "Sinchew",
#     		"image": item.get("image")   # ✔ 必须有
#         })
#     return articles
# import json
# from bs4 import BeautifulSoup
# from core.http import safe_get

# def fetch_sinchew():

#     url = "https://www.sinchew.com.my/hot-post-list/?taxid=-1"

#     res = safe_get(url)

#     if not res:
#         return []

#     data = None

#     # -------------------------
#     # TRY JSON MODE FIRST
#     # -------------------------
#     try:
#         data = res.json()
#     except:
#         data = None

#     articles = []

#     # -------------------------
#     # CASE 1: JSON SUCCESS
#     # -------------------------
#     if isinstance(data, dict) and "zero" in data:

#         for item in data.get("zero", []):
#             articles.append({
#                 "title": item.get("post_title"),
#                 "url": item.get("the_permalink"),
#                 "content": "",
#                 "source": "Sinchew",
#                 "image": item.get("image")
#             })

#         return articles

#     # -------------------------
#     # CASE 2: FALLBACK HTML PARSE
#     # -------------------------
#     soup = BeautifulSoup(res.text, "html.parser")

#     for a in soup.find_all("a", href=True):

#         href = a["href"]
#         title = a.get_text(strip=True)

#         if "sinchew.com.my" in href and title:

#             articles.append({
#                 "title": title,
#                 "url": href,
#                 "content": "",
#                 "source": "Sinchew"
#             })

#     return articles

from core.http import safe_get

def fetch_sinchew():

    # 1️⃣ primary API (often blocked)
    url_api = "https://www.sinchew.com.my/hot-post-list/?taxid=-1"

    res = safe_get(url_api)

    if res:

        try:
            data = res.json()

            if isinstance(data, dict) and "zero" in data:

                return [
                    {
                        "title": x.get("post_title"),
                        "url": x.get("the_permalink"),
                        "image": x.get("image"),
                        "source": "Sinchew"
                    }
                    for x in data["zero"]
                ]

        except:
            pass

    print("[Sinchew] API failed → fallback HTML")

    # 2️⃣ fallback HTML mode
    url_html = "https://www.sinchew.com.my/hot-posts"

    res = safe_get(url_html)

    if not res:
        return []

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(res.text, "html.parser")

    articles = []

    for a in soup.find_all("a", href=True):

        if "sinchew.com.my" in a["href"]:

            articles.append({
                "title": a.get_text(strip=True),
                "url": a["href"],
                "image": None,
                "source": "Sinchew"
            })

    return articles