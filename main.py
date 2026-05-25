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
            # 1. get full article
            # content = extract_content(news["url"])
            

            if already_posted(news["url"]):
                print("Skipped:", news["title"])
                continue
            # news["content"] = content
            detail = extract_content(news["url"])

            news["content"] = detail["content"]
            news["image"] = detail["image"]
            # 2. AI
            result = generate_news(news)

            # 3. formatter
            msg = f"""
📌 {result['hashtags']}

🔥 {result['title_cn']}
{result['content_cn']}

🇲🇾 {result['title_ms']}
{result['content_ms']}

━━━━━━━━━━━━━━
📢 关注大事件频道➡️@Malaysia_New  

📡 https://whatsapp.com/channel/0029Vb7xVrFFMqrOgMRT8p2T
"""
            msg = msg[:1000]

            # 4. send to Telegram
            await send_post(
                caption=msg,
                image=news.get("image")
            )

            print("Sent:", news["title"])
            save_posted(news["url"])
            await asyncio.sleep(5)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())