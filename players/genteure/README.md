# PowerShell 迷宫

（注：本 writeup 是在手机上使用 GitHub 网页编辑的，排版不太美观还请谅解）

个人认为这道题是一个很简单的题，在问题中给出了足够甚至偏多的提示（，有效地（？）实现了安利 pscore 的目的）。如果这道题换成写 py 或者 js 的话，感觉会成为成功解答人数最多的题（之一）

本题的官方预期解是使用图的广度搜索算法对迷宫进行搜索，并且：

> 题外话：有心人可能会发现搜索的进度会随着深度加深越来越慢。这是由于题目内部实现中，验证一个路径合法性需要在迷宫上依次遍历；出题人没有在这方面做优化，最后巧合地刚好卡到了一个暴力递归无法在一个会话限时内完成搜索的性能，可喜可贺（拖走暴揍）。

这里算是非预期解法3：

不 cd 进目录，在根目录使用绝对路径进行访问。这种方法对比 cd 再 ls 会节省至少 50% 的时间。因为减少了 Provider 内部实现的调用次数，显著提高了查询搜索的效率，即使是深度优先搜索也可以在时间限制内查找到目标 flag。本人在 CTF 期间写的代码（的清理后版本）如下：

```powershell
using namespace System

$list = [System.Collections.Generic.List[Tuple[int, int]]]::new()

function Run ($Cell, $Path) {
    $list.Add([Tuple[int, int]]::new($Cell.X, $Cell.Y))
    if ($null -eq $Cell.Flag) {
        $Path += "/" + $Cell.Direction
        foreach ($item in (Get-ChildItem $Path)) {
            if (-not $list.Contains([Tuple[int, int]]::new($item.X, $item.Y))) {
                $result = Run $item $Path
                if ($null -ne $result) {
                    return $result
                }
            }
        }
        return $null
    }
    else {
        return $Cell.Flag
    }
}

Run (Get-ChildItem)[0] "Maze:"
```
