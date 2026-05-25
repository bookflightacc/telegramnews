import asyncio

from sources.bharian import fetch_bharian
from sources.sinchew import fetch_sinchew
from core.extractor import extract_content
from core.ai import generate_news
from core.telegram import send_post
from core.db import already_posted, save_posted	

def get_all_news():

    try:
        bh = fetch_bharian()
    except Exception as e:
        print("Bharian failed:", e)
        bh = []

    try:
        sc = fetch_sinchew()
    except Exception as e:
        print("Sinchew failed:", e)
        sc = []

    return bh + sc


async def main():
    news_list = get_all_news()

    for news in news_list:

        try:

            # --------------------------
            # 0. validate news
            # --------------------------
            if not isinstance(news, dict):
                print("Skip invalid news:", news)
                continue

            if not news.get("url"):
                print("Skip no url:", news)
                continue

            # --------------------------
            # 1. dedup check
            # --------------------------
            if already_posted(news["url"]):
                print("Skipped:", news.get("title"))
                continue

            # --------------------------
            # 2. extract content safely
            # --------------------------
            detail = extract_content(news["url"])

            if not isinstance(detail, dict):
                print("Bad detail:", detail)
                continue

            news["content"] = detail.get("content", "")
            news["image"] = detail.get("image", None)

            # --------------------------
            # 3. AI (safe)
            # --------------------------
            result = generate_news(news)

            if not isinstance(result, dict):
                print("AI failed:", result)
                continue

            # --------------------------
            # 4. formatter
            # --------------------------
            msg = f"""
        📌 {result.get('hashtags', '#新闻')}

        🔥 {result.get('title_cn', news.get('title', ''))}
        {result.get('content_cn', '')}

        🇲🇾 {result.get('title_ms', '')}
        {result.get('content_ms', '')}

        ━━━━━━━━━━━━━━
        📢 关注大事件频道➡️@Malaysia_New  

        📡 https://whatsapp.com/channel/0029Vb7xVrFFMqrOgMRT8p2T
        """

            msg = msg[:1000]

            # --------------------------
            # 5. send telegram
            # --------------------------
            await send_post(
                caption=msg,
                image=news.get("image")
            )

            print("Sent:", news.get("title"))

            save_posted(news["url"])

            await asyncio.sleep(5)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())