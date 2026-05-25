def format_post(news):

    return f"""
📌 {news['hashtags']}

🇨🇳 {news['title_cn']}

{news['content_cn']}

🇲🇾 {news['title_ms']}

{news['content_ms']}

━━━━━━━━━━━━━━

📢 关注大事件频道：
@Malaysia_New

📲 WhatsApp频道：
https://whatsapp.com/channel/0029Vb7xVrFFMqrOgMRT8p2T
"""