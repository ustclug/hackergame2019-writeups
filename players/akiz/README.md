# Akiz

## PowerShell 迷宫

官方题解实在是太慢啦！竟然要将近4分钟才能得到结果什么的（

下面这个方法只要数十秒就可以找到啦w

```
function recursive($path, $max)
{
    foreach ($item in @(Get-ChildItem $path))
    {
        $x = $item.X
    	$y = $item.Y
        $flag = $item.Flag
        if ($flag -ne $null) { 
            Write-Host ""
            Write-Host "$flag"
            $end = Get-Date
            Write-Host ('Total Runtime: ' + ($end - $start).TotalSeconds)
            exit 
        }
    	if ($x -eq $max) { return }
    	if ($y -eq $max) { return }
    	if ($array[$x, $y] -ne 1) { 
            $array[$x, $y] = 1 
            Write-Host -NoNewline "."
        	recursive $item.PSPath $max 
        }
    }
}

$start = Get-Date
$array=New-Object 'int[,]' 70, 70
recursive (Resolve-Path Down).ProviderPath 70

```

![1.png](https://i.loli.net/2019/10/22/ukIf1BipO7e8voH.png)

![2.png](https://i.loli.net/2019/10/22/tZ4kDIvhYMmK8sS.png)
