# 十次方根

这是一道数论（也算是密码学）题目，题目的 flag 被编码为了一个大整数 n，n 需要满足 10 次方 mod (x * y^3) 之后等于 z。

这题考察的是 RSA 加密中 e 与 phi(n) 不互素的情况。当然，n 也不只是分解成 p * q 的形式，而是 p * q^3 的形式。

这题相比于标准的 RSA 有以下几个坑：

- 变量名使用了 x、y、z，与 RSA 的常见记法格格不入，但这不重要。**我们下面统一使用 RSA 的记法。**
- 模数是 p * q^3 的形式。但是套公式可以很容易知道 phi(n) 是 (p-1)(q-1)q^2。
- e 与 phi(n) 不互素，所以会有多解。我们可以全都解出来，然后判断转换为字符串之后是否以 `flag` 开头。

**出题人数理基础不够好，并不知道这类问题有没有通用解法或者比较优雅的解法，也不知道是否有软件可以直接计算这类问题。**

所以出题人只有一个能跑出来但是很糟糕的解法。

## 出题人糟糕的解法

比较显然的一点是，不管 mod n 开几次方，如果你不能分解 n，那么都不可能在可接受时间内算出来，这是 RSA 加密的安全性的基础。所以直接在各种软件（包括但不限于 SageMath、Mathematica、SymPy）中，都不大可能直接求解这个方程，你没办法告诉这些软件 n 的分解是那样的形式（如果有办法请告诉我）。

所以我为了避免自己实现算法（因为懒），尝试了把 sympy 的整数分解函数 `sympy.ntheory.residue_ntheory.factorint` 替换成了我自己的版本，它会根据我已知的大素数来直接返回 n 的分解。

但是我发现，10 次方根还是跑不出来，但是 2 次方根可以跑出来，所以我再开个 5 次方就行了。

先找到 c 的一个 5 次方根，然后找到 1 的一些可能的 5 次方根，然后就可以得到所有 c 的 5 次方根。（都是 mod n 意义下，我不确定是否找全了）

然后再对每个数 mod n 开平方就行了。

代码如下：

```python
#!/usr/bin/env python3

from easy_math import x as p, y as q, z as c
from sympy.ntheory.residue_ntheory import sqrt_mod
import sympy.ntheory.residue_ntheory
import gmpy2


def factor_(nn, *args, **kwargs):
    t = 0
    while nn % p == 0:
        t += 1
        nn //= p
    s = 0
    while nn % q == 0:
        s += 1
        nn //= q
    if nn != 1:
        print(nn)
        return None
    return {p: t, q: s}


sympy.ntheory.residue_ntheory.factorint = factor_

n = p * q ** 3
phi = (p - 1) * (q ** 2) * (q - 1)
root_5th_of_c = pow(c, gmpy2.invert(5, phi // 5), n)
root_5th_of_1_all = set(pow(i, (phi // 5), n) for i in range(1, 20))
root_5th_of_1_all = set(r for r in set(root_5th_of_1_all) if pow(r, 5, n) == 1)
root_5th_of_c_all = [root_5th_of_c * r % n for r in root_5th_of_1_all]
m_all = [m for r in root_5th_of_c_all for m in sqrt_mod(r, n, True)]
print(len(m_all))
for m in m_all:
    h = hex(m)[2:]
    if len(h) % 2 == 0 and bytes.fromhex(hex(m)[2:]).startswith(b"flag"):
        print(bytes.fromhex(hex(m)[2:]).decode()[:32])
```

我相信一定有人有比我更优雅，并且更容易理解的做法。
