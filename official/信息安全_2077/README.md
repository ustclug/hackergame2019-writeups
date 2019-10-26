# 信息安全 2077

本题是一道相对简单的 Web 题。通过提示应该可以看得出，我们需要在未来的某一个时刻发送请求。通过打开浏览器 F12 界面，我们很容易抓到整个 HTTP 请求。示例请求如下：

```plain
POST /flag.txt HTTP/1.1
Host: x.x.x.x:2077
Connection: keep-alive
Content-Length: 0
Pragma: no-cache
Cache-Control: no-cache
Sec-Fetch-Mode: cors
Origin: http://x.x.x.x:2077
If-Unmodified-Since: Mon, 22 Oct 2019 03:59:59 GMT
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) HEICORE/49.1.2623.213 Safari/537.36
Accept: */*
Sec-Fetch-Site: same-origin
Referer: http://x.x.x.x:2077/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8

```

其中唯一涉及时间戳的地方只有 `If-Unmodified-Since` 这一 Header。我们再看返回的请求：

```plain
HTTP/1.0 412 PRECONDITION FAILED
Content-Type: text/plain; charset=utf-8
Last-Modified: Fri, 01 Oct 2077 00:00:00 GMT
Content-Length: 0
Server: Werkzeug/0.15.5 Python/3.7.4
Date: Mon, 22 Oct 2019 04:00:00 GMT

```

其中 `Last-Modified` 这一 Header 指示了另一个时间戳（北京时间 2077 年 10 月 1 日早 8 点）。

我们不难猜测，只需要把 `If-Unmodified-Since` 设置在 `Last-Modified` 之后就可以解决问题了。

## 解法一：把电脑时钟调到目标时间之后

别笑，这个真的管用。

如果参赛选手使用的是 Windows，可以在拥有管理员权限的 PowerShell（可使用 Win+X 和 A 打开）里输入 `Set-Date "2077-10-01 08:00:00"` 调整日期以绕过官方配置界面对年份的限制。

改完电脑时钟后重新打开网页就可以了。当然这题如果选用 HTTPS 而非 HTTP，这样做可能就不太合适了。

## 解法二：构造一个设置为目标时间的请求头

构造的方法很多，对于出题人自己来说，最简单的办法是在浏览器的控制台下构造一个 Fetch 请求：

```javascript
(await fetch("/flag.txt", {headers: {"If-Unmodified-Since": "Fri, 01 Oct 2077 00:00:00 GMT"}, method: "POST"})).text()
```

在返回值就能看到 flag 了：

```plain
"flag{Welc0me_to_competit1on_in_2077}"
```

## 注

* 在请求中添加黑曜石浏览器的 User Agent 只是为了致敬去年的题目。实际上至今部分浏览器仍然不支持自定义 User Agent，因此服务器后端实际上是不检查这一 Header 的。源代码中 [`app.py`](src/app.py) 即为本届比赛的后端代码。

* 但愿第 64 届信息安全大赛真的能够在未来顺利举办，如果能够在签到题中使用本题的 flag 就更好了。
