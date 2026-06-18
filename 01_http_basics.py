# === 第1步：HTTP 请求基础 ===
#
# 【爬虫概念】
# 爬虫的本质 = 模拟浏览器发送请求，获取网页内容
# 你在浏览器地址栏输入网址按回车 = 发送 GET 请求
# 你填写表单点提交 = 发送 POST 请求
# 爬虫用代码做同样的事，然后把返回的内容提取出你需要的数据
#
# 【Git 概念】
# git init    → 初始化仓库（给项目装上"时光机"）
# git add     → 把文件放入暂存区（告诉 Git "我要跟踪这个改动"）
# git commit  → 提交到历史记录（给当前状态拍一张"快照"）
# 流程：工作区 → 暂存区 → 仓库

import requests

# ------ 1. 最简单的 GET 请求 ------
# requests.get() 就像在浏览器地址栏输入网址

response = requests.get("https://www.baidu.com")
print("状态码：", response.status_code )# 200 表示成功
print("编码：", response.encoding) # 服务器告诉我们内容的编码方式 网页使用的字符编码
print("内容长度：", len(response.text),"字节") # 网页内容的长度 -》 网页的大小

# ------ 2. 带参数的 GET 请求 ------
# 就像搜索时 URL 后面会带上 ?keyword=python&page=1
params = {"wd":"python"}# 这个字典会被转换成 URL 参数 wd means "搜索关键词"
response = requests.get("https://www.baidu.com/s",params = params)
 # 这个字典会被转换成 URL 参数 keyword means "搜索关键词"，page means "页码"
#response = requests.get("https://httpbin.org/get",params = params)# httpbin.org 是一个专门用来测试 HTTP 请求的服务, parameters are sent as query string in the URL
print(f"实际请求的完整URL: {response.url}")
print(f"状态码: {response.status_code}")
print(f"搜索结果页面长度: {len(response.text)} 字符")
print()
 # 把返回的 JSON 格式内容转换成 Python 字典
#json 是一种数据格式，类似于 Python 的字典和列表，可以用来表示结构化数据。JSON 格式的字符串可以通过 json.loads() 函数转换成 Python 的字典或列表，反之亦然。
#用到json的时候，通常是因为我们从网络上获取的数据是以 JSON 格式返回的，我们需要把它转换成 Python 的数据结构来进行处理。比如在这个例子中，httpbin.org/get 返回的内容是一个 JSON 格式的字符串，包含了我们发送请求时的一些信息，比如 URL、请求头、查询参数等。通过 response.json() 方法，我们可以把这个 JSON 字符串转换成一个 Python 字典，这样我们就可以通过键来访问其中的数据了。

# print("response URL:",data["url"]) # 服务器会把我们发送的 URL 返回来，看看参数是否正确传递了
#URL 是服务器接收到的完整 URL，包括参数部分，具体定义是服务器接收到的 URL 包含协议、域名、路径和查询参数等组成部分，通常格式为 "协议://域名/路径?查询参数"。在这个例子中，URL 是 "https://httpbin.org/get?keyword=python&page=1"，其中 "https://httpbin.org/get" 是协议、域名和路径部分，"?keyword=python&page=1" 是查询参数部分。域名是指服务器的地址，在这个例子中是 "httpbin.org"，路径是指服务器上资源的位置，在这个例子中是 "/get"。
# 打个比喻：URL 就像是一个地址，协议是交通工具（比如 HTTP 就像是汽车），域名是城市（比如 httpbin.org），路径是街道和门牌号（比如 /get），查询参数就像是你在地址后面写的备注（比如 ?keyword=python&page=1），告诉服务器你想要什么样的内容。
try:
    data = response.json()  # 把 JSON 格式的响应转成 Python 字典
    print("✅ JSON解析成功！")
    print("服务器收到参数:", data["args"])
except Exception as e:
    print(f"❌ JSON解析失败: {e}")
    print("完整响应头:", dict(response.headers))
