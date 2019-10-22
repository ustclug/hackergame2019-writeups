## 介绍

这题主要考察的是 websocket 的原理及其调试。只涉及一个非常简单的漏洞

## 编译(部署题目过程不需要编译）
1. 安装 golang
2. 按照 go-bindata，这是一个将静态资源编码到可执行文件的库，使得我们可以产生一个单一的可执行文件。
2. 运行 ./build.sh
3. wa-darwin,wa-linux 和 wa-windows.exe 分别是在对于64位系统中的可执行程序。

在可执行文件同目录下，将flag写入 “flag.txt” 文件中。

## 二进制运行（部署题目过程使用docker部署，不需要执行二进制）

```
./wa-linux
```
程序默认端口 80 端口。

## 容器化（部署题目所需要执行的过程）
构建docker不需要重新运行 build.sh
```
docker-compose up -d
```

## EXP

需要运行 python3 exp.py。注意需要安装依赖

```
pip3 install websocket_client
cd exp  && python3 exp.py
```
