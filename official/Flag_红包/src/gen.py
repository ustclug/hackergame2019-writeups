import json
import numpy as np

j=json.loads(open("idl.json").read())

pinyin=set()
lose=set()
win=set()

for w in j:
    pinyin.add(j[w]['first'])
    pinyin.add(j[w]['last'])

flag = True

while flag:
    temp=set()
    for w in j:
        if j[w]['last'] in pinyin:
            temp.add(j[w]['first'])
    flag=bool(pinyin-temp-lose)
    lose|=pinyin-temp
    for w in j:
        if j[w]['last'] in lose:
            win.add(j[w]['first'])
            pinyin-=set([j[w]['first']])

kernel=list(pinyin-lose)
win=list(win)
lose=list(lose)
kernel.sort()
win.sort()
lose.sort()
pinyin=kernel+win+lose

m=np.zeros((len(pinyin),len(pinyin)), dtype='uint8')
wl=open("idlist.txt","w")
pl=open("pinyinlist.txt","w")
for w in j:
    print(w, file=wl)
    a = pinyin.index(j[w]['first'])
    b = pinyin.index(j[w]['last'])
    print("%d %d"%(a,b), file=pl)
    m[a,b]+=1
wl.close()
pl.close()

idm=open("idm.h", "w")
s="int8_t idm[ntotal*ntotal] = {\n"
for x in m:
    for y in x:
        s+="%d, "% y
    s=s[:-1]
    s+='\n'
s=s[:-2]
s+="\n};"
idm.write(s)
idm.close()

idn=open("idn.h", "w")
print(f"const int nkernel = {len(kernel)};", file=idn)
print(f"const int nwin = {len(win)};", file=idn)
print(f"const int nlose = {len(lose)};", file=idn)
print(f"const int ntotal = {len(pinyin)};", file=idn)
print(f"const int nidioms = {len(j)};", file=idn)
idn.close()