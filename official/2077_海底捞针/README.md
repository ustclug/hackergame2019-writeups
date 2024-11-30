# 2077 海底捞针

- 题目分类：math

- 题目分值：300

提示：情节内容仅为有趣，可能和解法无关。

```
:: XGUID = MINDSNAPSHOT##4AZ6F0KQ2TV3ST4#000EARTH0CHINA0SU00220456-D0A3-RLWE-AES*-SHA3-0020770630235960335760219
::
:: CHARSET = UTF-8-Extension
::
:: ELEMENT#3092   旧式阅读增强时间戳 2077 年 6 月 30 日 23 时 59 分 60 秒 335 毫秒 760 微秒 219 纳秒
:: ELEMENT#3093   旧式额外时间备注 常年, 闰秒, 计时器允差 (5 sigma) 12纳秒, UTC 同步允差 (5 sigma) 60纳秒
:: ELEMENT#1344   旧式内容分类标准字符串 “思维快照”
:: ELEMENT#6641   旧式人员 ID 4AZ6F0KQ2TV3ST4
:: ELEMENT#6642   (外键来源) 旧式人员名称字符串 "Kestify"
:: ELEMENT#9269   (外键来源) 旧式人员职位标准字符串 “协作员-O 级人员”
:: ELEMENT#14236  旧式安全协议 非对称密钥 Ring-LWE-65536 对称密钥 AES-1024 哈希 SHA3-1024
:: ELEMENT#14239  旧式安全协议备注 抗量子计算=yes, 公钥体系=lattice

```

注：以下内容已经从乔姆斯基波兰式语法树翻译为旧版自然语序，并压缩了冗余标记，以供未改造人阅读，但不保证完全的歧义消除。

这次拉索集团一如既往没有留下任何直接证据。“黑色儿童节████████████[数据删除]” 事件之后，代号为 “拉索” 的组织因编号为 573892523532 的攻击一举成名。

拉索集团属于人工智能技术激进反对分子，对地球政治协作共同体的编号为 7267879432687 的提案非常不满。该提案要求加速人工智能技术的社会应用。我个人对这个提案的评价是█████████████████████████████████████████████[数据删除]

不过这次我们获得了一些可能相关的数据。我们发现了 CIDAR10 数据集，其中包含 50000 张 32 \* 32 的 24 位色彩深度图片。CIDAR10 是目前学龄前人类的玩具数据集之一，24 位色彩是为了适应旧人类 3 色感知的一种颜色编码。以及如下几个代码片段：

片段1：

```
import numpy as np
import torchvision
from PIL import Image

trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True)
images = trainset.data # 50000, 32, 32, 3
choices = ████████████████████████████████████[目标数据]
assert 30 < len(choices) < 5000
targets = images[choices]
averaged = np.mean(targets, axis=0).astype(np.uint8)
Image.fromarray(averaged).save("averaged.png")

```

片段2：

```
secret = choices

import hashlib
digest = hashlib.sha384('.'.join(str(n) for n in np.sort(secret)).encode()).hexdigest()
print('flag{' + digest + '}')

```

从代码中可以推理出，choices 是获取 flag 的关键。拉索集团使用 choices 从 CIFAR10 数据集中任意取了 31～4999 张图片并加权平均，舍弃像素的小数位后保存为 averaged.png。averaged.png 是曾经的称为 “文件名” 的文件标识，而其中 png 是非常古老的“扩展名”的概念，代表着一种弃用的低效无损图片压缩格式。令人震惊的是，他们居然没有添加 Python 类型注释，以至于我们使用了 2019 年的 Python3 解释器才能成功运行这个程序。这个程序也没有使用任何并行技术，即使在数据下载完成后执行时间依然长达 100000 微秒，我为 Python 语言如此久之后才被淘汰深感遗憾。这段程序唯一的亮点是使用了 SHA3，如果 TA 们使用了 SHA1 那么我们应该很快就能搞定。无论如何，这个老古董程序几乎就是来源于拉索集团（在 KB2342905202 推理框架下置信度为 0.993），因为 TA 们就是一群顽固不化的人。（注：本段使用了情感修饰，可能异于原先内容）

