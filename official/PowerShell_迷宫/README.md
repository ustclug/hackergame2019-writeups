# PowerShell 迷宫

花絮：本题最早源自 zzh 的一系列发言（“出个微软技术的题吧”、“用 PowerShell 搞个迷宫”），作为和 USTC LUG 还有关联的最大软粉的我就站了出来背锅。思考了一下怎么做个迷宫之后，决定用 PowerShell 的 `Provider` 机制进行实现。赶鸭子上架之下最终就是那样子一副勉强能玩的状态啦。

本题 Provider 源码位于 [Blealtan/PSMaze](https://github.com/Blealtan/PSMaze)。感兴趣的同学可以围观一下。

## PowerShell 简介和一些私货

PowerShell Core 是基于 .NET Core 实现的一个跨平台 shell，其语言设计继承自 Windows PowerShell，毫无疑问地 POSIX 不兼容。
其设计比起一个 shell，更像是一个可以用常规 shell 语法执行可执行文件的脚本语言 REPL：动态类型的 `PSObject` 加上 .NET 的静态类型系统（称作 `CTS`，Common Type System）组成的 gradual typing system，作为基础支持兼高级功能的 .NET Core 完整 API，相当完备的命令（像 `Invoke-WebRequest` 的存在直接消除了 `curl` 的生存意义）……
这使得在不需要 `numpy` 等 Python 的便利的库时，出题人通常会打开 PowerShell 解决自己的 scripting 需求。

许多人批评 PowerShell 的命令和参数繁杂，但在出题人看来，基于 Verb 前缀的表示有助于快速查找想要的命令，而常用命令也都有着其短小精悍的 alias，同时参数名的 `-Xxx` 也可以取其最短无歧义前缀使用（例如 `ls -r === Get-ChildItem -Recurse`），这已经足够便利。

美中不足之处（也是出题人本人在 Linux 上最终弃用 PowerShell 作为日常 shell、退为 Python 替代品的原因）在于，由于非 Windows 平台上基于 xterm 的交互方式某种程度上弱于 Win32 API 中对控制台的操作接口、看起来微软也懒得优化用户体验，在 Linux、macOS 上的实际交互体验远差于 Windows，但比本次比赛中提供的 Web 界面还是要正常不少。

## 本题解法之预期解

这里出题人按照最老实而严谨的思路解本题，并假设阅读人仅仅具备基本的数据结构知识。

根据文案，本题的预期解是在终端中执行一些命令，完成 `Maze:/` 的搜索，找到有 Flag 的格子。
由于题目没有说明迷宫大小、是否有限、是否唯一路径，这里应当采用图的宽度优先搜索算法（Breadth First Search，BFS，参见 <https://en.wikipedia.org/wiki/Breadth-first_search>）进行迷宫的搜索。

为了实现 BFS，我们首先需要一个队列。
文案中给出了使用 `Dictionary[string, Tuple[int, int]]` 的样例。
结合 [.NET Core 2.2 API](https://docs.microsoft.com/en-us/dotnet/api/?view=netcore-2.2)，不难联想到使用 `Queue[string]`，其中每个元素为访问的路径（也是从出发点走到那个位置的路径）。
此外，还需要一个 visited set 保存经过的格子；观察 `Get-ChildItem / ls / gci` 的结果可知格子的唯一标识为 `(X, Y)`，二者均为 `int` 类型。
因此，类似地，使用 `HashSet[Tuple[int, int]]` 存储 visited set 即可。

一个简单的实现代码如下：

```powershell
using namespace System.Collections.Generic
# 初始化数据结构
$queue = [Queue[string]]::new()
$queue.Enqueue("Maze:/")
$visited = [HashSet[Tuple[int, int]]]::new()
# 开始搜索循环
while ($queue.Count -ne 0) {
    $path = $queue.Dequeue()
    $gi = Get-Item $path
    $xy = [Tuple[int, int]]::new($gi.X, $gi.Y)
    if ($visited.Contains($xy)) { continue }
	$visited.Add($xy) | Out-Null
    if ($gi.Flag -ne $null) {
        Write-Output $path
        Write-Output $gi.Flag
		break
    }
    Get-ChildItem $path | Foreach-Object { $queue.Enqueue("$path/$($_.Direction)") } | Out-Null
}
```

题外话：有心人可能会发现搜索的进度会随着深度加深越来越慢。这是由于题目内部实现中，验证一个路径合法性需要在迷宫上依次遍历；出题人没有在这方面做优化，最后巧合地刚好卡到了一个暴力递归无法在一个会话限时内完成搜索的性能，可喜可贺（拖走暴揍）。

## 本题解法之各种非预期解

### 通过 WebSocket 交互搜索

花絮：在出题时本题就被 zzh 指出了此种解法。出题人当时想到了一种绝妙的办法解决这一问题，可惜 <del>代码里写不下</del> 离比赛只剩几天，时间来不及了。最终这个路子就只通过没有提供 `nc` 界面来稍微避免了一下，但看起来还是有一些选手如此完成了题目。

具体细节不多赘述，大致上来说，由于前端网页是通过 WebSocket 和后端交互，只需要通过 WebSocket 连接，并反复使用 `ls`、`cd` 命令结合搜索迷宫即可。主要的工作量应当是在 parse PowerShell 的输出上。

### 通过逆向 `/opt/PSMaze.dll` 解题

花絮：一位验题人提出并实操了此种做法的后半段，但同时也承认了这种做法的高度复杂性和毫无意义；出题人本人并没有完整验证这种方法。

有心人（真的有吗）可能会发现 `/opt/PSMaze.dll` 是提供本题中迷宫实现的 .NET 库文件。
`strings` 之并不会提供任何线索；这是由于两方面原因：其一，.NET 中的字符串都是 UTF-16 格式；其二，flag 并未以任何加密形式存储于其中。

通过 `[Convert]::ToBase64String` 将其编码为 base64 传回本地后，通过 ILSpy 分析类 `PSMaze.MazeProvider`，会发现这是一个未经混淆和加壳的 .NET dll，从中可以得到如下信息：

1. 迷宫大小为 64*64，单连通（路径唯一），随机生成但种子固定为 `0x1551`，Flag 固定位于迷宫右下角；
2. Flag 由固定前缀及一个根据路径计算得出的 `Int32` 值的十六进制表示组合而成。

本地重复迷宫生成算法并使用同样的 .NET Core 2.2 的 `System.Random`，在生成的迷宫上搜索找到左上角到右下角的路径后，即可计算出 flag。
