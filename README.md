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

把 master 回退到 step1（保留文件在工作区，不删除）
git reset --soft 342672f
--soft = 软回退：只撤销 commit，文件还在暂存区
--mixed = 混合回退：撤销 commit 和 add，文件还在工作区（默认）
--hard = 硬回退：彻底删掉，文件也没了（慎用！）
git log 进入了分页模式（内容太多显示不完），按 q 键可以退出来

## 爬虫最核心的技能

——**怎么找到你要的内容在 HTML 的什么位置。

答案是：用浏览器的开发者工具（F12。

怎么找到选择器？
第一步：打开目标网页
用 Chrome 或 Edge 打开目标网站
第二步：打开开发者工具
   按 F12 键，或者右键 → 右键页面上，或者 **检查"元素
按 F12 就会弹出开发者工具的小箭头
第三步：用"选择元素工具
   在开发者工具的左上角有个小箭头图标（或者按 Ctrl +Shift + C
   然后在网页上你想找的内容（比如某条名言），点一下
第四步：看 HTML 结构
   点完之后，开发者工具会自动定位到那条名言对应的 HTML 代码。你就能看到：

```bash
<div class="quote" ...>
  <span class="text" ...>名言内容
  <span>
    <small class="author">作者
    <a href="/author/...">
    ...
```

你就知道了：
每条名言都在 class="quote" 的 div 里
名言内容在 class="text" 的 span 里
作者在 class="author" 的 small 里
实际操作
找选择器的方法
方法：
开发者工具 → Elements 面板里，找到对应元素上 → 右键 → Copy → Copy selector
就能拿到 CSS 选择器
类比
你可以试试打开 quotes.toscrape.com 来练习一下，找找看：
名言在哪个标签里？
下一页按钮的链接在哪？
标签页的链接怎么找？
这是爬虫的"侦察"工作，80% 的时间都花在这上面了。写代码本身反而简单。

---

# 第3步补充：真实网页爬取的常用知识点

## select_one / select  vs  find / find_all

| | find / find_all | select_one / select |
|---|---|---|
| 用的语言 | BeautifulSoup 自己的方法 | CSS 选择器 |
| 找一个 | soup.find("div", class_="quote") | soup.select_one(".quote") |
| 找多个 | soup.find_all("div", class_="quote") | soup.select(".quote") |
| 复杂查找 | 写起来啰嗦，要一层层找 | 一行搞定 |

建议优先学 CSS 选择器（select），因为它通用、简洁，浏览器也能直接 Copy selector。

## CSS 选择器语法速查

| 写法 | 意思 | 例子 |
|---|---|---|
| 标签名 | 找这种标签 | `a`、`div`、`p` |
| .class名 | 找 class 等于这个的 | `.tag`、`.product` |
| #id名 | 找 id 等于这个的 | `#news`、`#header` |
| [属性] | 找有这个属性的 | `[href]` |
| [属性=值] | 属性等于某值 | `a[href="/page/2"]` |

记忆口诀：**标签直接写，class 加个点，id 用 #，属性放括号**

组合示例：
- `a.tag` → class 是 tag 的 a 标签
- `#main .product a` → id 为 main 的元素下、class 为 product 里的 a
- `a[href^="https://"]` → href 以 https 开头的 a 标签

## id 是什么

id 是 HTML 标签的属性，给元素起一个**唯一**的名字（一个页面只能出现一次，像身份证）。
- id：唯一，用 `#名字` 选择，定位单个元素
- class：可重复，用 `.名字` 选择，给一组元素打标签

定位优先级：优先用 id（唯一最准）→ 没有就用 class → 再没有就用层级关系。

## strip() 去空白

网页文字前后常有换行和空格，用 strip() 清理：
- `.strip()`  去掉两边空白
- `.lstrip()` 去掉左边
- `.rstrip()` 去掉右边

爬虫最佳实践：提取文本后养成 `.text.strip()` 的习惯。

## os 模块

os = 操作系统，常用于文件/文件夹操作：
- `os.makedirs("output", exist_ok=True)` 创建文件夹（exist_ok=True 表示已存在也不报错）
- `os.path.exists("xxx")` 判断文件是否存在
- `os.path.join("a", "b")` 拼接路径（跨平台安全）
- `os.listdir("xxx")` 列出目录里的文件

## 如何找选择器（爬虫核心技能）

1. Chrome/Edge 打开目标网页
2. 按 F12 打开开发者工具
3. 按 Ctrl+Shift+C 点选页面元素
4. 查看高亮的 HTML 结构，确定标签/class/id
5. 也可右键元素 → Copy → Copy selector 直接拿到选择器

爬虫 80% 的时间花在"侦察"（找选择器）上，写代码反而简单。

---

# 第4步补充：翻页 + pandas + Git Tag

## 翻页策略

1. URL 规律翻页：`/page/1/`、`/page/2/`…循环请求
2. 找"下一页"链接：解析 Next 按钮的 href

## pandas 基础（代码版 Excel）

两个核心概念：
- Series = 一列数据（Excel 的一列）
- DataFrame = 一张表格（整个 Excel 表）

常用操作：
```python
import pandas as pd

# 字典列表 -> 表格
df = pd.DataFrame(data)

# 取一列
df["author"]

# 去重计数（多少个不同的作者）
df["author"].nunique()

# 每个值出现次数
df["author"].value_counts()

# 取前 5 名
df["author"].value_counts().head(5)

# 遍历统计结果
for author, count in df["author"].value_counts().head(5).items():
    print(author, count)

# 导出
df.to_csv("data.csv", index=False, encoding="utf-8-sig")  # utf-8-sig 防止Excel中文乱码
df.to_excel("data.xlsx", index=False)

# 读取
df = pd.read_csv("data.csv")
df = pd.read_excel("data.xlsx")
```

参数说明：
- `index=False` 不保存行号
- `encoding="utf-8-sig"` 解决 Excel 打开中文乱码

## 三种存储格式对比

| 格式 | 优点 | 适合场景 |
|---|---|---|
| CSV | 简单，Excel 直接打开 | 表格数据、快速查看 |
| Excel(.xlsx) | 好看，可加样式 | 给人看的报表 |
| JSON | 灵活，支持嵌套 | 给程序读的数据 |

## Git Tag（里程碑标记）

```bash
git tag v0.4-step4     # 给当前提交打标签
git tag -l             # 查看所有标签
git push --tags        # 推送标签到 GitHub（tag 不会随 git push 自动推送）
```
