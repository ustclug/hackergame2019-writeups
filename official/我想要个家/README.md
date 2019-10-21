# 我想要个家

> 注意：该题提示了做本题可能有一定的危险性。一切导致了系统崩溃、从删库到跑路的事件的发生均系做题人在知晓其行为后果的前提下导致的，出题人和主办团队概不负责！

## 萌新·解法

构造 rootfs 这样的文件夹。将程序 `ih-linux`（二进制程序）放置到 rootfs 文件夹中，而后运行 

```bash
sudo chroot rootfs ih-linux
```

即可。下面讲解构造 rootfs 的步骤。

### 构造 rootfs

* Step1: 根据提示新建 Bedroom, Kitchen 和 Lavatory, Living_Room 四个文件夹.
* Step2: 文章要求删除 `/etc` `/bin` `/usr` 等文件夹，这些文件夹对于 Linux 的运行具有重要意义，因此只能构造一个不完整的根文件系统，而后切换到这个新的 rootfs 中，才能完成本题。
* Step3: 新建一个 Microphone 的文本文件，然后建立一个指向 Microphone 的名为 Headset 的软连接。
* Step4: 新建 Living_Room/run.sh 然后在外部运行这个脚本。这个脚本的作用是不断将时间写入 Living_Room/Clock 文件中
* Step5: 将 `/bin/sh` 和 `/bin/sleep` 两个程序复制到 rootfs 中。使用 `ldd` 命令来查看他们的依赖。出题者在 alpine 中构建的 rootfs 因此依赖较少，有 `/dev/null`, `/lib/ld-musl-x86_64.so.1` 和 `/lib/libc.musl-x86_64.so.1`。将这些依赖设备和动态链接库复制到指定位置。
* Step6: 当程序运行到此处时候，输入 `sleep 10`

## 逆向大手子·解法

本题使用 golang 程序语言编写，去掉了调试信息和符号表。同时，flag 使用 AES 加密硬编码在程序中。逆向大手子可以使用二进制逆向分析的技术来获取 flag 。

## 变态·解法

直接在真实机器或虚拟机中构建 rootfs。

## 附言 (From iBug)

其实上面那个构造 rootfs 的办法第 5 和 6 步用不着那么复杂，知道程序运行原理的同学可以自己动手编写一个最简单的 C 程序：

```c
#include <unistd.h>

int main() {
  sleep(10);
  return 0;
}
```

编译成 `sleep` 并放进 rootfs 里，注意需要静态链接：

```shell
gcc sleep.c -o rootfs/sleep -static
```

这时候程序运行到要睡觉的那一步时直接输入 `/sleep`，你自己编写的<s>吃饭睡觉打豆豆</s>程序就会运行并等待 10 秒了，这样就绕过研究 shell 和程序依赖的那两步了。

P.S. 第 4 步可以用一种神奇的办法，不需要额外运行一个不断写入时间的程序。大致做法就是先写入当前时间并立即运行题目程序（一行 shell 命令可以运行多条子命令，只需要用分号将各条子命令隔开就行），然后观察输出，发现两个时间相差 8 秒。修改命令行的前半部分，改为将当前时间 +8s 写入文件并运行程序即可<s>蒙混过关</s>。

对于典型的 Linux 系统（使用 GNU Core Utilities），应该是如下操作：

```shell
date '+%Y-%m-%d %H:%M:%S' > rootfs/Living_Room/Clock; chroot rootfs /IWantAHome-linux
# 哎哟，慢了 8 秒钟
date -d '+8 seconds' '+%Y-%m-%d %H:%M:%S' > rootfs/Living_Room/Clock; chroot rootfs /IWantAHome-linux
```
