# 信息安全 2077（iPadOS/iOS）

查看页面源码，观察到 POST 请求中的 `If-Unmodified-Since` 头。阅读请求失败后的处理代码，发现只处理了时间早于某一日期的情况，因此推断服务器不会判断截止日期。根据题目信息，该比赛举办于 2077 年，因此将年份设置为 2078 即可通过服务器校验。

构造请求：

> 方法：POST
> 链接：http://202.38.93.241:2077/flag.txt
> 请求头：
> If-Unmodified-Since: Sat, 01 Jan 2078 00:00:00 GMT
> User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) HEICORE/49.1.2623.213 Safari/537.36

可以[使用 JSBox](2077.js) 构造请求并展示结果，或者用 Anubis 构造请求后查看响应。