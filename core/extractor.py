import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ms-MY,ms;q=0.9,en-US;q=0.8,en;q=0.7",
}

def extract_content(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
    except Exception as e:
        print(f"Request failed [{url}]: {e}")
        return {"content": "", "image": None}

    if res.status_code != 200:
        print(f"extract_content blocked [{res.status_code}]: {url}")
        return {"content": "", "image": None}

    soup = BeautifulSoup(res.text, "html.parser")

    # Remove noise tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()

    # -------------------
    # 1. CONTENT
    # Try article body first, fall back to all <p>
    # -------------------
    body = (
        soup.find("div", class_=lambda c: c and any(
            x in c for x in ["article-body", "article-content", "entry-content", "post-content", "story-body"]
        ))
        or soup.find("article")
    )

    if body:
        paragraphs = body.find_all("p")
    else:
        paragraphs = soup.find_all("p")

    content = "\n".join(
        p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
    )

    # -------------------
    # 2. IMAGE
    # OG image is most reliable (used for social sharing, always high quality)
    # -------------------
    image = None

    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        image = og_image["content"]
    else:
        # fallback: first real img tag
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
            if src and src.startswith("http"):
                image = src
                break

    print(f"Extracted {len(content)} chars, image: {'yes' if image else 'no'} [{url}]")
    return {"content": content[:3000], "image": image}