from bs4 import BeautifulSoup
import json

# HTMLファイルを読み込む
with open("article1.html", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

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

    # 結果を表示
    print(f"Title: {title}")
    print(f"Keywords: {unique_keywords}")
    print(f"Topics: {topics}")
else:
    print("No JSON-LD script found.")