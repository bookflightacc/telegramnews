from core.extractor import extract_content

url = "https://www.sinchew.com.my/?p=7530985"

content = extract_content(url)

print(content[:1000])