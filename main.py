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
        print(f"Bharian: {len(bh)} articles")
    except Exception as e:
        print("Bharian failed:", e)
        bh = []

    await asyncio.sleep(2)  # FIX 2: small gap between sources

    try:
        sc = fetch_sinchew()
        print(f"Sinchew: {len(sc)} articles")
    except Exception as e:
        print("Sinchew failed:", e)
        sc = []

    return bh + sc


def format_message(result: dict) -> str:
    """Build Telegram message — safe HTML, no hard slice."""
    msg = (
        f"📌 {result['hashtags']}\n\n"
        f"🔥 {result['title_cn']}\n"
        f"{result['content_cn']}\n\n"
        f"🇲🇾 {result['title_ms']}\n"
        f"{result['content_ms']}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"📢 关注大事件频道➡️@Malaysia_New\n\n"
        f'📡 <a href="https://whatsapp.com/channel/0029Vb7xVrFFMqrOgMRT8p2T">关注WhatsApp频道</a>'
    )

    # FIX 3: Trim content fields BEFORE assembly, not the final HTML string
    # Telegram caption limit is 1024 chars
    if len(msg) > 1024:
        allowed = 1024 - (len(msg) - len(result['content_cn']))
        result['content_cn'] = result['content_cn'][:max(0, allowed)] + "…"
        # rebuild with trimmed content
        msg = format_message(result)

    return msg


async def send_with_retry(caption: str, image: str, retries: int = 3) -> bool:
    """FIX 4: Retry Telegram send up to N times."""
    for attempt in range(1, retries + 1):
        try:
            await send_post(caption=caption, image=image, parse_mode="HTML")
            return True
        except Exception as e:
            print(f"Send attempt {attempt} failed: {e}")
            if attempt < retries:
                await asyncio.sleep(3 * attempt)  # backoff: 3s, 6s
    return False


async def main():
    news_list = await get_all_news()
    print(f"Total articles to process: {len(news_list)}")

    sent_count = 0
    skip_count = 0
    fail_count = 0

    for news in news_list:
        url = news.get("url")
        title = news.get("title", "No title")

        try:
            # FIX 1: Check DB FIRST before any heavy work
            if already_posted(url):
                print(f"⏭ Skipped (already posted): {title}")
                skip_count += 1
                continue

            # 1. Fetch full article
            # 1. Fetch full article
            extracted = extract_content(url)
            content = extracted["content"]
            image_from_page = extracted["image"]

            if not content:
                print(f"⚠ Empty content [{url}]: {title}")
                continue

            news["content"] = content

            # Use page image if source didn't provide one
            if not news.get("image") and image_from_page:
                news["image"] = image_from_page
            
            # 2. AI generation
            result = generate_news(news)

            # 3. Format message safely
            msg = format_message(result)

            # 4. Send to Telegram with retry
            success = await send_with_retry(caption=msg, image=news.get("image"))

            if success:
                save_posted(url)
                print(f"✅ Sent: {title}")
                sent_count += 1
            else:
                print(f"❌ Failed to send after retries: {title}")
                fail_count += 1

            await asyncio.sleep(5)

        except Exception as e:
            print(f"❌ Error processing [{title}]: {e}")
            fail_count += 1

    print(f"\n📊 Done — Sent: {sent_count} | Skipped: {skip_count} | Failed: {fail_count}")


if __name__ == "__main__":
    asyncio.run(main())