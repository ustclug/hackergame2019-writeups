# 网页读取器

- 题目分类：web

- 题目分值：150

今年，刚刚学会网络编程的小 T 花了一点时间，写了一个非常简单的网站：输入一个 URL，返回对应的内容。

不过小 T 想对用户访问的站点进行一些限制，所以他决定自己来解析 URL，阻止不满足要求的请求。这样也顺便解决了 SSRF（Server-Side Request Forgery, 服务器端请求伪造）的问题。

想象很美好，但小 T 真的彻底解决了问题吗？

[打开/下载题目](http://202.38.93.241:10020/)

---

本题的灵感来源于 *A New Era of SSRF - Exploiting URL Parser in Trending Programming Languages!*。而这道题主要的点就是 URL 的 parser 和 requester 的不一致性导致的意料之外的 SSRF 问题。

## 关于 URI（统一资源标志符）

URL（统一资源定位符）是 URI 最常见的一种形式，而 URL 就是我们常说的「网址」。

根据 [RFC3986 (*Uniform Resource Identifier (URI): Generic Syntax*)](https://tools.ietf.org/html/rfc3986) 第 3 节的描述，URI 的语法大概长成下面这个样子：

```
scheme:[//authority]path[?query][#fragment]
```

其中用 `[]` 围住的是可选的。然后我们来看一下各部分：

- 协议 (scheme)：访问资源使用的协议，比如说 `http`, `https` 之类的。
- 来源 (authority)：来源中包含了主机名，和可选的用户信息和端口号，比如 `www.ustc.edu.cn`, `admin:admin@www.example.com:2333`（使用用户名为 admin，密码为 admin，访问 www.example.com 的 2333 端口获取资源）。
- 路径 (path)：比如说 `/cgi-bin`, `/a/b/c/d/e/f/g` 等，有等级 (hierarchical) 关系。
- 查询 (query)：没有等级 (non-hierarchical) 关系的数据。一般来说，查询中的参数会被网站的后端获取到，然后进行对应的处理，比如 `?q=keyword`，`?a=1&b=2`。
- 片段 (fragment)：指向一个更低级别的资源，例如 `#Examples`，浏览器访问时会滚动到 `id` 为 `Examples` 的标签。如果写过单页面应用 (SPA) 的同学可能会知道，一些框架处理路由时使用 hash 模式，这里的 hash 就是片段开头的 `#`。

## 解法

我们围观一下小 T 自己造的 parser 轮子：

```python
def check_hostname(url):
    for i in whitelist_scheme:
        if url.startswith(i):
            url = url[len(i):]  # strip scheme
            url = url[url.find("@") + 1:]  # strip userinfo
            if not url.find("/") == -1:
                url = url[:url.find("/")]  # strip parts after authority
            if not url.find(":") == -1:
                url = url[:url.find(":")]  # strip port
            if url not in whitelist_hostname:
                return (False, "hostname {} not in whitelist".format(url))
            return (True, "ok")
    return (False, "scheme not in whitelist, only {} allowed".format(whitelist_scheme))
```

看起来似乎没有什么问题：把协议丢掉，来源后面的东西丢掉，用户信息和端口号也丢掉，剩下来的不就是主机名吗？对大部分的 URL，这没有太大的问题。

但如果我们构造一个奇怪的 URL 会怎么样？如果我们能想办法让 `check_hostname` 解释出主机名为 `example.com` 的同时，让 `requests.get()` 实际访问我们想要的地址，那就成功了。

预期解就使用到了 fragment（当然用 `?` 也是可以的）。现有的 requester 都会直接忽略掉 `#` 后面的东西，毕竟这对请求网站内容是没有意义的。但这里的代码没有对 `#` 进行任何处理，而且会粗暴地忽略掉 `@` 前面的所有内容。

也就是说，可以构造出类似于下面的东西：

```
http://web1/flag#@example.com
```

输入进去，就拿到 flag 啦。

~~所以说，有的时候，轮子还是不要自己瞎造的好。~~