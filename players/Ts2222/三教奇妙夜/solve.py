import hashlib
import os
import cv2
from tqdm import trange
 
#rm_all()
def readVideo(name):
    cap = cv2.VideoCapture(name)
    #_, frame1 = cap.read()
    i = 0
    count = cap.get(7)
    for i in trange(int(count)-1):
        ret, frame = cap.read()
        if (frame[104, 40] == [0,0,0]).all():
            cv2.imwrite("./images/%d.jpeg" % i, frame)
            
readVideo("output.mp4")
#readVideo("test.mp4")      