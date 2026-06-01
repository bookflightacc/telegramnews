import asyncio

from sources.bharian import fetch_bharian
from sources.sinchew import fetch_sinchew
from core.extractor import extract_content
from core.ai import generate_news
from core.telegram import send_post
from core.db import already_posted, save_posted	

async def get_all_news():

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
    news_list = await get_all_news()
    
    for news in news_list:

        try:
            # 1. get full article
            content = extract_content(news["url"])

            if already_posted(news["url"]):
                print("Skipped:", news["title"])
                continue
            news["content"] = content

            # 2. AI
            result = generate_news(news)

            # 3. formatter
            msg = f"""
<b>{result['hashtags']}</b>

<b>📰 {result['title_cn']}</b>
{result['content_cn']}

<b>🇲🇾 {result['title_ms']}</b>
{result['content_ms']}

━━━━━━━━━━━━━━
📢 关注新闻频道 <a href="https://t.me/Malaysia_New">@Malaysia_New</a>
📡 <a href="https://whatsapp.com/channel/0029Vb7xVrFFMqrOgMRT8p2T">关注WhatsApp频道</a>
🌐 投稿 Penyerahan artikel <a href="https://t.me/MK_DEE96">@MK_DEE96</a>
🎉 娱乐城 <a href="https://t.me/freekredit66">@freecredit66</a>
"""
            msg = msg[:1000]

            # 4. send to Telegram
            await send_post(
                caption=msg,
                image=news.get("image"),
                parse_mode= "HTML"
            )

            print("Sent:", news["title"])
            save_posted(news["url"])
            await asyncio.sleep(5)

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    asyncio.run(main())