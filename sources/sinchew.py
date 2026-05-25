import cloudscraper
import time
import feedparser

def fetch_sinchew_scraper():
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "darwin", "mobile": False}
    )

    api_url = "https://www.sinchew.com.my/hot-post-list/?taxid=-1"

    print("Warming up session...")
    scraper.get("https://www.sinchew.com.my/", timeout=30)
    time.sleep(2)
    scraper.get("https://www.sinchew.com.my/hot-posts/", timeout=30)
    time.sleep(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.sinchew.com.my/hot-posts/",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    }

    res = scraper.get(api_url, headers=headers, timeout=30)
    print("Scraper STATUS:", res.status_code)

    if res.status_code != 200:
        return []

    try:
        data = res.json()
    except Exception as e:
        print("JSON ERROR:", e)
        return []

    if "zero" not in data:
        return []

    return [
        {
            "title":   item.get("post_title"),
            "url":     item.get("the_permalink"),
            "image":   item.get("image"),
            "content": "",
            "source":  "Sinchew"
        }
        for item in data["zero"]
    ]


def fetch_sinchew_rss():
    print("Trying Sin Chew RSS fallback...")
    feed = feedparser.parse("https://www.sinchew.com.my/feed/")

    if not feed.entries:
        print("RSS also empty — Sin Chew unreachable")
        return []

    articles = []
    for entry in feed.entries[:10]:
        # extract image from media_content or enclosures
        image = ""
        if hasattr(entry, "media_content") and entry.media_content:
            image = entry.media_content[0].get("url", "")
        elif hasattr(entry, "enclosures") and entry.enclosures:
            image = entry.enclosures[0].get("url", "")

        articles.append({
            "title":   entry.title,
            "url":     entry.link,
            "image":   image,
            "content": entry.get("summary", ""),  # RSS gives summary as content
            "source":  "Sinchew"
        })

    print(f"RSS fetched {len(articles)} articles from Sin Chew")
    return articles


def fetch_sinchew():
    articles = fetch_sinchew_scraper()
    if not articles:
        print("Scraper blocked, falling back to RSS...")
        articles = fetch_sinchew_rss()
    return articles