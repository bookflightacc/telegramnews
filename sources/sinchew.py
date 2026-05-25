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

import cloudscraper

def fetch_sinchew():

    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "darwin",
            "mobile": False
        }
    )

    headers = {
        "accept": "*/*",
        "accept-language": "zh-MY,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "referer": "https://www.sinchew.com.my/hot-posts",
        "x-requested-with": "XMLHttpRequest",
        "user-agent": "Mozilla/5.0"
    }

    url = "https://www.sinchew.com.my/hot-post-list/?taxid=-1"

    res = scraper.get(url, headers=headers)

    print("STATUS:", res.status_code)

    if res.status_code != 200:
        return []

    try:
        data = res.json()
    except Exception as e:
        print("JSON ERROR:", e)
        return []

    articles = []

    for item in data.get("zero", []):

        title = item.get("post_title")
        link = item.get("the_permalink")

        if not title or not link:
            continue

        articles.append({
            "title": title,
            "url": link,
            "image": item.get("image"),
            "content": "",
            "source": "Sinchew"
        })

    return articles