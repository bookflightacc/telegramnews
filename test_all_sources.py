from sources.bharian import fetch_bharian
from sources.sinchew import fetch_sinchew

def get_all():
    news = []
    news += fetch_bharian()
    news += fetch_sinchew()
    return news

news = get_all()

print("TOTAL:", len(news))

for n in news:
    print("\n---")
    print(n["source"])
    print(n["title"])
    print(n["url"])