估计这种解法要被官方打死,和之前一样,这题又用的是websocket,直接想到python直接跑,
于是乎
```
#!/usr/bin/python2
#coding:utf-8

from websocket import create_connection
import time



class Stack(object):
	def __init__(self):
		self.items = []
	def is_empty(self):
		return self.items == []
	def push(self, item):
		self.items.append(item)
	def pop(self):
		return self.items.pop()
	def peek(self):
		return self.items[len(self.items)-1]
	def size(self):
		return len(self.items)
	def out(self):
		ret=""
		for i in self.items:
			ret=ret+i+'/'
		print(ret)
		return ret
def init(stack):
	global ws
	ws = create_connection("ws://202.38.93.241:10023/shell")
	print(ws.recv())
	ws.send(token+'\n')
	temp=ws.recv()
	while("PS Maze:/" not in temp):
		temp=ws.recv()
		print(temp)
	temp=ws.recv()
	while("PS Maze:/" not in temp):
		temp=ws.recv()
		print(temp)
	print("初始化成功")
	if(stack.is_empty()):
		pass
	else:
		way=stack.out()
		ws.send('cd '+way+'\n')
		ws.recv()
		temp=ws.recv()
		print(temp)
		try:
			while("PS Maze:/" not in temp):
				temp=ws.recv()
				f.write(temp)
		except Exception:
			init(stack)

def go(way):
	global stack
	try:
		ws.send('cd '+way+'\n')
		stack.push(way)
		ws.recv()
		temp=ws.recv()
		print(temp)
		while("PS Maze:/" not in temp):
			temp=ws.recv()
			f.write(temp)
		ws.send("dir\n")
		ws.recv()
	except Exception:
		init(stack)
		go('./')
		# print(temp)
	temp=""
	t=""
	try:
		while("PS Maze:/" not in t):
			t=ws.recv()
			if("cd" not in t and "Maze" not in t):
				temp=temp+t
				f.write(t)
	except Exception:
		init(stack)
		go('./')
	if("Right" in temp and "Left" not in way):
		go('Right')
	if("Down" in temp and "Up" not in way):
		go('Down')
	if("Up" in temp and "Down" not in way):
		go('Up')
	if("Left" in temp and "Right" not in way):
		go('Left')
	ws.send('cd ../\n')
	temp=""
	try:
		while("PS Maze:/" not in temp):
			# print(temp)
			temp=ws.recv()
	except Exception:
		init(stack)
	stack.pop()

token="416:MEUCIQD4wz3qknMtWb9J2w5b5aPkFXjxeobWbsgdw+kCafOixAIgaLQp/xq0HAoxOX6/ylW3fZ0OSKmU8nFeycjVUqwtrfs="
cookies={'token':'416:MEUCIQD4wz3qknMtWb9J2w5b5aPkFXjxeobWbsgdw+kCafOixAIgaLQp/xq0HAoxOX6/ylW3fZ0OSKmU8nFeycjVUqwtrfs='}



f=open('./ans.txt','w+')
ws=""
stack=Stack()
init(stack)

go("Down")
f.close()
ws.close()

#flag{D0_y0u_1ik3_PSC0r3_n0w_2C6BE488}
```

最初是先左下遍历规则,但是就算家里异常处理,最终还是会死,不过跑了几次之后发现左下跑最后都会回到很靠近0,0的位置,
所以猜左下没有flag,于是改成右下原则,跑了20s,就出结果了