我和同级别人员讨论了是否可以从 averaged.png 中反向得出内容，目前结论是暴力枚举 choices 的成功概率低于
1 / 3480654770799877797889721073843915681584916072058351754594847201198802549202414602327028114551252904508540000，这是不可接受的。按照行政流程 395827792042，我们向决议机器 1036ZD132WV3S5D 发送了公开征集请求，目前 1036ZD132WV3S5D 已经作出了肯定批复 (REGRET 值为 0.03)，决议号为 1036ZD132WV3S5D:7293992432，1036ZD132WV3S5D 同时已经调度社会公开公关机器资源组 455FGS990 对 1036ZD132WV3S5D:7293992432 进行后续的公开征集请求跟踪。对于非改造人，可以使用 “海底捞针” 索引 1036ZD132WV3S5D:7293992432。

1036ZD132WV3S5D:7293992432 的摘要如下：

对于所有 D 级以上的数理基础良好人员，如解决 1036ZD132WV3S5D:7293992432, 则按照行政流程 212707199541 进行奖励。预计难度：3。

```
:: AUDIT = 1036ZD132WV3S5D:29837423948324792809735
:: ELEMENT#17394 (外键来源) 旧式审核内容摘要
                    R0 我可以证实此文章片段的最初版本是直接从 
4AZ6F0KQ2TV3ST4 的思维中读取的。
                    R1 已经删去了 4AZ6F0KQ2TV3ST4 的个人政治评价。地球政治协作共同体禁止任何形式的公开政治评论。
                    R2 根据绝对性别中立原则，文章中在证据不足时不应包含任何性别偏见，已经将‘他们’ 替换为 ‘TA 们’。

:: FINGERPRINT = AAAAB3NzaC1yc2EAAAABIwAAAQEA3RhdMH4nPhHX5Pg2eW+PT5
::::

```

**补充说明：新的情报同步已经完成，根据旧式 UNIX 文件系统访问时间戳，一名 D 级左右数理基础良好人员已经几乎肯定，出现在该文章中的代码片段 1 的 choices 取的图片其实不超过 100 张（在 KB2342905202 推理框架下置信度为 0.998）。**

**提示：拉索集团注册商标为 Lasso**

[打开/下载题目](src/averaged.png)

---

本题是一个标准的数学题，不同于对代码的逆向，这题是对数据的逆向。

下面我们对题目内容进行形式化。首先注意到一个重要性质：加权平均是作用在每个图片中相同位置的像素上的（更准确地说是每个像素的颜色分量），不同位置的像素互不相干。由此一个简单的思路是不考虑这些像素之间的空间关系，直接把整个图片作为一个 3072 维的向量进行处理。由此我们可以得到以下若干等式：

```
y_0 = floor(k_0 * x_0_0 + k_1 * x_1_0 + .. + k_50000 * x_50000_0)
y_1 = floor(k_0 * x_0_1 + k_1 * x_1_1 + .. + k_50000 * x_50000_1)
...
y_3071 = floor(k_0 * x_0_3071 + k_1 * x_1_3071 + .. + k_50000 * x_50000_3071)
```

其中 `y` 是 `averaged.png` 对应的向量, `y_i` 是 `y` 中的第 i 个 分量； `x_i_j` 是 CIFAR10 数据集中第 i 个 图片对应的向量的第 j 个分量。`k_i` 属于集合 `{0, 1 / N}`，其中 `N` 是用于平均的总图片数目； `floor` 是向下取整函数。这个等价于以下的代数方程：

```
y = floor(k X)
```

注意到，由于 `floor` 的存在，这个并不是传统意义上的线性代数，而是一种整数方程。一种方法是将 floor 改编为不等式，即 `y = floor(x) <=> y <= x < y+1`，然后转化为 0/1 整系数规划问题。不过这种问题仍然有几个，首先是 0/1 整系数规划问题本身很难解；第二是 `N` 是未知的，这个可以通过暴力遍历解决，但是这会进一步使得问题解决变慢。这里我们使用另外一种思路（注：0/1 整系数规划问题是一个可行的思路，但是由于它的难度不是本题的预期解；也有可能参赛选手有更加高级的数学知识而使用其它方法）。

新的思路是将 `floor` 对数据的影响作为噪声，这个噪声可以近似认为是均匀分布，而且很关键的一点是有界的，这样方程可以改写为

```
y = k X + \epsilon, |epsilon_i| <= 1
```

这个方程咋一看非常类似于一个线性代数方程，但是存在几个问题：

1. `k` 的取值是离散的，所以本质上还是整数方程。
2. （作为线性代数方程而言）方程是欠定的，我们需要求解的系数 `k` 有 50000 个，但是方程只有 3072 个。
3. N 未知。
4. 存在噪声。