print()
# ------ 3. 自定义请求头 ------
# User-Agent = 告诉服务器你用的是什么浏览器
# 如果不设置，requests 会告诉服务器"我是 Python 程序"
# 有些网站会拒绝这样的请求，所以我们需要伪装一下

# 先看一下默认的 User-Agent 长什么样
print("--- 默认情况（不设置User-Agent）---")
response = requests.get("https://httpbin.org/user-agent",timeout = 10)
#httpbin.org/user-agent 是一个专门用来测试 User-Agent 的接口，它会把服务器收到的 User-Agent 返回来，让我们看看默认情况下 requests 发送的 User-Agent 是什么样子的。通常情况下，requests 会发送一个类似于 "python-requests/2.25.1" 这样的 User-Agent，告诉服务器这是一个 Python 程序在发送请求。某些网站可能会拒绝这样的请求或者返回不同的内容，所以我们需要设置一个更像浏览器的 User-Agent 来伪装一下。
if response.status_code == 200: # 200 表示请求成功
    data = response.json()
    print("服务器收到的User-Agent:", data["user-agent"])
else:
    print(f"无法解析，原始响应内容：{response.text[:100]}") # 如果请求失败了，我们就打印前100个字符的原始响应内容，看看服务器到底返回了什么，这样我们就可以判断是哪里出了问题了。


# User-Agent 告诉服务器"我是谁"，很多网站会检查这个字段来判断请求是否来自浏览器，或者是爬虫
headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"} #伪装成谷歌浏览器
# 这个 User-Agent 模拟了一个常见的浏览器，如果不设置，某些网站可能会拒绝响应或者返回不同的内容
#headers 是一个字典，包含了 HTTP 请求头的信息，HTTP 请求头是一些键值对，用来告诉服务器关于客户端的一些信息，比如 User-Agent、Accept、Cookie 等等。在这个例子中，我们设置了 User-Agent 这个请求头，告诉服务器我们是一个使用 Windows 10 操作系统的浏览器，这样可以增加我们请求被接受的概率。
#打个比方：HTTP 请求头就像是你在邮寄包裹时填写的标签，上面写着你的名字、地址、联系方式等信息，告诉邮递员这个包裹是谁寄的，应该送到哪里，以及如何联系你。在 HTTP 请求中，请求头就是告诉服务器这个请求是从哪里来的，是什么类型的客户端发出的，以及其他一些相关的信息，这样服务器就可以根据这些信息来决定如何处理这个请求了。
#而headers 在这个比方中就相当于你在邮寄包裹时填写的标签上的信息，比如你的名字、地址、联系方式等，这些信息就是 HTTP 请求头中的键值对，告诉服务器这个请求是从哪里来的，是什么类型的客户端发出的，以及其他一些相关的信息。
#所谓的 User-Agent 就是 HTTP 请求头中的一个键，它的值是一个字符串，告诉服务器这个请求是从什么样的客户端发出的，比如浏览器、爬虫、手机应用等等。服务器可以根据 User-Agent 的值来判断这个请求是否来自一个正常的浏览器，如果不是，可能会拒绝响应或者返回不同的内容。


print("--- 自定义User-Agent（伪装Chrome）---")
try:
    response = requests.get("https://httpbin.org/user-agent", headers=headers, timeout=10)
    if response.status_code == 200:
        print(f"自定义User-Agent: {response.json()['user-agent']}")
except Exception as e:
    print(f"httpbin访问超时，没关系，不影响我们学习: {e}")
print()

