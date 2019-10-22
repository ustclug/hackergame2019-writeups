# 宇宙终极问题

## 42
[Google](https://lmgtfy.com/?q=42+sum+of+three+cubes&s=g) 一下就好了~

## Everything
还是 Google 一下就[找到了](https://www.alpertron.com.ar/FCUBES.HTM).

## Last Question
> An integer greater than one can be written as a sum of two squares if and only if its prime decomposition contains no prime congruent to 3 modulo 4 raised to an odd power.

根据 [Brahmagupta–Fibonacci identity](https://en.wikipedia.org/wiki/Brahmagupta%E2%80%93Fibonacci_identity), 先试图分解给定整数, 直到满足条件.

再利用 [Gaussian GCD](https://math.stackexchange.com/questions/5877/efficiently-finding-two-squares-which-sum-to-a-prime) 计算每个质数的分解.
