# === 第2步：HTML 解析 - 从网页中提取数据 ===
#
# 【爬虫概念】
# 拿到了网页源代码（一大坨HTML），怎么提取你想要的数据？
# 答案：用 BeautifulSoup 解析 HTML，然后用 CSS 选择器定位元素
# HTML 就像一棵倒过来的树：html → body → div → p → a
#div 是树枝，p 是树枝，a 是叶子，你想要的链接就在 a 标签里
#div -> division, HTML 的一个常用标签，表示一个区块或者容器，通常用来把网页分成不同的部分，比如头部、内容区、侧边栏、底部等等。div 标签本身没有任何语义，只是一个通用的容器，可以用来包裹其他元素，帮助我们布局和组织网页内容了。
#p -> paragraph，HTML 的一个常用标签，表示一个段落，通常用来包裹一段文本内容，帮助我们把文本分成不同的段落，增加可读性了。
#a -> anchor，HTML 的一个常用标签，表示一个链接，通常用来创建一个超链接，指向另一个网页或者资源了。a 标签的 href 属性就是链接的地址，标签内的文本就是链接的文字了。

#网页排版通常是div + CSS 来实现的，div 就像树枝一样，把网页分成不同的部分了。我们想要的数据通常在某个 div 里，或者在 div 下面的某个 p 标签里，或者在 p 标签下面的某个 a 标签里了。我们就像在树上找叶子一样，顺着树枝找到你想要的数据了。
# 我们从树根出发，顺着树枝找到你要的叶子
#
# 【Git概念 - 本步涉及】
# git branch          → 查看所有分支
# git checkout -b 名  → 新建并切换到新分支
# git diff            → 查看改动内容（和上一次提交比）
# git merge 名        → 把某个分支合并到当前分支
# 分支 = 平行宇宙，互不干扰，想合并就 merge

from bs4 import BeautifulSoup

# ---------------------------------------------------------------
# 模拟一段 HTML（实际爬虫中这是从网上请求下来的）
# ---------------------------------------------------------------
html_doc = """
<html>
  <head>
    <title>爬虫学习网站</title>
  </head>
  <body>
    <h1 class="main-title">欢迎来到爬虫世界</h1>
    <p class="intro">这是一个用来练习解析的网页。</p>
    
    <div id="news">
      <h2>最新新闻</h2>
      <ul class="news-list">
        <li class="news-item"><a href="/news/1">新闻一：Python爬虫入门</a></li>
        <li class="news-item"><a href="/news/2">新闻二：BeautifulSoup教程</a></li>
        <li class="news-item"><a href="/news/3">新闻三：数据可视化</a></li>
      </ul>
    </div>
    
    <div class="product-list">
      <h2>产品列表</h2>
      <div class="product" data-price="99">
        <h3>产品A</h3>
        <p class="price">99元</p>
        <span class="rating">★★★★☆</span>
      </div>
      <div class="product" data-price="199">
        <h3>产品B</h3>
        <p class="price">199元</p>
        <span class="rating">★★★★★</span>
      </div>
      <div class="product" data-price="49">
        <h3>产品C</h3>
        <p class="price">49元</p>
        <span class="rating">★★★☆☆</span>
      </div>
    </div>
  </body>
</html>


"""

'''
h-> heading,HTML 的一个常用标签,表示标题，h1 是一级标题，h2 是二级标题，h3 是三级标题，以此类推。通常用来表示网页的结构和层次了。
ul -> unordered list，HTML 的一个常用标签，表示无序列表，通常用来包裹一组相关的列表项了。
li -> list item，HTML 的一个常用标签，表示列表项，通常用来包裹一个列表中的每一项了。
p -> paragraph，HTML 的一个常用标签，表示一个段落，通常用来包裹一段文本内容了。
span -> span，HTML 的一个常用标签，表示一个行内元素，通常用来包裹一小段文本或者一个小的元素了。span 标签本身没有任何语义，只是一个通用的行内容器，可以用来给文本或者元素添加样式或者属性了。
'''
# ---------------------------------------------------------------
# 1. 创建 BeautifulSoup 对象
# ---------------------------------------------------------------
# 第一个参数：HTML文本
# 第二个参数：解析器（lxml 比默认的快）
#lxml 是一个第三方库，提供了一个更快的 HTML 解析器，比 Python 内置的解析器更高效了。要使用 lxml 解析器，需要先安装 lxml 库了，可以通过 pip install lxml 来安装了。

soup = BeautifulSoup(html_doc,"lxml") # 现在 soup 就是一个 BeautifulSoup 对象了，我们可以用它来解析 HTML 了
# html_doc 是我们之前定义的 HTML 文本，"lxml" 是我们选择的解析器了。现在 soup 就是一个 BeautifulSoup 对象了，我们可以用它来解析 HTML 了了。

print("=" * 50)
print("1. 最基本的：找到一个标签")
print("=" * 50)

#find() = > 找到第一个符合条件的标签
#find_all() => 找到所有符合条件的标签，返回一个列表了

title = soup.find("title") # 找到第一个 title 标签了
print(f"网页标题：{title.text}") # .text = 标签里的文字
main_title = soup.find("h1", class_="main-title") # 找到第一个 h1 标签，class_ 是因为 class 是 Python 的保留字了
print(f"主标题：{main_title.text}")

