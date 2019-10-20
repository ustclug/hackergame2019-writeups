import sys
from PIL import Image


def converge(c1,c2):
    c=round(255*c1/(255+c1-c2)) if 255+c1-c2!=0 else 0
    alpha=255+c1-c2 if 255+c1-c2<=255 else 255
    return (c,alpha)


name1=input("Input the name of bright image:")
name2=input("Input the name of dark image:")
name3=input("Input the name of output image")


bright=Image.open(name1,'r').convert('LA').split()[0]
dark=Image.open(name2,'r').convert('LA').split()[0]
assert(dark.size==bright.size)


newData=list(map(converge,dark.getdata(),bright.getdata()))

newImg = Image.new('LA',dark.size)
newImg.putdata(newData)
newImg.save(name3, "PNG")