# response = requests.get("https://httpbin.org/get",headers = headers)
# data = response.json() # 把返回的 JSON 格式内容转换成 Python 字典 一般会返回的是一个 JSON 格式的字符串，包含了我们发送请求时的一些信息，比如 URL、请求头、查询参数等。通过 response.json() 方法，我们可以把这个 JSON 字符串转换成一个 Python 字典，这样我们就可以通过键来访问其中的数据了。
# print("服务器收到的User-Agent:",data["headers"]["User-Agent"])
#data 里面包含的子字典有 "args"（查询参数）、"headers"（请求头）、"origin"（客户端 IP 地址）和 "url"（服务器接收到的完整 URL）。我们通过 data["headers"]["User-Agent"] 来访问请求头中的 User-Agent 字段，看看服务器收到了什么样的 User-Agent。
#而对于每个子字典，他们的分别包含的键值对如下：
# "args" 包含了我们发送的查询参数，有 "keyword" 和 "page" 两个键，分别对应我们在 params 字典中设置的值 "python" 和 1。
# "headers" 包含了我们发送的请求头，有 "Accept"、"Accept-Encoding"、"Host"、"User-Agent" 等等，其中 "User-Agent" 是我们设置的那个值 "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"。
# "origin" 包含了客户端的 IP 地址，这个值可能会根据你的网络环境而不同。
# "url" 包含了服务器接收到的完整 URL，包括查询参数部分，这个值应该是 "https://httpbin.org/get?keyword=python&page=1"，说明我们的参数正确地传递了。

# ------ 4. POST 请求 ------
# POST 用于提交数据，比如登录、注册、提交表单

# POST = 向服务器提交数据，比如登录、搜索、提交表单
# 我们用本地方式演示，不依赖httpbin
print("=" * 50)
print("4. POST 请求概念")
print("=" * 50)
print("""
POST 和 GET 的区别：
  GET: 参数放在URL里，比如 https://www.baidu.com/s?wd=xxx
        长度有限制，对用户可见（浏览器地址栏能看到）
  POST: 参数放在请求体里，不在URL中
        长度没有限制，不显示给用户

常见场景：
  GET: 浏览网页、搜索关键词（大多数爬虫都是GET）
  POST: 登录、注册、提交评论、上传文件
""")

# from_data = {"username":"test_user","password":"test_pass"}
# response = requests.post("https://httpbin.org/post",data = from_data)
# data = response.json()
# print("提交的数据：", data["from"])

# ------ 5. 超时和异常处理 ------
# 网络请求可能失败，必须加保护

try:
    response = requests.get("https://www.baidu.com",timeout = 5) # 设置超时时间为 5 秒
    print("query succeeded:",response.status_code)
except requests.exceptions.Timeout: # 如果请求超过了设置的超时时间，就会抛出 Timeout 异常，我们可以捕获这个异常来处理超时的情况
    #except 是 Python 中的一个关键字，用来捕获和处理异常。当我们使用 try-except 语句时，Python 会尝试执行 try 块中的代码，如果在执行过程中发生了指定的异常（在这个例子中是 requests.exceptions.Timeout），就会跳转到 except 块中执行相应的代码来处理这个异常。在这个例子中，如果请求超过了设置的超时时间，就会抛出 Timeout 异常，我们捕获这个异常后，打印 "query timed out" 来告诉用户请求超时了。
    #exceptions 是 requests 模块中的一个子模块，包含了各种与请求相关的异常类，比如 Timeout、ConnectionError、HTTPError 等等。当我们使用 requests 模块发送请求时，如果发生了某些错误，比如网络连接失败、请求超时、服务器返回错误状态码等等，就会抛出相应的异常，我们可以通过捕获这些异常来处理错误情况，避免程序崩溃。
    print("query timed out")
except requests.exceceptions.RequestException as e: # 捕获其他所有与请求相关的异常，RequestException 是 requests 模块中所有请求异常的基类，捕获这个异常可以处理所有与请求相关的错误情况，比如网络连接失败、请求超时、服务器返回错误状态码等等。我们还可以通过 as e 来获取这个异常对象，查看具体的错误信息。
    print("query failed:",e)

# ------ 小结 ------
# requests.get()  → 获取网页（最常用）
# requests.post() → 提交数据
# headers 的 User-Agent → 伪装身份
# timeout + try/except → 防止程序崩溃
# .text → 网页文本 / .json() → JSON数据 / .content → 原始字节

