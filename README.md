# Python 爬虫学习笔记

从零开始学习 Python 爬虫 + Git/GitHub 双线学习计划。

## 目录

- [第1步：HTTP 请求基础](#第1步http-请求基础)
- [第2步：HTML 解析](#第2步html-解析)
- [环境准备](#环境准备)

---

## 第1步：HTTP 请求基础

### 核心概念

爬虫的本质 = 模拟浏览器发送请求，获取网页内容。

- **GET 请求**：从服务器获取数据（就像在浏览器输入网址按回车）
- **POST 请求**：向服务器提交数据（就像填写表单点提交）
- **状态码**：服务器告诉你请求结果
  - `200` - 成功
  - `404` - 页面不存在
  - `500` - 服务器出错
- **请求头（Headers）**：告诉服务器"我是谁"，其中 `User-Agent` 最重要
- **超时（timeout）**：防止请求永远卡住，爬虫必须设置

### 常用代码

```python
import requests

#Get reqry
response = requests.get("https://www.baidu.com", timeout=10)

#带参数的GET
params = {"wd":"python"}
response = requests.get("https://www.baidu.com/s",params = params, timeout = 10)

# 自定义请求头（伪装浏览器）
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; ...)"}
response = requests.get(url,headers = headers, timeout = 10)

# 解析 JSON
data = response.json()

# 异常处理
try:
    response = requests.get(url,timeout = 10)
    response.raise_for_status()
except requests.Timeout:
    print("请求超时")
except requests.RequestException as e:
    print("fails:",e)
```

## 关于HTML解析

```python
<html>                       ← 根标签
  <head>                     ← 头部（放标题、CSS等）
    <title>网页标题</title>
  </head>
  <body>                     ← 正文（用户能看到的内容都在这里）
    <h1>欢迎学习爬虫</h1>     ← 一级标题
    <p class="intro">        ← 段落标签，带 class 属性
      爬虫可以提取网页中的<a href="https://example.com">链接</a>
    </p>
    <ul id="list">           ← 无序列表，带 id 属性
      <li>第一项</li>        ← 列表项
      <li>第二项</li>
    </ul>
  </body>
</html>

核心要素：
标签：用 <标签名> 开始，</标签名> 结束
属性：标签里的 class="xxx"、id="xxx"、href="xxx" 等
文本：标签中间夹着的文字内容
选择器：用来"定位"到你想要的标签，就像找文件的路径
BeautifulSoup 是 Python 最流行的 HTML 解析库，用 CSS 选择器来提取数据。


```

拿到网页 HTML 之后，用 BeautifulSoup 解析，用 CSS 选择器 定位元素。
HTML：网页的骨架，由标签组成（如 \<div>、\<p>、\<a>）
标签属性：class、id、href、src 等
CSS 选择器：定位元素的方式标签名：p、a、div
class：.item、.product
id：#header、#main
后代：.product-list .product

### tips

写完 README 后，你可以用 VS Code 打开它，按 Ctrl+Shift+V 预览渲染效果（Markdown 预览），看看是不是和 GitHub 上显示的一样。

### 常用代码2

```python
from bs4 import BeautifulSoup

#创建解析对象

soup = BeautifulSoup(html_text,"lxml")

#find first one
title = soup.find("title")
print(title.text)

#find multiple projects(CSS选择器)
items = soup.select(".news-item")
for item in items:
    print(item.text)

#find one (CSS selector)
product = soup.select_one(".product")
print(product.get("data-price"))# 提取属性
```

## 环境准备

```bash
pip install requests beautifulsoup4 lxml
```

已安装
-Python 3.12
-requests 2.x
-beautifulsoup4 4.x
-lxml
-pandas

## git command

git init -> 初始化仓库
git add 文件名 ->添加到暂存区
git commit -m "说明" -> 提交到历史
git status -> 查看当前状态
git log --oneline -> 查看提交历史
git branch -> 查看所有分支
git checkout -b 分支名 -> 新建并切换分支
git merge 分支名 -> 合并分支到当前
git diff -> 查看改动
git diff master..HEAD 意思是：对比 master 分支和当前分支 HEAD 的差异
# 3. 把 master 回退到 step1（保留文件在工作区，不删除）
git reset --soft 342672f
--soft = 软回退：只撤销 commit，文件还在暂存区
--mixed = 混合回退：撤销 commit 和 add，文件还在工作区（默认）
--hard = 硬回退：彻底删掉，文件也没了（慎用！）
