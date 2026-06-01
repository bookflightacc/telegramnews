import os
from typing import Iterable

import requests
from dotenv import load_dotenv


load_dotenv()


ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v24.0")


class WhatsAppConfigError(RuntimeError):
    pass


def get_recipients() -> list[str]:
    raw = os.getenv("WHATSAPP_TO", "")
    return [number.strip() for number in raw.split(",") if number.strip()]


def require_config() -> None:
    missing = []

    if not ACCESS_TOKEN:
        missing.append("WHATSAPP_ACCESS_TOKEN")
    if not PHONE_NUMBER_ID:
        missing.append("WHATSAPP_PHONE_NUMBER_ID")
    if not get_recipients():
        missing.append("WHATSAPP_TO")

    if missing:
        raise WhatsAppConfigError(f"Missing WhatsApp env vars: {', '.join(missing)}")


def messages_url() -> str:
    return f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"


def post_message(payload: dict) -> dict:
    require_config()

    response = requests.post(
        messages_url(),
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

    try:
        data = response.json()
    except ValueError:
        data = {"raw": response.text}

    if response.status_code >= 400:
        raise RuntimeError(f"WhatsApp API error {response.status_code}: {data}")

    return data


def build_text_payload(to: str, text: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {
            "preview_url": True,
            "body": text,
        },
    }


def build_image_payload(to: str, image_url: str, caption: str) -> dict:
    return {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "image",
        "image": {
            "link": image_url,
            "caption": caption,
        },
    }


def send_whatsapp_post(caption: str, image: str | None = None, recipients: Iterable[str] | None = None) -> list[dict]:
    targets = list(recipients or get_recipients())
    results = []

    for to in targets:
        if image:
            payload = build_image_payload(to, image, caption)
        else:
            payload = build_text_payload(to, caption)

        results.append(post_message(payload))

    return results


if __name__ == "__main__":
    test_caption = "WhatsApp bot test from telegram-ai-news."
    responses = send_whatsapp_post(test_caption)
    print("Sent WhatsApp test message:")
    for response in responses:
        print(response)
