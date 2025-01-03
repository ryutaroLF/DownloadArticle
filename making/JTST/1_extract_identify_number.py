import requests
from bs4 import BeautifulSoup

# 保存されたHTMLファイルのパス
html_file_path = "list.html"

# ファイルを開いてHTMLを解析
with open(html_file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# サブページのURLを格納するリスト
subpage_urls = []

# 固有番号を抽出
base_url = "https://www.jstage.jst.go.jp/article/jtst"
articles = soup.find_all("a", href=True)
for article in articles:
    href = article["href"]
    if "/article/jtst/" in href and "_article" in href:
        subpage_urls.append(href)

# URLをフルパスにする
subpage_urls = [base_url + url.split("/article/jtst")[1] for url in subpage_urls]

# 結果を出力
print("Found Subpage URLs:")
for url in subpage_urls:
    print(url)