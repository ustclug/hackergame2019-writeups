# 宇宙终极问题

- 题目分类：math

- 题目分值：42（100）+ Everything（150）+ Last question（200）

> 天何所杳, 十二焉分?
>
> 日月安属, 列星安陈?

浩瀚宇宙的一个寻常星系里, 弥漫六合的暗物质晕中, 远古的诗歌在狄拉克海上无声回荡.

史诗般的超级计算机 **Deep Thought** , 寒冷星空下的百万亿场效应管, 人类终得以一窥这个宇宙最深层的奥秘.

没错, 就是 42, 对于生命, 对于宇宙, 对于世间万物的答案.

你可以通过 `nc 202.38.93.241 10017` 命令来连接题目，或者使用我们提供的[网页终端](http://202.38.93.241:10018/?token={token})。

如果你不知道 `nc` 是什么，或者在使用上面的命令时遇到了困难，可以参考我们编写的 [萌新入门手册：如何使用 nc/ncat？](https://planet.ustclug.org/post/268)

---

## 42
[Google](https://lmgtfy.com/?q=42+sum+of+three+cubes&s=g) 一下就好了~

## Everything
还是 Google 一下就[找到了](https://www.alpertron.com.ar/FCUBES.HTM).

## Last Question
> An integer greater than one can be written as a sum of two squares if and only if its prime decomposition contains no prime congruent to 3 modulo 4 raised to an odd power.

根据 [Brahmagupta–Fibonacci identity](https://en.wikipedia.org/wiki/Brahmagupta%E2%80%93Fibonacci_identity), 先试图分解给定整数, 直到满足条件.

再利用 [Gaussian GCD](https://math.stackexchange.com/questions/5877/efficiently-finding-two-squares-which-sum-to-a-prime) 计算每个质数的分解.
