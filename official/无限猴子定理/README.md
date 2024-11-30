# 无限猴子定理

- 题目分类：math

- 题目分值：250

无限猴子定理指出：一只猴子在打字机上仅靠随机按键，几乎必然能够在足够长的时间后打出莎士比亚的全套著作，自然也能打出本次比赛的所有 flag。

小郑曾经和小赵说过：宇宙的本质是计算。因此，小赵认为，辅助利用计算机生成的随机数，能够更容易地找到 flag 等有意义的信息，从而大大缩短验证无限猴子定理的时间。小赵找到了一串猴子打出的文本（`might_be_flag.txt`），并自行编写了生成随机数的程序（`find_flag.py`）。

一系列随机数将会通过程序源源不断地生成，而每个随机数都可能在文本中对应出一个正确的 flag。小赵到底能不能如愿以偿地拿到 flag 呢？

注：

- flag 一定代表一串有意义的英文单词序列，但本题完全不需要任何程度的基于机器的自然语言识别。
- 和本次比赛的其他 flag 类似，本题的对应 flag 中可能有英文字母被替换混淆。
- flag 代表的第一个英文单词既不会是名词，也不会是形容词。

[打开/下载题目](files/InfMonkey.zip)

---

本题是一道偏 Crypto 的题，主要考察的是参赛选手是否对随机数生成器的质量有一定的认识。

通过对 `find_flag.py` 的解读可以注意到，每次“flag”的选取都是在一个无限长的序列中选取一个长为 18 的窗口截取的结果，而这个窗口会不断向前滑动 17 个单位：

> `=>`**`EH650ARRBN6wFygy3E`**`ELPa1VXQdAYxlD1FxVd+7waO7T0B5pAs2n+TkwdI21/wzJ5YiIdw...`  
> `=>EH650ARRBN6wFygy3`**`EELPa1VXQdAYxlD1Fx`**`Vd+7waO7T0B5pAs2n+TkwdI21/wzJ5YiIdw...`  
> `=>EH650ARRBN6wFygy3EELPa1VXQdAYxlD1F`**`xVd+7waO7T0B5pAs2n`**`+TkwdI21/wzJ5YiIdw...`  
> `=>EH650ARRBN6wFygy3EELPa1VXQdAYxlD1FxVd+7waO7T0B5pAs2`**`n+TkwdI21/wzJ5YiId`**`w...`  

我们很快就会产生对于这个序列是如何生成的的兴趣。经过研究，我们可以注意到这一序列是一个基于线性同余法的随机数生成器生成相应的数，并一一映射到某个字符串的下标上形成的。

以下是这个随机数生成器的递推公式：

```plain
next(x) = (x * 30211 + 38923) % 65531
```

既然是线性同余法，我们自然会意识到这个随机数生成器是存在周期的，我们可以截获这个周期以内所有可能的“flag”。我们放任这个程序生成（记得把 `sleep` 那句去掉），直到输出出现周期。

> 00001: `(0x0000) => flag{EH650ARRBN6wFygy3E}`  
> 00002: `(0x316B) => flag{EELPa1VXQdAYxlD1Fx}`  
> 00003: `(0xB110) => flag{xVd+7waO7T0B5pAs2n}`  
> 00004: `(0x7762) => flag{n+TkwdI21/wzJ5YiId}`  
> ...  
> ...  
> ...  
> 65511: `(0xB025) => flag{nHaQ/zePfOoxuXRQNy}`  
> 65512: `(0x5C0B) => flag{yAaUnoXFpNWPp9j9/E}`  
> 65513: `(0x0000) => flag{EH650ARRBN6wFygy3E}`  
> 65514: `(0x316B) => flag{EELPa1VXQdAYxlD1Fx}`  
> ...  

我们会注意到周期 65512 小于随机数生成器理论上的最大周期 65531。此时我们应该能够立刻意识到：这不是一个好的随机数生成器（一个好的随机数生成器应能遍历最大周期内所有的值）。我们自然想搞清楚排在周期之外的 19 个随机数身上发生了什么。

## 解法一：获取剩余 19 个随机数对应的内容

程序见于源代码中 [`solve_flag.py`](src/solve_flag.py)，记得和源文件放在同一目录下运行。

以下是输出：

> `(0x0C2A) => flag{+8ad+LC+Generat0r+}`  
> `(0x19A3) => flag{at0r+A+8ad+LC+Gene}`  
> `(0x271C) => flag{+Generat0r+A+8ad+L}`  
> `(0x3495) => flag{8ad+LC+Generat0r+A}`  
> `(0x420E) => flag{t0r+A+8ad+LC+Gener}`  
> `(0x4F87) => flag{Generat0r+A+8ad+LC}`  
> `(0x5D00) => flag{ad+LC+Generat0r+A+}`  
> `(0x6A79) => flag{0r+A+8ad+LC+Genera}`  
> `(0x77F2) => flag{enerat0r+A+8ad+LC+}`  
> `(0x856B) => flag{d+LC+Generat0r+A+8}`  
> `(0x92E4) => flag{r+A+8ad+LC+Generat}`  
> `(0xA05D) => flag{nerat0r+A+8ad+LC+G}`  
> `(0xADD6) => flag{+LC+Generat0r+A+8a}`  
> `(0xBB4F) => flag{+A+8ad+LC+Generat0}`  
> `(0xC8C8) => flag{erat0r+A+8ad+LC+Ge}`  
> `(0xD641) => flag{LC+Generat0r+A+8ad}`  
> `(0xE3BA) => flag{A+8ad+LC+Generat0r}`  
> `(0xF133) => flag{rat0r+A+8ad+LC+Gen}`  
> `(0xFEAC) => flag{C+Generat0r+A+8ad+}`  

事实上这十九个输出看起来都只是一个序列的重排。通过规则“flag 代表的第一个英文单词既不会是名词，也不会是形容词”，我们很容易排出 `0xE3BA` 代表的便是正确 flag。

## 解法二：利用无限猴子定理获得 flag

找来一排猴子，他们会通过打字机的方式告诉你本题的正确 flag 是什么的。

## 注

* 本题可能是本届比赛中唯一一道违反了“出现形如 `flag{xxx}` 字样的一定是 flag”这一约定的题目。

* 若使用解法二，假设在本届比赛开始时便一直产生随机“flag”，并假设产生的速率为一秒 20 个，那么在比赛结束前产生正确 flag 的概率不会超过 0.000000000000000000000004%。
