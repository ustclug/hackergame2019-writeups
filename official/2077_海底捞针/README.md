# 2077 海底捞针

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
