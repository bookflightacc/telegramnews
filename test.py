import asyncio
from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

bot = Bot(token=BOT_TOKEN)

async def main():
    await bot.send_message(
        chat_id=CHANNEL,
        text="Hello from AI Bot 🚀"
    )

    print("Message sent!")

asyncio.run(main())