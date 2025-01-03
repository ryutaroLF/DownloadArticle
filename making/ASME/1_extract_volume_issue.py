from bs4 import BeautifulSoup
import re

# HTMLファイルを読み込む
with open('list.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoupでHTMLを解析
soup = BeautifulSoup(html_content, 'html.parser')

# URLのベースパス
base_url = "https://asmedigitalcollection.asme.org"

# volume-issueリンクを抽出する
volume_issue_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if '/heattransfer/issue/' in href:
        # volume-issueの形式を確認 (数字型のみを抽出)
        match = re.match(r'^/heattransfer/issue/\d+/\d+$', href)
        if match:
            full_url = base_url + href
            volume_issue_links.append(full_url)

# 結果を出力
for url in volume_issue_links:
    print(url)