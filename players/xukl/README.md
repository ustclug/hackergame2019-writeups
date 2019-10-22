# Write-ups

## 三教奇妙夜
有视频处理的地方就有FFmpeg！

### filter blackframe
看到题目中的“黑底白字”的提示，灵机一动：“大概有flag的帧会很黑吧！”（通过观察1分钟的视频可以验证猜想）

通过查阅[冗长的文档](http://ffmpeg.org/ffmpeg-all.html#blackframe)找到一个名为blackframe的filter。

输入命令`ffmpeg -i output.mp4 -vf blackframe why_output.mp4`，输出大致如下。
```
[Parsed_blackframe_0 @ 0x55d873a3f580] frame:1499 pblack:98 pts:767488 t:59.960000 type:I last_keyframe:1499
（下略）
```
从blackframe的输出中能发现黑帧的时间。（以下来自上面提到的FFmpeg文档）
> Output lines consist of the frame number of the detected frame, the percentage of blackness, the position in the file if known or -1 and the timestamp in seconds. 

于是再`ffplay -ss 58`这样看看这帧到底有什么flag就好啦。

此法优点：
* 命令短，不用自己写代码
* 速度较快

缺点：
* 查个文档累死人
