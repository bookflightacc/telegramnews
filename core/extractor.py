import requests
from bs4 import BeautifulSoup

def extract_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(res.text, "html.parser")

    # 去掉无用标签
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    paragraphs = soup.find_all("p")

    content = "\n".join(
        [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
    )

    return content[:3000]  # 防止太长