# Flag 红包

- 题目分类：general

- 题目分值：350

你知道「[一个顶俩（liǎ）](https://lia.ustc-zzzz.net/)」吗？

又（快）到了发红包的季节。为了让别人陷入成语红包收不到的尴尬，某同学用了一周的开发时间，精心打造了一个成语接龙 AI。

那么，你能抢到他发出的红包吗？

成语数据库可以在题目网页的右上角下载。

注：上面链接的网站与题目无关。

**补充说明：socket io 需要定时发送 ping，否则会被服务器主动断开连接。**

[打开/下载题目](http://202.38.73.168:8081/?token={token})

---

```
docker pull traefik:1.7
docker pull ubuntu:rolling
docker-compose --compatibility up --build -d
```

上述命令将启动 64 个实例，采用 [Traefik](https://traefik.io/) 进行负载均衡。稍稍修改即可用于本地测试。

## 代码结构

```app``` 目录中为网站代码。其中 ```app.py``` 会加载 ```ladder.cc``` 编译成的 ```libladder.so``` 作为成语接龙引擎。

```gen.py``` 会处理成语数据库中的成语，简单处理必胜必败的情况，然后生成头文件供 ```ladder.cc``` 使用。

```ladder.cc``` 为成语接龙核心引擎（代码较为凌乱，请见谅）。原理是简单的 [MCTS](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)，但是对参数做了一定调整，使其能力有所弱化。成语采用 [csr](https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format)) 稀疏有向图格式存储。

## 开源协议

代码采用 [WTFPL](https://en.wikipedia.org/wiki/WTFPL) 协议开源。

## 题解

什么? 左右互博还需要题解?
