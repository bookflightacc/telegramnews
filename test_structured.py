from core.ai import generate_news

news = {
    "title": "欧洲女子吐槽KL道路设计",
    "content": "A European tourist complained..."
}

result = generate_news(news)

print(result)