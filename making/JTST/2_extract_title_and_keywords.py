from bs4 import BeautifulSoup

# ローカルのサブページHTMLファイルのパス
html_file_path = "sub.html"

# ファイルを開いてHTMLを解析
with open(html_file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# 論文タイトルを抽出
title = soup.find("div", class_="global-article-title").get_text(strip=True)

# キーワードを抽出
keywords_section = soup.find("div", class_="global-para")
keywords = [a.get_text(strip=True) for a in keywords_section.find_all("a")]

# 抽出した結果を表示
print("Title:", title)
print("Keywords:", ", ".join(keywords))