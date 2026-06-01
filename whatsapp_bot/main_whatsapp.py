import asyncio
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.ai import generate_news
from core.extractor import extract_content
from sources.bharian import fetch_bharian
from sources.sinchew import fetch_sinchew
from whatsapp_bot.db import already_posted, save_posted
from whatsapp_bot.send_whatsapp import send_whatsapp_post


def get_all_news():
    news = []

    try:
        news += fetch_bharian()
    except Exception as e:
        print("Bharian failed:", e)

    try:
        news += fetch_sinchew()
    except Exception as e:
        print("Sinchew failed:", e)

    return news


def apply_article_detail(news):
    detail = extract_content(news["url"])

    if isinstance(detail, dict):
        news["content"] = detail.get("content", "")

        if not news.get("image"):
            news["image"] = detail.get("image")
    else:
        news["content"] = detail or ""


def format_whatsapp_message(result):
    return f"""{result['hashtags']}

📰 {result['title_cn']}
{result['content_cn']}

🇲🇾 {result['title_ms']}
{result['content_ms']}

━━━━━━━━━━━━━━
📢 关注新闻频道 https://t.me/Malaysia_New
📡 关注WhatsApp频道 https://whatsapp.com/channel/0029Vb7xVrFFMqrOgMRT8p2T
🌐 投稿 Penyerahan artikel https://t.me/MK_DEE96
🎉 娱乐城 https://t.me/freekredit66
""".strip()


async def main():
    for news in get_all_news():
        try:
            if already_posted(news["url"]):
                print("Skipped:", news["title"])
                continue

            apply_article_detail(news)
            result = generate_news(news)
            msg = format_whatsapp_message(result)

            send_whatsapp_post(
                caption=msg[:1024],
                image=news.get("image"),
            )

            print("Sent WhatsApp:", news["title"])
            save_posted(news["url"])
            await asyncio.sleep(5)

        except Exception as e:
            print("WhatsApp error:", e)


if __name__ == "__main__":
    asyncio.run(main())
