import requests
from bs4 import BeautifulSoup

# サブページのURL
url = "https://www.jstage.jst.go.jp/article/jtst/19/2/19_24-00172/_article/-char/en"

# サブページのHTMLを取得
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # 論文タイトルを抽出
    title = soup.find("div", class_="global-article-title").get_text(strip=True)

    # キーワードを抽出
    keywords_section = soup.find("div", class_="global-para")
    keywords = [a.get_text(strip=True) for a in keywords_section.find_all("a")]

    # 結果を表示
    print("Title:", title)
    print("Keywords:", ", ".join(keywords))
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")