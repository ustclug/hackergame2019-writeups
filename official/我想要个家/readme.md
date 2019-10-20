# 我想要个家

> 注意：该题提示了做本题可能有一定的危险性。一切导致了系统崩溃、从删库到跑路的事件的发生均系做题人在知晓其行为后果的前提下导致的，出题人和主办团队概不负责！

## 萌新·解法

构造 rootfs 这样的文件夹。将程序 ih-linux(二进制程序) 放置到  rootfs 文件夹中，而后运行 

```bash
sudo chroot rootfs ih-linux
```

即可。下面讲解构造 rootfs 的步骤

### 构造 rootfs

* Step1: 根据提示新建 Bedroom, Kitchen 和 Lavatory, Living_Room 四个文件夹.
* Step2: 文章要求删除 /etc /bin /usr 等文件夹，这些文件夹对于 linux 的运行具有重要意义，因此只能构造一个不完整的根文件系统，而后切换到这个新的 rootfs 中，才能完成本题。
* Step3: 新建一个 Microphone 的文本文件，然后建立一个指向 Microphone 的名为 Headset 的软连接。
* Step4: 新建 Living_Room/run.sh 然后在外部运行这个脚本。这个脚本的作用是不断将时间写入 Living_Room/Clock 文件中
* Step5: 将 /bin/sh 和 /bin/sleep 两个程序复制到 rootfs 中。使用 ldd  命令来查看他们的依赖。出题者在 alpine 中构建的rootfs 因此依赖较少，有 /dev/null, /lib/ld-musl-x86_64.so.1 和 /lib/libc.musl-x86_64.so.1 将这些依赖设备和动态链接库复制到指定位置。
* Step6: 当程序运行到此处时候，输入 sleep 10

## 逆向大手子·解法

本题使用 golang 程序编写，去掉了调试信息和符号表。同时，flag使用 aes 加密硬编码在程序中。逆向大手子可以使用二进制逆向分析的技术来获取 flag 。

## 变态·解法

直接在真实机器或虚拟机中构建 rootfs。

