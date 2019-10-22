这道题我看到是每个一段一个全黑背景图的帧的时候，想到了之前做图像处理用的opencv，
想要按帧比较，但是想到是10个小时的视频，于是选择了只比较一个像素，然后用python写成脚本，跑了大约5min就能出结果

```
import cv2
vc=cv2.VideoCapture("output.mp4")  #读入视频文件  
c=1  
if vc.isOpened():
    rval,frame=vc.read()
else:
    rval=False
count=0
save=0
while True:
    count=count+1
    if(count%60000==0):
        print("[*]"+str(count))
    rval,frame=vc.read()
    #print(len(frame[0]))
    if(frame[150][150][1]!=save): #每隔timeF帧进行存储操作
        cv2.imwrite(str(c)+'.jpg',frame) #存储为图像
        c=c+1
        save=frame[150][150][1]
        #print(frame[0][0][0])
vc.release()
```
