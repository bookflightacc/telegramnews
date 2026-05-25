import json
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
        "user-agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/147.0.0.0 Safari/537.36"
        )
    }

    url = "https://www.sinchew.com.my/hot-post-list/?taxid=-1"

    try:

        # Optional: visit homepage first
        scraper.get("https://www.sinchew.com.my", headers=headers)

        res = scraper.get(url, headers=headers)

        print("\n==============================")
        print("STATUS:", res.status_code)
        print("CONTENT-TYPE:", res.headers.get("content-type"))
        print("==============================\n")

        # DEBUG preview
        print("FIRST 500 CHARS:\n")
        print(res.text[:500])
        print("\n==============================\n")

        if res.status_code != 200:
            print("FAILED REQUEST")
            return []

        try:
            data = res.json()
        except Exception as e:
            print("JSON PARSE ERROR:", e)
            return []

        if "zero" not in data:
            print("INVALID JSON STRUCTURE")
            return []

        articles = []

        for item in data.get("zero", []):

            title = item.get("post_title")
            link = item.get("the_permalink")
            image = item.get("image")

            if not title or not link:
                continue

            articles.append({
                "title": title,
                "url": link,
                "image": image,
                "source": "Sinchew"
            })

        return articles

    except Exception as e:
        print("FETCH ERROR:", e)
        return []


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    news = fetch_sinchew()

    print(f"\nTOTAL ARTICLES: {len(news)}\n")

    for i, item in enumerate(news[:10], 1):

        print("=" * 60)
        print(f"{i}. TITLE:")
        print(item["title"])

        print("\nURL:")
        print(item["url"])

        print("\nIMAGE:")
        print(item["image"])

        print("=" * 60)
        print()