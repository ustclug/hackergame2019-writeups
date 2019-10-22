# ustc-hackergame-2019
## 三教奇妙夜

使用ffmpeg分析帧之间的差别并输出具有差别的帧
参考 https://www.bogotobogo.com/FFMpeg/ffmpeg_thumbnails_select_scene_iframe.php 中的 “Capturing scene change“ 一节

```
ffmpeg -i input.mp4 -vf  "select=gt(scene\,0.3), scale=320:240" -vsync vfr flag_frame%03d.png
```

即可输出带有flag的关键帧。

（一共能输出12张图片，其中包括6张带有flag的图片）
