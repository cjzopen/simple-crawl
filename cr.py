import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import time

def crawl_website(url):
    """爬取網站並提取標題和連結，過濾特定網址，並儲存為 JSON 檔案"""
    visited = set()  # 追蹤已訪問的網址
    queue = [url]  # 待訪問的網址佇列
    base_url = url  # 儲存網站的根網址，用於判斷同網域
    data = []  # 儲存爬取到的資料

    while queue:
        current_url = queue.pop(0)
        if current_url in visited:
            continue
        visited.add(current_url)

        # 檢查網址是否符合條件
        print(f"檢查網址：{current_url}")
        # if current_url != url and not current_url.startswith(url + "/tw/"):
        #     print(f"跳過不符合條件的網址：{current_url}")
        #     continue
        if "/tag/" in current_url or "/search" in current_url or "/en" in current_url or "/#" in current_url or ".png" in current_url or ".jpg" in current_url or ".webp" in current_url:
            print(f"跳過不符合條件的網址：{current_url}")
            continue

        try:
            response = requests.get(current_url)
            response.raise_for_status()  # 檢查 HTTP 狀態碼
            soup = BeautifulSoup(response.content, "html.parser")

            title = soup.title.string if soup.title else "無標題"
            h1_text = soup.find("h1").get_text(strip=True) if soup.find("h1") else ""
            print(f"標題：{title}，連結：{current_url}，H1：{h1_text}")

            # 將資料儲存到列表中
            data.append({"title": title, "link": current_url, "h1": h1_text})

            # 尋找頁面上的所有連結
            for link in soup.find_all("a", href=True):
                absolute_url = urljoin(current_url, link["href"])
                if absolute_url.startswith(base_url):  # 只爬取同網域的連結
                    queue.append(absolute_url)

        except requests.exceptions.RequestException as e:
            print(f"訪問 {current_url} 時發生錯誤：{e}")

        time.sleep(5)  # 在每次請求之間添加延遲

    # 將資料儲存為 JSON 檔案
    with open(f"{domain_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 輸入你的網站網址
domain_name = "xxx.com"
website_url = f"https://{domain_name}"
crawl_website(website_url)