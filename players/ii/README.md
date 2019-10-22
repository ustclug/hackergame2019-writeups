# Write-up

## 宇宙终极问题
### 42
百度
```python
x, y, z = -80538738812075974, 80435758145817515, 12602123297335631
```
### Everything
问题：找到8个整数a, b, c, d, i, j, k and l, such that
a^3 + b^3 + c^3 + d^3 = i^2 + j^2 + k^2 + l^2 = random_prime(2^256) * random_prime(2^256)

可以百度到四平方和定理，但它只证明了可行性，对于计算求解似乎没什么用。
也暂时不清楚目标数字为两个质数的乘积这个条件有什么用。

百度可知，较小的模9不为4或5的整数，绝大多数可写为三立方和；这个结论或许做可以作为寻找a、b、c、d的跳板，算法无思路。

Google一下“four cube sum”，得到一个[网站](https://www.alpertron.com.ar/FCUBES.HTM)。
这个网站可以直接求解四立方和，但是有提示：`This applet does not work if the number is congruent to 4 or 5 (mod 9)`，所以有一定概率失败，如果失败就重新来一遍就好了。
具体用到算法有待研究。

求解四平方和的思路：

对于素数p，x^2 + y^2=p有整数解的充分必要条件是`p=2`或`p=4k+1`，且该解可快速算得。求解需要先使用TonelliShanks算法求p-1的模p平方根x0，也即找到一个x0使得x0的平方模p为-1；然后令y0=1；这样得到:
`x0^2 + y0^2 = mp`，其中m为正整数。

然后再将m降为1即可。这些算法应该可以在信息安全数学基础的课本上找到。

要找`i^2 + j^2 + k^2 + l^2 = n`，其中n为较大奇数。
考虑随机取奇偶性相同的i、j，若`k^2 + l^2 = n - i^2 - j^2`为质数且模4余1，则四平方和的解即可找到。

求解四平方和代码如下，运行时间几乎可以忽略。
执行的时候记得把main中的n替换为目标的数值。
```python
import gmpy2
from Crypto.Util.number import getPrime, getRandomInteger


def TonelliShanks(p, a):
    if pow(a, (p - 1) // 2, p) != 1:
        return -1
    q = p - 1
    m = 0
    while q % 2 == 0:
        q //= 2
        m += 1
    z = 0
    while pow(z, (p - 1) // 2, p) != p - 1:
        z = getRandomInteger(10)
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    while m > 1:
        tmp = pow(t, 1 << (m - 2), p)
        if tmp != 1:
            r = r * c % p
            t = t * (c * c % p) % p
        c = c * c % p
        m -= 1
    return r


def find_small_m(x, y, p):
    x2y2 = x * x + y * y
    m = x2y2 // p
    assert 0 == (x2y2 % p) and 0 == (x2y2 % m)
    while 1 < m:
        u, v = x % m, y % m
        if u * 2 > m:
            u -= m
        if v * 2 > m:
            v -= m
        u2v2 = u * u + v * v
        mm = u2v2 // m
        assert 0 == (u2v2 % m) and 0 < mm < m
        
        x, y = (u * x + v * y) // m, (u * y - v * x) // m
        x2y2 = x * x + y * y
        m = x2y2 // p
        assert 0 == (x2y2 % p) and 0 == (x2y2 % m)
    
    return x, y, m


def get2square(r):
    if r == 2:
        return 1, 1
    assert 1 == r % 4 and gmpy2.is_prime(r)
    x0 = TonelliShanks(r, r - 1)
    assert r - 1 == pow(x0, 2, r)
    k, l, m = find_small_m(x0, 1, r)
    assert k * k + l * l == m * r
    assert 1 == m
    return k, l


def get4square(n):
    print("n =", n)
    while True:
        i = getRandomInteger(100)
        j = getRandomInteger(100)
        j ^= (i ^ j) & 0x1
        r = n - i * i - j * j
        if 1 == r % 4 and gmpy2.is_prime(r):
            break
    print("r =", r)

    k, l = get2square(r)
    
    assert i * i + j * j + k * k + l * l == n
    print("i =", i)
    print("j =", j)
    print("k =", k)
    print("l =", l)
    return i, j, k, l


if __name__ == '__main__':
    n = getPrime(256) * getPrime(256)
    print(get4square(n))

```

当然从别人的WP那里发现四平方和问题也可以在这个网站解决：
[四平方和计算](https://www.alpertron.com.ar/FSQUARES.HTM)

### Last Question
问题：找到2个整数 p and q, such that p^2 + q^2 = randint(2^256)。
随机数的双平方和分解问题。

查一下关于两个数平方和的内容，在[wikipedia](https://en.wikipedia.org/wiki/Sum_of_two_squares_theorem) 中看到`An integer greater than one can be written as a sum of two squares if and only if its prime decomposition contains no prime congruent to 3 modulo 4 raised to an odd power`，翻译一下就是：整数n能分解为两个整数的平方和的充要条件是，n的质因数分解不存在(4k+3)型质数的奇数次方。

所以，对于随机的n，只能有一定概率有解。
如果有解，能否快速算出呢？这是另一个问题了。结论是：只要已知其质因数分解，那么就可以快速算出。

注意到，如果有`x^2 + y^2 = p` 和 `u^2 + v^2 = q`，那么就有恒等式：
`p*q=(u*x + v*y)^2 + (u*y - v*x)^2`，

也就是说如果n的因数全部已经写成了双平方和的形式，那么只需要反复运用上面的等式就可以把n也写成双平方和。

（质因数分解我用的是yafu，如果某个数yafu分解时间太长也跳过重来就好。）

上一小问的过程中用到了对“4k+1”型质数的双平方和分解，是可以瞬间完成的。

对n的质因数构成分如下情况讨论：
1. 如果n本身是“4k+1”型质数，应用上一小问的方法，立刻完成。
2. 如果n的质因数分解只包含“4k+1”型质数，使用上面的恒等式和上一小问的方法，立刻完成。
3. 如果n的质因数分解中，除了“4k+1”型质数，还包括2的若干次方；由于`2 = 1^2 + 1^2`，所以跟情况2一样可以解决。
4. 如果n的质因数分解中，除了2和“4k+1”型质数，只包括若干个“4k+1”型质数的偶次方，那么偶次方本身即可写成两个数平方和的形式 （`自身平方根^2 + 0^2`），然后再应用上面的恒等式也可解决。
5. 如果n的质因数分解中，包含“4k+3”型质数的奇数次方，那么无解。

比如说我最后拿到flag时得到的随机数是
```python
n=88198781941253046930688691757645075291191233647327468276701864250634373543813
```
质因数分解为
```python
n=89*577*1717500086484782718257719933745741734488564127652278703808966647530511821
```
这三个数都是“4k+1”型质数。
把它们分别放到get2square函数中运行，这个函数在上一小问的代码中出现过。
可以得到：
```python
89=5^2+8^2
577=24^2+1^2
1717500086484782718257719933745741734488564127652278703808966647530511821=1303274471958470822478593977547211805^2+137752449074968420575899896690938786^2
```
那么就有`89*577 = (5*24 + 8*1)^2 + (5*1 - 8*24)^2 = 128^2 + 187^2`。
同样的方法就可以得到原来n的分解了。

写一个小函数实现这个过程，输入是n和一个list，list的内容是它的所有质因数，要求它们都是“4k+1”型质数。其中调用了get2square函数。
（至于质因数分解中包含“4k+3”型质数偶次方的情况，这里的代码没有考虑到，可以自己改一下一下。因为一般多尝试几次就会出现不包含“4k+3”型质数的n。）
```python
def get2square_list(n, primes):
    assert list == type(primes)
    check_product = 1
    for p in primes:
        assert 2 == p or (1 == p % 4 and gmpy2.is_prime(p))
        check_product *= p
    assert check_product == n
    u, v = 1, 0
    for p in primes:
        x, y = get2square(p)
        u, v = u * x + v * y, u * y - v * x
    assert u * u + v * v == n
    return u, v
```
总结一下，想拿到最后的flag需要这么几步的成功通过：
1、第二小问中，四立方和的求解，有一定概率那个网站分解不了给定的数。
2、计算四立方和，这一步瞬间完成，不会失败。
3、最后一问中，双平方和的求解，有较大的概率n的质因数分解中包含非“4k+1”型的质数。
失败了就重来几次，多几次就成功了。
（没写连socket的脚本，每次都是手动复制的，web师傅们可以考虑写个脚本，让后把其中的一些判断自动化一下，请多指教。）

## 驴啃计算器
（数理基础不够扎实，这题做的方法实在丑陋。只用了cos、exp、sqrt、R2D、tan、D2R。）
首先cos+exp可以得到一个自然对数的底数e，那就一切从e出发。（好处在于它是个大于1的数）
只考虑正数就行，负的手动加"-x"都行。（下文中的delta指的是当前值与目标数值的误差。

首先用exp+sqrt，比目标数大就sqrt，比目标数小就exp，这个过程没什么数学根据，就是瞎蹦，但效果不错，基本都能蹦到比较近的地方。delta可以达到1e-3，代码中这一步delta设为1。这个过程很快，几十或者几百次就可以。

然后考虑怎么微调一下。
我就想到tan可以把数值略微调大一点，而且跟零靠的越近，幅度就越小。然后R2D和D2R就可以当做一个调整数量级的东西。
比如说我已有的数比目标数稍微小一点，但是如果tan一下可能增幅就太大了，那我就先D2R一下再tan，然后再R2D回到原来的数量级，这样比直接tan的增幅小一点。如果还是太大的话那就多D2R几次，下几个数量级再tan，tan完再R2D同样的次数恢复回来就好了。
如果比pi/2大的话肯定不能直接tan的，要先D2R到小于pi/2。如果一次tan的增幅不够就多次连续tan。
用tan+r2d+d2r微调，delta设置小一点就可以了。
这个方法的坏处就是结果比较长，每个数可能需要几千次运算。（复制到表单的时候甚至浏览器有点卡。

然后提交的时候好几次system_error，不知道怎么回事（或许是答案实在太长了），多试了几次就成功了。
代码：
calc函数中的while循环是exp+sqrt，slightly_bigger函数是tan+r2d+d2r微调。结果写进了rst.txt。

```python
import math

ANS_INIT = 'cos,exp'
ANS = 'cos,exp'
delta_big = 1
delta = 1e-8


def cos(x):
    global ANS
    ANS += ',cos'
    return math.cos(x)
def sin(x):
    global ANS
    ANS += ',sin'
    return math.sin(x)
def exp(x):
    global ANS
    ANS += ',exp'
    return math.exp(x)
def sqrt(x):
    global ANS
    ANS += ',sqrt'
    return math.sqrt(x)
def tan(x):
    global ANS
    ANS += ',tan'
    return math.tan(x)
def r2d(x):
    global ANS
    ANS += ',R2D'
    return math.degrees(x)
def d2r(x):
    global ANS
    ANS += ',D2R'
    return math.radians(x)


def calc(n, f):
    global ANS
    ANS = ANS_INIT
    print()
    print("n =", n)
    now = math.exp(1)
    counter1 = 0
    while now > n or abs(now - n) > delta_big:
        counter1 += 1
        if now < n:
            now = exp(now)
        else:
            now = sqrt(now)
        if counter1 % 1000 == 0:
            print("Counter1 =", counter1, "\tgap =", now - n)

    print("\nn =", n, file=f)
    print("Counter1 =", counter1, "\tgap1 =", now - n, file=f)

    now = slightly_bigger(now, n, f)
    
    print("ANS =", ANS, file=f)
    

def slightly_bigger(now, target, f):
    def many_r2d(now, level):
        for _ in range(level):
            now = math.degrees(now)
        return now
    
    d2r_levels = 0
    many_d2r_now = now
    while many_d2r_now >= math.radians(90):
        d2r_levels += 1
        many_d2r_now = math.radians(many_d2r_now)
        now = d2r(now)
    counter2 = 0
    while True:
        new = math.tan(now)
        while many_r2d(new, d2r_levels) < target:
            now = tan(now)
            new = math.tan(now)
            counter2 += 1
            if counter2 % 1000 == 0:
                print("Counter2 =", counter2, "\tgap2 =", many_r2d(now, d2r_levels) - target)
        
        if abs(many_r2d(now, d2r_levels) - target) < delta:
            break
        
        d2r_levels += 1
        now = d2r(now)
    
    for _ in range(d2r_levels):
        now = r2d(now)
    print("Counter2 =", counter2, "\tgap2 =", now - target, file=f)
    return now
    

if __name__ == "__main__":
    f = open('rst.txt', "w")
    calc(37.74301078348758, f)
    calc(92.31201561805436, f)
    calc(17.09413090153682, f)
    f.close()


```


