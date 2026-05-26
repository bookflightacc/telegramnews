# import requests
# from bs4 import BeautifulSoup

# def extract_content(url):
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }

#     res = requests.get(url, headers=headers, timeout=15)
#     soup = BeautifulSoup(res.text, "html.parser")

#     # 去掉无用标签
#     for tag in soup(["script", "style", "noscript"]):
#         tag.decompose()

#     paragraphs = soup.find_all("p")

#     content = "\n".join(
#         [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
#     )

#     return content[:3000]  # 防止太长

import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

def extract_content(url):

    res = requests.get(url, headers=headers, timeout=10)

    if res.status_code != 200:
        return ""

    soup = BeautifulSoup(res.text, "html.parser")

    # -------------------
    # 1. CONTENT
    # -------------------
    paragraphs = soup.find_all("p")
    content = "\n".join([p.get_text(strip=True) for p in paragraphs])

    # -------------------
    # 2. IMAGE (IMPORTANT FIX)
    # -------------------
    image = None

    img_tag = soup.find("img")

    if img_tag:

        # case 1: normal
        if img_tag.get("src"):
            image = img_tag["src"]

        # case 2: lazy load
        elif img_tag.get("data-src"):
            image = img_tag["data-src"]

    return {
        "content": content,
        "image": image
    }