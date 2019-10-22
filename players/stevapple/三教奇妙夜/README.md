# 三教奇妙夜（macOS）

正常情况下，视频文件本身很难被压缩；因此该压缩包的压缩率十分可疑，基本可以确定 I 帧存在大量冗余。

通过 `ffmpeg -i output.mp4` 读取文件信息，发现该视频长达 11:58:24.28，帧率为 25fps，码率仅有 12kbps，这是疑点二，意味着 B 帧和 P 帧占据绝对多数。

先尝试提取所有关键帧，使用命令 `ffmpeg -i output.mp4 -vf select='eq(pict_type\,I)' -vsync 2 tmp/core-%05d.jpg`。

查看输出的文件，直接通过文件大小升序排列，发现前几个文件包含 flag 中的前五个部分。考虑到 ffmpeg 经常会漏掉末尾的关键帧，使用 `ffmpeg -i output.mp4 -ss 43104 -vsync 2 tmp/last-%02d.jpg` 提取 11:58:00 之后的所有帧，用同上方法可以找到最后一张 flag 的图片。

根据补充信息查阅字形以区别 0 和 O。