# 不同寻常的 Python 考试

这是一道考察 Python 语言奇技淫巧（各种边界情况）的题，一共包括了 20 个小题，回答任意 10 小题可以拿到第一个 flag，任意 15 小题可以拿到第二个 flag，全部答对可以拿到第三个 flag。对于每个小题，用户的输入由 Python 的 `ast.literal_eval` 读入。根据[文档](https://docs.python.org/3/library/ast.html#ast.literal_eval)，这个函数类似 `eval`，但是只能读入 Python 的基本类型，包括字符串、数值、列表等等，它可以安全地读入 Python 的字面量而无需担心任意代码执行的问题。

服务器上跑的 Python 版本是 3.7，有些人可能因为本地运行的 Python 版本比服务器低从而导致了本地和远程的行为不一致。远程 Python 的版本可以通过测试一些版本之间的细微区别来确定。预期解法在近几个 Python 3 的版本中都可以跑通。

## 解答

```python
def challenge_1(self, answer):
    if answer == "Hello":
        return True
```

直接输入 `'Hello'` 即可过关。

```python
def challenge_2(self, answer):
    a, b, c, d = answer
    if a == b and a is b and c == d and c is not d:
        return True
```

Python 中 `==` 表示判断相等关系，而 `is` 判断是否为同一个对象。相等并且为同一个对象的例子可以是 `None`。一些整数和字符串也可能满足这个性质，但这与实现有关，Python 并不保证这一点。

相等但是不为同一个对象的例子，找一种可变的数据类型即可，例如列表。

一个例子：`1, 1, [1], [1]`。

```python
def challenge_3(self, answer):
    if answer in answer == answer:
        return True
```

这里 `in` 和 `==` 的优先级是什么呢？其实 Python 中比较运算这样连起来写等价于 `answer in answer and answer == answer`，正如 `1 < x < 2` 等价于 `1 < x and x < 2`。

随便一个字符串都可以过关。

```python
def challenge_4(self, answer):
    a1, b1 = answer
    a2, b2 = answer
    if a1 * 2 != a1 and b1 * 2 != b1:
        a1 *= 2
        b1 *= 2
        if a1 == a2 and b1 != b2:
            return True
```

这个小题需要我们找到两个对象，其中一个 `*= 2` 之后对象本身会改变（和自己的另一个引用相等），而另一个对象 `*= 2` 之后引用改变（和原来自己的引用不相等）。找一个 mutable 和一个 immutable 即可，例如 `[1], 1`。

```python
def challenge_5(self, answer):
    r = reversed([1, 2, 3])
    if list(r) == list(r) + answer:
        return True
```

看上去像是 `answer = []`，但实际上 `reversed([1, 2, 3])` 是一个 iterator，遍历一次之后就空了，所以答案是 `[3, 2, 1]`。

```python
def challenge_6(self, answer):
    a, b = answer
    if max(a, b) != max(b, a):
        return True
```

`max` 函数用对象之间的比较运算来取出最大值。我们可以找 `{0}, {1}` 这两个集合，Python 中集合的比较运算是判断（真）子集关系，所以 `{0} > {1}` 和 `{1} > {0}` 都是 `False`，两次 `max` 结果不同。

```python
def challenge_7(self, answer):
    a, b, c = answer
    for x in a, b, c:
        if isinstance(x, float) or isinstance(x, complex):
            return False
    if a * (b + c) != a * b + a * c:
        return True
```

不满足乘法分配律？Python 中的乘法不一定是对数值进行，字符串和列表也可以和整数做乘法，所以很容易找到 `2, 'a', 'b'` 这样的解，此时等号两边是 `abab` 和 `aabb`。

```python
def challenge_8(self, answer):
    a, b, c = answer
    for x in a, b, c:
        if isinstance(x, float) or isinstance(x, complex):
            return False
    if a * (b * c) != (a * b) * c:
        return True
```

不满足乘法结合律？也可以和上一题一样用字符串或者列表来构造。这里可以利用它们乘以负数时总是会得到空串的性质，例如一个解是 `[0], -1, -1`。

```python
def challenge_9(self, answer):
    a, b = answer
    for x in a, b:
        if isinstance(x, float) or isinstance(x, complex):
            return False
    if type(a ** b) != type(b ** a):
        return True
```

需要 `a ** b` 和 `b ** a` 的类型不同。这里想要考察，Python 中相同基本类型的运算结果类型，可能与具体的值相关。

`(-1) ** 2 = 1`，是 `int` 类型，而 `2 ** (-1) = 0.5`，是 `float` 类型。也可以用 `(-1) ** 0.5` 来得到 `complex` 复数类型。

```python
def challenge_10(self, answer):
    a, b = answer
    if a and a.count(b) > len(a):
        return True
```

`a` 非空，并且 `a` 里面对 `b` 进行无覆盖的计数结果大于 `a` 的长度，这看起来不可能，其实 `b` 是空串的时候就可以。一个可能的解是 `'a', ''`。

```python
def challenge_11(self, answer):
    if max(answer) != max(*answer):
        return True
```

Python 中的函数可以以 `max(1, 2, 3)` 的形式调用，也可以以 `max([1, 2, 3])` 的形式调用。当参数个数为 1 时，就会匹配后一种形式。所以我们只需要让 `answer` 列表里面只有一个元素，这样 `max(*answer)` 就也会匹配到第二种形式，从而可以做到两个 `max` 的结果不相同。一个可能的解是 `[[0]]`。

```python
def challenge_12(self, answer):
    a, b = answer
    if a < b and all(x > y for x, y in zip(a, b)):
        return True
```

`a` 比 `b` 小，但是 `a` 中的每个元素都比 `b` 中对应位置的元素大？看起来不大可能，其实 `a` 是空列表并且 `b` 非空的时候就可以做到，因为 `a` 中根本没有元素，对空集计算 `all` 会得到 `True`。

```python
def challenge_13(self, answer):
    a, b = answer
    if b and not (a ^ b) - a:
        return True
```

看似 `a` 和 `b` 是两个整数，但如果这样的话，我们可以推出 `a ^ b == a`，从而 `b == 0`，矛盾，这是不可能的。除了整数以外，集合也支持 `^` 和 `-` 运算，很容易找到满足题目中关系的集合，例如 `{1}, {1}`。

```python
def challenge_14(self, answer):
    backup = deepcopy(answer)
    try:
        answer[0] += answer[1]
    except:
        if backup != answer:
            return True
```

这里 `answer[0] += answer[1]` 一行执行时需要产生异常，但是却需要 `answer` 的值发生变化。这是 Python 官方文档 FAQ 中[指出](https://docs.python.org/3/faq/programming.html#why-does-a-tuple-i-item-raise-an-exception-when-the-addition-works)的一种特殊情况，让 `answer` 是 tuple 并且 `answer[0]` 是 list 就可能触发这种情况，原因是 list 的 `+=` 运算可以正常进行，但是接下来在 tuple 中更新引用时会失败，tuple 是 immutable 类型。答案可以是 `[1], [1]`。

```python
def challenge_15(self, answer):
    item, l = answer
    if item in l and not min(l) <= item <= max(l):
        return True
```

看起来似乎需要找一个列表和一个列表中的元素，元素不在列表的最大和最小值之间。但其实 `item` 和 `l` 都可以是字符串，此时 `item` 可以是一个长度大于等于 2 的字符串，而 `min(l)` 和 `max(l)` 都是按单个字符计算的。一个可能的答案是 `'aa', 'aaa'`。

```python
def challenge_16(self, answer):
    item, l = answer
    if item == 233 and item in l and l in l:
        return True
```

看似不可能。我们可以从 `l in l` 开始思考，Python 中什么字面量可以 `in` 它自己呢？可以是字符串或者 `bytes`。对 `bytes` 进行遍历时，元素是 0~255 范围的 `int`，所以 `233, b'\xe9'` 可以满足条件。

```python
def challenge_17(self, answer):
    item, l = answer
    if l[0] == item and item not in l:
        return True
```

对 `l` 取下标 `0` 得到的元素并不 `in l`，这可能吗？可以想想 Python 的各种基本类型，其中 `dict` 就可以满足我们的要求，因为对 `dict` 类型取下标拿到的是 value，而判断对象是否 `in` 一个 dict 时，是根据 key 的集合判断的。一个可能的答案是 `1, {0:1}`。

```python
def challenge_18(self, answer):
    a, b = answer
    if (a - b) != -(b - a):
        return True
```

这个小题有点 tricky，看起来使用各种 `list`、`dict`、`set` 之类的东西搞不定了。我们可以拿出杀手锏，浮点数中的特殊值，[`inf` 和 `nan`](https://stackoverflow.com/questions/17628613/what-is-inf-and-nan)。这种浮点数并不能直接输入，但经过简单尝试可以发现，输入很大的数，例如 `1e999`，就可以得到 `inf`，而 `inf - inf` 可以得到 `nan`，`nan` 有一个性质就是 `nan == nan` 并不成立，所以这道题的答案可以是 `1e999, 1e999`。

```python
def challenge_19(self, answer):
    if answer.isdecimal():
        if len(answer) < 5:
            if sum(ord(c) - ord("0") for c in answer) == 23333:
                return True
```

长度小于 5 的字符串，每个字符都是 `decimal`，并且取 Unicode 码之后加起来需要等于 23333。我们可以发现，满足 `isdecimal()` 条件的字符，不只有 0~9 这 10 个数字，还有很多各种各样的 Unicode 字符。我们可以简单写一个程序输出它们：

```python
for i in range(0x110000):
    if chr(i).isdecimal():
        print(i)
```

在输出的这些 Unicode 码中，找到 5 个加起来是 23333 并不难，可以在适当的范围内手工尝试，也可以写程序搜索解决。例如一个可行的解是 `'᱙᱙᱃۰'`。

```python
def challenge_20(self, answer):
    if len(set(str(x) for x in answer)) == 7 and all(x == 0 for x in answer):
        return True
```

我们需要找到 7 个对象，它们转化为字符串之后各不相同，但是每个对象却都和 0 相等。比较好想到的例子是 `0`、`0.0`、`False` 和 `0j`，它们分别是 `int`、`float`、`bool`、`complex` 四种 Python 数值类型的对象。可 Python 只有这四种数值类型，另外三个去哪里找呢？

我们可以发现，浮点数标准中，是存在 `0.0` 和 `-0.0` 两个表示 0 的值的，它们相等。Python 中，`str(-0.0)` 可以得到 `'-0.0'` 这个字符串。我们可以类似构造出复数类型下面的各种包含浮点 `0.0` 和 `-0.0` 的组合。最终的 7 个对象是：`0, 0.0, -0.0, False, -0.0-0.0j, -0.0j, 0j`。

其实我作为出题人不知道是否有第 8 种满足条件的对象，我自己尽力找只能找到这 7 种。我非常期待有人可以构造出第 8 种甚至更多，如果你找到了，一定记得告诉我😑

## 其他

对于所有小题，如果你有其他更巧妙的解法，欢迎补充。

关于 Python 冷知识的一些参考资料：

<https://github.com/satwikkansal/wtfpython>

<https://github.com/cosmologicon/pywat>
