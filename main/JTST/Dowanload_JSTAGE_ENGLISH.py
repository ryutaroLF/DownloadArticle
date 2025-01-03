from bs4 import BeautifulSoup
import requests
import json
import configparser
import os

# 外部ファイルから設定を読み込む
def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file, encoding="utf-8")
    return config

# 現在のディレクトリにある設定ファイルを探す
def find_config_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "config.ini")

# 保存フォルダを作成する
def ensure_save_directory():
    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Save")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return save_dir

# 設定ファイルを読み込む
config_file = find_config_file()
config = load_config(config_file)

# 設定からURLと辞書情報を取得
basepath = config["URLs"]["basepath"]
list_page_base = config["URLs"]["list_page_base"]
subpage_suffix = config["URLs"]["subpage_suffix"]
volume_issue_year = json.loads(config["Data"]["volume_issue_year"])

# 共通ヘッダー
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
}

# yearごとに結果を保存する関数
def save_to_file(year, title, keywords):
    save_dir = ensure_save_directory()
    filename = os.path.join(save_dir, f"{year}.txt")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"title : {title}\n")
        file.write(f"keyword : {', '.join(keywords)}\n")
        file.write("-----\n")

# リストページから固有番号を抽出する関数
def extract_unique_ids(list_page_url):
    print(f"Fetching list page URL: {list_page_url}")  # デバッグ用
    response = requests.get(list_page_url, headers=headers)
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
    response = requests.get(subpage_url, headers=headers)
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
        subpage_url = f"{basepath}/{unique_id}{subpage_suffix}"
        
        print(f"Generated Subpage URL: {subpage_url}")  # 確認用

        title, keywords = extract_title_keywords(subpage_url)
        
        if title and keywords:
            # year.txtに保存
            save_to_file(year, title, keywords)