# === 第3步：真实网页爬取 - quotes.toscrape.com ===
#
# 【爬虫概念】
# 爬真实网站的三大原则：
# 1. 设置 User-Agent，伪装成浏览器
# 2. 设置超时 + 异常处理，程序不崩溃
# 3. 控制请求频率（time.sleep），不要给服务器太大压力

#爬真实网站的三件套
# User-Agent 伪装 — 告诉服务器"我是浏览器"
# 超时 + 异常处理 — 网络不可靠，出错了要优雅处理
# 请求间隔（限速） — 不要爬太快，尊重服务器，也避免被封 IP

# 目标网站：http://quotes.toscrape.com/
# 这是一个专门用来练习爬虫的网站，100% 合法安全
#
# 【Git概念】
# .gitignore 文件 = 告诉 Git 哪些文件不要提交
# 比如生成的数据文件、缓存文件、IDE配置等
# 规则写在 .gitignore 里，每行一条

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding = 'utf-8')

# sys.stdout.buffer → 拿到标准输出的"底层缓冲区"（原始字节流
# `io.TextIOWrapper(..., encoding='utf-8') → 把它用 UTF-8 编码重新包装一下
# 这样打印中文就不会报错了

import requests 
from bs4 import BeautifulSoup
import time 
import csv

#基础配置
BASE_URL = "https://quotes.toscrape.com"
HEADERS = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.361"
}

def get_page(url):
    """获取一个页面的 HTML，封装了超时和异常处理"""
    try:
        response = requests.get(url,headers = HEADERS,timeout = 15)
        response.raise_for_status() # 状态码不是2xx就抛异常
        return response.text
    except requests.Timeout:
        print(f"⏰ 请求超时：{url}")
        return None
    except requests.ConnectionError:
        print(f"  🔌 连接失败: {url}")
        return None
    except requests.HTTPError as e:
        print(f"  ❌ HTTP错误: {e}")
        return None
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return None

def parse_quotes(html):
    """从HTML中提取名言、作者、标签"""
    soup = BeautifulSoup(html,"lxml")
    quotes = []

  # 每个名言都在 class="quote" 的 div 里
    for quote_div in soup.select(".quote"):
        # 提取名言内容
        text = quote_div.select_one(".text").text

        #提取作者
        author = quote_div.select_one(".author").text

        #提取标签（可能有多个）
        tags = [tag.text for tag in quote_div.select(".tag")]

         # 提取作者详情页链接
        author_link = quote_div.select_one("a")["href"]
        author_url = BASE_URL + author_link

        quotes.append({
            "text": text,
            "author":author,
            "tags":",".join(tags),
            "author_url": author_url
})
        return quotes

def main():
    print("=" * 60)
    print("  第3步：爬取真实网站 - quotes.toscrape.com")
    print("=" * 60)

     # 爬取第1页
    url = BASE_URL + "/"
    print(f"\n正在爬取: {url}")
    html = get_page(url)
    if not html:
        print("爬取失败！")
        return

    # 解析数据
    quotes = parse_quotes(html)
    print(f"\n✅ 成功提取 {len(quotes)} 条名言\n")

    # 打印结果
    for i, q in enumerate(quotes, 1):
        print(f"[{i}] {q['text']}")
        print(f"    —— {q['author']}")
        print(f"    标签: {q['tags']}")
        print()

    #保存到csv
    with open("output/quotes_page1.csv","w",newline="",encoding = "utf-8-sig") as f:
        writer = csv.DictWriter(f,fieldnames=['text','author','tags','author_url'])
        writer.writeheader()
        writer.writerows(quotes)

    print(f"💾 数据已保存到 output/quotes_page1.csv")
    print(f"   （用 Excel 或记事本打开查看）")

    # 礼貌地等一下，再请求作者详情页（演示限速）
    time.sleep(1)
    
    first_author_url = quotes[0]["author_url"]
    print(f"正在获取作者详情: {first_author_url}")

    author_html = get_page(first_author_url)
    if author_html:
        soup = BeautifulSoup(author_html,"lxml")
        author_name = soup.select_one(".author-title").text.strip()
        author_born = soup.select_one(".author-born-date").text.strip()
        author_bio = soup.select_one(".author-description").text.strip()

        print(f"\n👤 作者: {author_name}")
        print(f"   出生日期: {author_born}")
        print(f"   简介: {author_bio[:150]}...")

    print("\n" + "=" * 60)
    print("  第3步完成！")
    print("  你学会了：伪装请求头 / 异常处理 / 限速 / 提取数据")
    print("=" * 60)

if __name__ == "__main__":
    # 先创建output目录（如果不存在)
    import os
    os.makedirs("output",exist_ok = True)
    main()