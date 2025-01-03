from bs4 import BeautifulSoup

# ファイルを開いてHTMLを解析
with open("1361.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

# 論文詳細ページのURLを格納するリスト
article_urls = []

# 各論文リンクを抽出
divs = soup.find_all("div", class_="al-article-item-wrap")
for div in divs:
    link = div.find("a", href=True)
    if link and "/heattransfer/article/" in link['href']:
        full_url = f"https://asmedigitalcollection.asme.org{link['href']}"
        article_urls.append(full_url)

# 結果を表示
for url in article_urls:
    print(url)

print(f"Extracted {len(article_urls)} article URLs.")