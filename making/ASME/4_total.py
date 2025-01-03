from bs4 import BeautifulSoup
import requests
import json
import re

# 年のリスト
years = [2023, 2024]

# URLのベースパス
base_year_url = "https://asmedigitalcollection.asme.org/heattransfer/issue/browse-by-year/{}"
base_issue_url = "https://asmedigitalcollection.asme.org"

# 共通ヘッダー
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

# 年ごとの処理
def process_year(year):
    year_url = base_year_url.format(year)
    print(f"Processing year: {year}, URL: {year_url}")

    # 年リストページのHTMLを取得
    response = requests.get(year_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch year page: {year_url}, Status Code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # volume-issueリンクを抽出
    volume_issue_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/heattransfer/issue/' in href:
            match = re.match(r'^/heattransfer/issue/\d+/\d+$', href)
            if match:
                full_url = base_issue_url + href
                volume_issue_links.append(full_url)

    # 各volume-issueの処理
    for issue_url in volume_issue_links:
        process_volume_issue(issue_url, year)

# volume-issueの処理
def process_volume_issue(issue_url, year):
    print(f"Processing issue: {issue_url}")

    # issueページのHTMLを取得
    response = requests.get(issue_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch issue page: {issue_url}, Status Code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # サブサブページリンクを抽出
    article_urls = []
    divs = soup.find_all("div", class_="al-article-item-wrap")
    for div in divs:
        link = div.find("a", href=True)
        if link and "/heattransfer/article/" in link['href']:
            full_url = f"https://asmedigitalcollection.asme.org{link['href']}"
            article_urls.append(full_url)

    # 各論文の情報を取得
    for article_url in article_urls:
        extract_article_info(article_url, year)

# サブサブページから情報を取得
def extract_article_info(article_url, year):
    print(f"Processing article: {article_url}")

    # 論文ページのHTMLを取得
    response = requests.get(article_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch article page: {article_url}, Status Code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # JSON-LDスクリプトを探す
    json_ld_script = soup.find("script", type="application/ld+json")
    if json_ld_script:
        json_data = json.loads(json_ld_script.string)

        # タイトルを取得
        title = json_data.get("name", "No title found")

        # キーワードとトピックスを取得
        keywords = json_data.get("keywords", [])
        topics = json_data.get("about", [])

        # キーワードからトピックスを除外
        unique_keywords = [keyword for keyword in keywords if keyword not in topics]

        # year.txtに保存
        save_to_file(year, title, unique_keywords, topics)
    else:
        print("No JSON-LD script found.")

# year.txtに保存
def save_to_file(year, title, keywords, topics):
    filename = f"{year}.txt"
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"title : {title}\n")
        file.write(f"keyword : {', '.join(keywords)}\n")
        file.write(f"topic : {', '.join(topics)}\n")
        file.write("-----\n")

# メイン処理
for year in years:
    process_year(year)