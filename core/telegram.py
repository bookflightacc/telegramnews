from telegram import Bot
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

async def send_post(caption, image=None):

    # 🚨 如果有图片 → send_photo（媒体帖）
    if image:
        await bot.send_photo(
            chat_id=CHANNEL,
            photo=image,
            caption=caption[:1024]  # Telegram限制
        )

    # ❌ 没图片 → fallback text
    else:
        await bot.send_message(
            chat_id=CHANNEL,
            text=caption
        )