h1 = soup.find("h1")
print(f"一级标题：{h1.text}")
print(f"h1 的 class 属性：{h1.get('class')}") #.get() = 获取标签属性

# ---------------------------------------------------------------
# 2. CSS 选择器（最常用！）
# ---------------------------------------------------------------
# select() = 用 CSS 选择器找多个元素
# select_one() = 找第一个匹配的元素
# 
# 常用选择器语法：
#   标签名        → 找这种标签的所有元素（如 p, a, div）
#   .class名      → 找 class 等于这个的元素（如 .intro, .news-item）
#   #id名         → 找 id 等于这个的元素（如 #news）
#   父选择器 子选择器 → 找父元素下面的子元素（如 #news li）

print("\n" + "=" * 50)
print("2. CSS 选择器")
print("=" * 50)

# 按class找
items = soup.select(".news-item") # 找所有 class="news-item" 的元素
print(f"找到{len(items)}条新闻")
for item in items:
    a_tag = item.find("a") # 在每个 li 标签里找到 a 标签
    print(f" -{a_tag.text} -> 链接：{a_tag['href']}']") # a_tag['href'] = 获取 a 标签的 href 属性 ; herf 是 a 标签的一个属性，表示链接地址

# 按id找
# id 是 HTML 中的一个属性，表示元素的唯一标识;一个网页中 id 应该是唯一的，不能重复的；我们可以用 #id 来选择这个元素
news_div = soup.select_one("#news") # 找 id="news" 的元素
# #news 是 css 选择的语法，# 表示 id 选择器，news 是 id 的值；select_one() 方法会返回第一个匹配的元素

# 按标签找
productss = soup.select(".product") # 找所有 class="product" 的元素
print(f"找到{len(productss)}个产品")
for product in productss:
    name = product.find("h3").text # 在每个 product div 里找到 h3 标签，获取产品名称
    price = product.find("p", class_="price").text # 在每个 product div 里找到 class="price" 的 p 标签，获取价格
    rating = product.find("span", class_="rating").text # 在每个 product div 里找到 class="rating" 的 span 标签，获取评分
    print(f" - {name}:{price}，评分:{rating}")

#层级选择器：找产品列表下面的所有产品
products = soup.select(".product-list.product") # 找 class="product-list" 下面的 class="product" 的元素
print(f"\n找到{len(products)}个产品")
for p in products:
  name = p.find("h3").text # 在每个 product div 里找到 h3 标签，获取产品名称
  price = p.select_one(".price").text # 在每个 product div 里找到 class="price" 的元素，获取价格
  rating = p.select_one(".rating").text # 在每个 product div 里找到 class="rating" 的元素，获取评分
  data_price = p.get("data-price") #自定义属性，获取data-price的值
  print(f" - {name}:{price}({rating},data-price = {data_price}元)")

# ---------------------------------------------------------------
# 3. 提取属性的几种方法
# ---------------------------------------------------------------
print("\n" + "=" * 50)
print("3. 提取属性的方法")
print("=" * 50)
#属性 = 标签的特征，比如 href、class、id、data-price 等等；用 .get()  or 用 [] 获取


first_a = soup.find("a")
print(f"标签名：{first_a.name}") # 标签名
print(f"href属性:{first_a['href']}") #像字典一样访问
print(f"href属性（get方式）：{first_a.get('href')}") #get() 更安全，没有就返回none
print(f"所有属性：{first_a.attrs}") #所有属性的字典

# ---------------------------------------------------------------
# 4. 找到父元素和兄弟元素
# ---------------------------------------------------------------
print("\n" + "=" * 50)
print("4. 父元素和兄弟元素")
print("=" * 50)

first_product = soup.select_one(".product")
print(f"第一个产品：{first_product.find('h3').text}") # get first product name
print(f"它的父元素的class：{first_product.parent.get('class')}")
# parent = 父元素，找到这个元素的上一级元素
#兄弟元素 = 同级元素，找到这个元素的同一级别的其他元素
print(f"下一个兄弟产品：{first_product.find_next_sibling('div').find('h3').text}")

# ---------------------------------------------------------------
# 5. 实战练习：提取所有产品信息存到列表
# ---------------------------------------------------------------
print("\n" + "=" * 50)
print("5. 实战：把产品数据整理成列表")
print("=" * 50)

product_list = []
for p in soup.select(".product"):
   product_data = {
      "name" : p.find("h3").text,
      "price": p.select_one(".price").text,
      "price_num":int(p.get("data-price")),
      "rating":p.select_one(".rating").text,
   }
   product_list.append(product_data)

for p in product_list:
   print(f" {p['name']}: {p['price_num']} 元,{p['rating']}")

# ---------------------------------------------------------------
# 小结
# ---------------------------------------------------------------
print("\n" + "=" * 50)
print("第2步小结:")
print("  BeautifulSoup 四步走：")
print("    1. soup = BeautifulSoup(html, 'lxml')  # 创建解析对象")
print("    2. soup.select('选择器')               # 用 CSS 选择器找元素")
print("    3. element.text                        # 提取文字")
print("    4. element.get('属性名')               # 提取属性")
print("")
print("  常用选择器：")
print("    标签名   → p, a, div, h1")
print("    .class名 → .item, .product")
print("    #id名    → #header, #main")
print("    后代选择 → .product-list .product")
print("=" * 50)
      
