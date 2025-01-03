import requests
from bs4 import BeautifulSoup

# 辞書型でvolume, issue, yearを指定
volume_issue_year = {
    "19_2": 2024,
    "19_1": 2024,
    "18_2": 2023,
    "18_1": 2023,
    # 必要に応じて追加
}

# Base URL 定義
basepath = "https://www.jstage.jst.go.jp/article/jtst"
list_page_base = "https://www.jstage.jst.go.jp/browse/jtst/{}/_contents/-char/en"
subpage_suffix = "/_article/-char/en"

# yearごとに結果を保存する関数
def save_to_file(year, title, keywords):
    filename = f"{year}.txt"
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"title : {title}\n")
        file.write(f"keyword : {', '.join(keywords)}\n")
        file.write("-----\n")

# リストページから固有番号を抽出する関数
def extract_unique_ids(list_page_url):
    print(f"Fetching list page URL: {list_page_url}")  # デバッグ用
    response = requests.get(list_page_url)
    if response.status_code != 200:
        print(f"Failed to fetch list page: {list_page_url}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    unique_ids = []
    articles = soup.find_all("a", href=True)
    for article in articles:
        href = article["href"]
        if "/article/jtst/" in href and "_article" in href:
            # Extract unique part without duplicates
            unique_ids.append(href.split("/article/jtst", 1)[1].split("/_article", 1)[0])
    print(f"Extracted Unique IDs: {unique_ids}")  # デバッグ用
    return unique_ids

# サブページからタイトルとキーワードを取得する関数
def extract_title_keywords(subpage_url):
    print(f"Fetching subpage URL: {subpage_url}")  # デバッグ用
    response = requests.get(subpage_url)
    if response.status_code != 200:
        print(f"Failed to fetch subpage: {subpage_url}")
        return None, None
    
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("div", class_="global-article-title").get_text(strip=True)
    keywords_section = soup.find("div", class_="global-para")
    keywords = [a.get_text(strip=True) for a in keywords_section.find_all("a")]
    print(f"Extracted Title: {title}")  # デバッグ用
    print(f"Extracted Keywords: {keywords}")  # デバッグ用
    return title, keywords

# メイン処理
for vol_issue, year in volume_issue_year.items():
    print(f"Processing volume/issue: {vol_issue}, year: {year}")
    
    # リストページのURLを生成
    list_page_url = list_page_base.format(vol_issue.replace("_", "/"))
    print(f"Generated List Page URL: {list_page_url}")  # デバッグ用
    
    # 固有番号を取得
    unique_ids = extract_unique_ids(list_page_url)
    if not unique_ids:
        continue
    
    # 各固有番号からサブページURLを生成し、タイトルとキーワードを取得
    for unique_id in unique_ids:
        # サブページURLの生成
        subpage_url = f"{basepath}{unique_id}{subpage_suffix}"
        
        print(f"Generated Subpage URL: {subpage_url}")  # 確認用

        title, keywords = extract_title_keywords(subpage_url)
        
        if title and keywords:
            # year.txtに保存
            save_to_file(year, title, keywords)