# === 第4步：翻页爬取 + 数据存储 ===
#
# 【爬虫概念】
# 1. 翻页：找到URL规律，循环请求每一页
# 2. 存储：CSV / Excel / JSON 三种格式，各有各的用处
#
# 【Git概念】
# git tag = 里程碑标记
# 比如完成一个大版本，打个 tag 做纪念
# git tag v1.0       打标签
# git tag -l          查看所有标签
# git push --tags     推送标签到GitHub

import sys 
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding = 'utf-8')

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

BASE_URL = "https://quotes.toscrape.com"
HEADERS ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

}

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR,exist_ok= True)

def get_page(url):
    """获取页面HTML"""
    try:
        response = requests.get(url,headers=HEADERS)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  请求失败: {e}")
        return None
    
#requests -> get html
#soup -> search for special info in a html

def parse_quotes(html):
    """解析一页的名言"""
    soup = BeautifulSoup(html,"lxml") #麻了
    quotes = []
    for quote_div in soup.select(".quote"):
        quotes.append({
            "text":quote_div.select_one(".text").text.strip(),
            "author": quote_div.select_one(".author").text.strip(),
            "tags":",".join(tag.text.strip() for tag in quote_div.select(".tags")),

        })
    return quotes

def crawl_all_pages():
    """翻页爬取所有名言"""
    all_quotes = []
    page = 1

    while True:
        url = f"{BASE_URL}/page/{page}/"
        print(f"正在爬取第{page}页：{url}")

        html  = get_page(url) #自定义函数：获取界面HTML
        if not html:
            break
        quotes = parse_quotes(html)
        if not quotes:
            print(f"第{page}页没有数据，爬取结束")
            break

        all_quotes.extend(quotes)
        print(f"✅ 提取到 {len(quotes)} 条，累计 {len(all_quotes)}")

        # 礼貌等待
        time.sleep(1)
        page += 1

        return all_quotes
def save_to_excel(data, filename):
    """保存为 Excel"""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False, sheet_name="名言")
    print(f"💾 已保存 Excel: {filename} ({len(data)} 条)")


def save_to_csv(data,filename):
    """保存为csv"""
    df = pd.DataFrame(data)
    df.to_csv(filename,index = False,encoding="utf-8-sig")
    print(f"💾 已保存 Excel: {filename} ({len(data)} 条)")

def save_to_json(data,filename):
    """保存为 JSON"""
    import json
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False,indent=2)
    print(f"💾 已保存 JSON: {filename} ({len(data)} 条)")

def main():
    print("=" * 60)
    print("  第4步：翻页爬取 + 数据存储")
    print("=" * 60)
    print()

    # 爬取所有页面
    all_quotes = crawl_all_pages()
    print()

    if not all_quotes:
        print("❌ 没有爬到数据")
        return
    
    print(f"🎉 总共爬取 {len(all_quotes)} 条名言！")
    print()

    #用pandas做简单统计
    df = pd.DataFrame(all_quotes)
    print(f"  作者数量: {df['author'].nunique()} 位")
    print(f"  名言数量: {len(df)} 条")
    print(f"  最多产的作者 TOP 5:")
    top_authors = df["author"].value_counts().head(5)
    for author, count in top_authors.items():
        print(f"    {author}: {count} 条")
    print()

    #保存为三种格式
    csv_path = os.path.join(OUTPUT_DIR,"quotes_all.csv")
    excel_path = os.path.join(OUTPUT_DIR,"quotes_all.xlsx")
    json_path = os.path.join(OUTPUT_DIR,"quotes_all.json")

    save_to_csv(all_quotes,csv_path)
    save_to_json(all_quotes,json_path)
    save_to_excel(all_quotes,excel_path)

    print()
    print("=" * 60)
    print("  第4步完成！")
    print("  你学会了：翻页爬取 / pandas 数据处理 / 三种格式存储")
    print("=" * 60)

if __name__ == "__main__":
    main()


        