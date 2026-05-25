from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def safe_parse(text):
    try:
        return json.loads(text)
    except:
        # fallback repair
        text = text.strip()

        # try extract JSON part
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            return json.loads(text[start:end+1])

        raise ValueError("Invalid JSON from model")

def generate_news(news):

    prompt = f"""
You are a professional news editor.

CRITICAL RULES:
- Output MUST be valid JSON only
- DO NOT use random or broken Chinese characters
- Chinese must be clean and natural Simplified Chinese
- NO repetition, NO nonsense words
- NO mixed languages inside Chinese field

Return ONLY JSON:

{{
  "hashtags": "relevant hashtag for example #国际新闻 #社会新闻",
  "title_cn": "clean Chinese headline",
  "content_cn": "clean Chinese paragraph(not more than 300 characters)",
  "title_ms": "natural Malay headline",
  "content_ms": "natural Malay content(not more than 500 characters)"
}}

News:

Title: {news['title']}
Content: {news['content']}
"""

    res = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    text = res.choices[0].message.content

    return safe_parse(text)
