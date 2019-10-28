## 十次方根题解
```python
from easy_math import x,y,z
from Crypto.Util.number import long_to_bytes
'''
step 1: Find roots over mod x,y
step 2: Use Hensel’s lifting to find roots over y**3
step 3: Use crt to find n mod x*y**3
'''
def lift(f, p, k, previous):
    result = []
    df = diff(f)
    for lower_solution in previous:
        dfr = Integer(df(lower_solution))
        fr = Integer(f(lower_solution))
        if dfr % p != 0:
            t = (-(xgcd(dfr, p)[1]) * int(fr / p ** (k - 1))) % p
            result.append(lower_solution + t * p ** (k - 1))
        if dfr % p == 0:
            if fr % p ** k == 0:
                for t in range(0, p):
                    result.append(lower_solution + t * p ** (k - 1))
    return result

def hensel_lifting(f, p, k, base_solution):
    solution = base_solution
    for i in range(2, k + 1):
        solution = lift(f, p, i, solution)
    return solution

if __name__ == "__main__":
    P.<a> = PolynomialRing(Zmod(x), implementation='NTL')
    f = a^10 - z
    result_a = [int(i[0]) for i in f.monic().roots()]

    P.<b> = PolynomialRing(Zmod(y), implementation='NTL')
    f = b^10 - z
    result_b = [int(i[0]) for i in f.monic().roots()]

    y3 = y**3
    P.<c> = PolynomialRing(Zmod(y3), implementation='NTL')
    f = c^10 - z
    k = 3
    result_b3 = hensel_lifting(f,y,k,result_b)

    for i in result_a:
        for j in result_b3:
            flag = long_to_bytes(crt([int(i),int(j)],[x,y3]))
            if flag.startswith(b"flag"):
                print(flag[:32])
```