# ------ 小结 ------
print("\n" + "=" * 50)
print("📝 第1步小结:")
print("=" * 50)
print("""
  🔹 requests.get(url)  → 获取网页（爬虫90%都是这个）
  🔹 requests.post(url) → 提交数据（登录/搜索）
  🔹 params=  → URL 查询参数
  🔹 headers= → 请求头，其中 User-Agent 最重要（伪装浏览器）
  🔹 timeout= → 超时时间，永远记得设置！
  🔹 try/except → 处理异常，防止程序崩溃
  🔹 .text  → 得到文本（HTML网页）
  🔹 .json() → 得到JSON数据（API接口）
  🔹 .content → 得到二进制（图片/文件）
""")
print("=" * 50)



# about git

#------ 6. Git 基础 ------
# Git 是一个版本控制系统，帮助我们管理代码的历史记录和协作开发
# git init    → 初始化仓库（给项目装上"时光机"） 在一个文件夹的终端里运行 git init 就会在这个文件夹里创建一个 .git 的隐藏文件夹，这个文件夹就是 Git 仓库，Git 会在这里记录这个项目的所有历史版本和改动信息，就像给这个项目装上了一个"时光机"，让我们可以随时回到过去的某个状态，查看历史记录，或者恢复到之前的版本。

# 1. 查看当前状态
# 告诉你哪些文件还没被 Git 跟踪
# git status

# 2. 把 01_http_basics.py 加入暂存区
# 告诉 Git："这个文件我做好了，准备提交"
# git add 01_http_basics.py

# PS: 你也可以用 git add . 来一次性把所有改动的文件都加入暂存区，但在实际开发中，建议你还是一个一个文件地添加，这样可以更清晰地知道每次提交都包含了哪些改动，避免不小心提交了一些不相关的文件或者改动。
# PPS: git rm --cached <file>..." to unstage 这个文件，意思是如果你不小心把一个文件加入了暂存区，想要撤销这个操作，可以使用 git rm --cached <file> 来把这个文件从暂存区移除，这样它就不会被提交了，但这个文件在你的工作区还是存在的，不会被删除。
# HEAD 是 Git 中的一个指针，指向当前分支的最新提交，也就是我们当前所在的位置。当我们提交新的改动时，HEAD 会自动移动到新的提交上，记录下这个新的状态。通过查看 HEAD，我们可以知道我们当前处于哪个版本，以及这个版本的历史记录是什么样子的。
# 使用git reset HEAD <file> 可以把这个文件从暂存区移除，撤销 git add 的操作，这样这个文件就不会被提交了，但它在你的工作区还是存在的，不会被删除。这个命令的作用是把 HEAD 指针回退到上一个提交状态，同时把指定的文件从暂存区移除，让你可以重新修改或者选择是否要加入暂存区了。
# PPPS: 如果你想查看哪些文件已经被加入了暂存区，可以用 git status 来查看，Git 会告诉你哪些文件在暂存区，哪些文件还没有被跟踪，哪些文件有改动但还没有加入暂存区等等。
# PPPPS: tab 补全功能在 Git 中也非常有用，比如当你输入 git add 01_ 然后按下 tab 键，Git 会自动补全文件名，帮助你快速输入命令，避免打错文件名或者命令。

# 3. 查看状态确认一下文件在暂存区了
# git status

# 4. 正式提交到历史记录
# -m 后面是提交说明，说明这次做了什么
# git commit -m "step1: 完成HTTP请求基础 - GET/POST/headers/超时/异常处理"
# -m 是 commit 的一个参数，表示提交说明（message），它后面跟着的字符串就是这次提交的说明，告诉其他人或者未来的自己这次提交做了什么改动。写一个清晰的提交说明是非常重要的，这样在查看历史记录的时候就能快速了解每次提交的内容和目的了。

# 5. 查看提交历史，确认提交成功
# git log --oneline
# --oneline 是 git log 的一个参数，表示以简洁的单行格式显示提交历史，每个提交只显示一个简短的哈希值和提交说明，这样可以更清晰地查看提交历史，快速找到你想要的提交了。