噪声不是非常大时，直接用线性回归等方法就可以求出 `k`。但是由于前面两个问题，参赛选手使用线性回归会得到无数可能的解。这个时候最关键的是注意到题目中间接给了一个可以利用的属性：N << 50000。一开始的题目中 N 不超过 5000，后来为了充分暗示这一点改成了不超过 100。这个属性就是著名的稀疏性假设。在噪声不过大的时候，稀疏性刚好可以完全应对上面几个问题。

稀疏性原则上要求求解以下最优化问题：

```
\argmin_k \sum_i(\sum_j k_j * x_j_i - y_i)^2 + \alpha * norm_0(k)
```

其中 \alpha 是一个系数，越大代表越稀疏。norm_0 是 0-范数，在这里表示非 0 的元素数量。但是优化 norm_0 是个 NP-hard 问题，所以一般采用 norm_1， 即 1-范数：

```
\argmin_k \sum_i(\sum_j k_j * x_j_i - y_i)^2 + \alpha * \sum | k |
```

Terry Tao 等人证明了很多情况下 1-norm 可以完美代替 0-norm，或者可以取得很好的近似效果，因此上面的优化形式经常被用于稀疏感知等领域(https://scikit-learn.org/stable/auto_examples/applications/plot_tomography_l1_reconstruction.html#sphx-glr-auto-examples-applications-plot-tomography-l1-reconstruction-py)。
这个方法还有一个非常著名的名字：Lasso。题目中的 “拉索集团” 其实也是暗示这个词。所以我们可以直接用 Lasso 来解决这个问题。方法包括但不限于调包等。Lasso 方法会返回一个 k，其中大部分内容为 0 或者非常小。

最后一个问题是，如何确定 N 和 \alpha 呢？这不是一个很容易解释清楚的问题，不过本题没有故意为难选手，在默认 \alpha = 1 时就可以明确看到效果：选手只要使用一种方法 （两项之间的差分，比值，或者甚至是绝对大小，或者某部分数据占总大小的比例），就可以发现被用于平均的图片和未被用于平均的图片的系数 k 有着很大差异。\alpha 在一定范围内都是有效的（尤其是增大的情况），如果较小可能会出现比预期更多的图片，但是大部分数量都较多，可以在几次尝试提交flag后被排除。

源代码位于 src/ 目录下，其中 generator.py 包括了图片生成和测试。

参考解决方案（带注释）：

```python
import numpy as np
from PIL import Image
import torchvision
# 这里默认使用了最流行的 scikit-learn 库。不排除自己解决或者使用其它库。
# 不过这种涉及数值计算类的问题除非自己很有经验或者非常简单，否则并不鼓励自己造轮子。
from sklearn import linear_model

trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True)
images = trainset.data # 50000, 32, 32, 3

# 把图片转成向量形式，以方便求出 y = kX 中的系数 k。
# 其中 y 是 averaged.png, X 是整个数据集中的图片构成的矩阵。
averaged = np.array(Image.open("averaged.png"))
averaged = averaged.reshape(-1).astype(np.float)
# 为了方便，我们令 y 和 k 都是行向量，所以这边 reshape 后矩阵要转置一下。
images = images.reshape(len(images), -1).T

# Lasso regression
# 拟合目标, 这里的 trick 是强制系数是正的，但是不使用也不会过多影响结果。
# alpha 值是 Lasso 回归中的 L1 惩罚系数，在一定范围内都是有效的，这里采用了默认值。
clf = linear_model.Lasso(alpha=1, positive=True)
clf.fit(images, averaged)

# 拟合后，clf.coef_ 对应了方程中各个图片的系数 k。

# cliff search
# 此处逆序排序后检测系数下降较快的边缘，以推知具体是由几个图片平均得到的 （也就是 i）。
# 这里有若干种方法可以实现，而且这样的候选位置可能不止一个，
sorted_coef = np.sort(clf.coef_)[::-1]
prev = sorted_coef[0]
for i, coef in enumerate(sorted_coef):
    if prev / coef > 10:
        break
    prev = coef

# 系数中前 i 大的数对应的系数中的位置构成的 list 就是我们的答案。
secret = np.sort(np.argsort(clf.coef_)[::-1][:i])
print(secret)

import hashlib
digest = hashlib.sha384('.'.join(str(n) for n in np.sort(secret)).encode()).hexdigest()
print('flag{' + digest + '}')
```
