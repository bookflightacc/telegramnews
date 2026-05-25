import cloudscraper
import time

def fetch_sinchew_scraper():
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "darwin",
            "mobile": False
        }
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
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    res = scraper.get(api_url, headers=headers, timeout=30)
    print("STATUS:", res.status_code)
    print("TEXT SAMPLE:", res.text[:300])

    if res.status_code != 200:
        return []

    try:
        data = res.json()
    except Exception as e:
        print("JSON ERROR:", e)
        return []

    if "zero" not in data:
        print("UNEXPECTED JSON STRUCTURE:", list(data.keys()))
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

    print(f"Fetched {len(articles)} articles from Sin Chew")
    return articles


def fetch_sinchew():
    return fetch_sinchew_scraper()