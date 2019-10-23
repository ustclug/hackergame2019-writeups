import json
import sys


#idlDicG = {}
#firstIdl = {}
#lastIdl = {}

#used = []
def genDict():
    content = open("./idl.json").read()
    idlDic = json.loads(content)
    firstIdl = {}
    lastIdl = {}
    numDic = {}
    for singleIdl in idlDic:
        first = idlDic[singleIdl]["first"]
        last = idlDic[singleIdl]["last"]
        try:
            firstIdl[first].append(singleIdl)
        except:
            firstIdl[first] = []
            firstIdl[first].append(singleIdl)
        try:
            lastIdl[last].append(singleIdl)
        except:
            lastIdl[last] = []
            lastIdl[last].append(singleIdl)
    for i in firstIdl:
        numDic[i] = len(firstIdl[i])
    return firstIdl, lastIdl, idlDic, numDic
    
def regenDict(idlDic):
    firstIdl = {}
    lastIdl = {}
    numDic = {}
    for singleIdl in idlDic:
        first = idlDic[singleIdl]["first"]
        last = idlDic[singleIdl]["last"]
        try:
            firstIdl[first].append(singleIdl)
        except:
            firstIdl[first] = []
            firstIdl[first].append(singleIdl)
        try:
            lastIdl[last].append(singleIdl)
        except:
            lastIdl[last] = []
            lastIdl[last].append(singleIdl)
    for i in firstIdl:
        numDic[i] = len(firstIdl[i])
    return firstIdl, lastIdl, numDic
        
def writeUsed(idl):
    with open("used.txt","a+") as f:
                f.write(" ")
                f.write(idl)
                



def deal(idl,used,idlDic):
    #genDict()
    '''
    with open("used.txt","r") as f:
        content = f.read()
        used = content.split(" ")
    '''
    #writeUsed(idl)
    #global idlDicG
    #idlDicG = idlDic
    try:
        for i in used:
            idlDic.pop(i)
    except:
        pass
    firstIdl, lastIdl, numDict =regenDict(idlDic)
    #idlDic = idlDic - used
    cantTouch = ['gei','lia','niang','cou','nou','fou',"nao","teng"]
    justOne = ['seng','shua','pie','zen','shuan','reng','nve','nuan','run']
    cantTouch = cantTouch + justOne
    
    
    last = idlDic[idl]["last"]
    idlOutputList = firstIdl[last]
    idlOutputList = sorted(idlOutputList,key = lambda a:len(firstIdl[idlDic[a]["last"]]))
    '''
    for i in (idlOutputList):
        print len(firstIdl[idlDic[i]["last"]]),idlDic[i]["last"]
    '''
    for singleOutput in idlOutputList:
        #firstOut = idlDic[singleOutput]["first"]
        #if firstOut in warningList:
        #    warn = True
        conputerOutput = firstIdl[idlDic[singleOutput]["last"]]
        fail = False
        for singleCOutput in conputerOutput:
            firstOut = idlDic[singleCOutput]["last"]
            if (idlDic[singleCOutput]["last"] in cantTouch):
                fail = True
            if idl == singleCOutput:
                fail = True
            '''
            if firstOut in warningList:
                fail = True
            '''
        if fail:
            continue
        '''
        for singleCOutput in conputerOutput:
            if not(idlDic[singleCOutput]["last"] not in cantTouch and singleOutput not in used) :
                continue
            if not idlDic[singleCOutput]["last"] == idlDic[singleCOutput]["first"] and singleOutput not in used:
                return singleOutput
        '''
        if idlDic[singleOutput]["last"] in cantTouch and singleOutput not in used:
            #used.append(singleOutput)
            #writeUsed(singleOutput)
            return singleOutput
        '''   
        if idlDic[singleOutput]["last"] == idlDic[singleOutput]["first"] and singleOutput not in used:
            used.append(singleOutput)
            return singleOutput
        '''
        if singleOutput not in used :# and not warn :
            #writeUsed(singleOutput)
            return singleOutput
        '''
        if singleOutput not in used and not warn :
            #writeUsed(singleOutput)
            return singleOutput
        '''
        #return singleOutput
    print "Died in %s" % last

    
            
    