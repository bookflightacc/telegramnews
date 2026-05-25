import cloudscraper

def fetch_sinchew():

    scraper = cloudscraper.create_scraper()

    url = "https://www.sinchew.com.my/hot-post-list/?taxid=-1"

    # STEP 1: warm up session (IMPORTANT for CI)
    scraper.get("https://www.sinchew.com.my/hot-posts")

    # STEP 2: minimal headers ONLY
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = scraper.get(url, headers=headers, timeout=30)

    print("STATUS:", res.status_code)

    # DEBUG (important in GitHub Actions)
    print("TEXT SAMPLE:", res.text[:200])

    if res.status_code != 200:
        return []

    try:
        data = res.json()
    except Exception as e:
        print("JSON ERROR:", e)
        return []

    if "zero" not in data:
        print("NOT VALID JSON RESPONSE")
        return []

    articles = []

    for item in data["zero"]:
        articles.append({
            "title": item.get("post_title"),
            "url": item.get("the_permalink"),
            "image": item.get("image"),
            "content": "",
            "source": "Sinchew"
        })

    return articles