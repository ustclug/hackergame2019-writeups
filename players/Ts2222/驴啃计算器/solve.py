from __future__ import division

from pwn import *
from numpy import *
from fractions import Fraction

calcList = []

def genFraction(num,n=20):
    f = Fraction(num)
    a = f.numerator
    b = f.denominator
    a = a*a
    b = b*b
    for i in range(n):
        result = a//b
        a = a - result*b
        #print a,b
        a,b = b,a
        #print a,b
        '''
        if result == 1:
            break
        '''
        #if result > 5000:
        #    break
        yield result
        if b == 0:
            break
        
def f(x):
    global calcList
    calcList += ["atan","sin","acos","tan"]
    return tan(arccos(sin(arctan(x))))
    
def g(x):
    global calcList
    calcList += ["atan","cos"]
    return f(cos(arctan(x)))
    
def test(aim):
    global calcList
    #aim = log(aim)
    #aim = 42.79781263758425 #tan(72.35711075569202)
    aim = deg2rad(aim)
    x = 0
    fList = []
    for i in genFraction(aim):
        fList.append(i)
    print fList
    for i in range(len(fList)):
        a = fList.pop()
        for j in range(a):
            x = g(x)
        calcList += ["1/x"]
        x = 1/x
    calcList += ["1/x"]
    x = 1/x
    calcList += ["R2D"]
    print "aim = %f" % rad2deg(aim)
    print "x = %f" % (rad2deg(x))
    #print "p = %f" % ((x*x))
    return ",".join(calcList)
    
  

import json
import requests

host = "http://202.38.93.241:10024"


def solve(x):
    return 'sin,cos,x^2' or 'magic'

def test2():
    with requests.session() as sess:
        r = sess.get(host + '/challenges')
        X = json.loads(r.text)["msg"]
        print(X)
        data = {
            "a1": test(X[0]),
            "a2": test(X[1]),
            "a3": test(X[2])
        }
        r = sess.post(host + "/submit", data=data)
        resp = json.loads(r.text)
        print(resp["msg"])  
    
test2()