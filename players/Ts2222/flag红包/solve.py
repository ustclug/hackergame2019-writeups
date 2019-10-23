import websocket, json, idlDict
try:
    import thread
except ImportError:
    import _thread as thread
import time

TOKEN = "13:MEUCIBLRnlEgplGtm3n2ks1PdVezT6X56PsIAxeByvSUK0RpAiEA0yhnSTSY+1k9VcS5UHlwvRxWjSR7/TtKNRC8YIi3Qr0="
cantTouch = ['gei','lia','niang','cou','nou','fou']
used = []
firstIdl = {}
lastIdl = {}
idlDic = {}
numDic = {}

def debug_info(idl):
    #print idl
    #first = idlDic[idl]["last"]
    last = idlDic[idl]["last"]
    #print numDic
    print "last = %s and len(dic) = %d" % (last,len(firstIdl[last]))

'''
def genWarnList():
    warnlist = []
    for i in numDic:
        if numDic[i]<= 10:
            warnlist.append(i)
    return warnlist
'''
    
def dealUsed(idl):
    used.append(idl)
    #a = idlDic.pop(idl)
    #print(type(idlDic))
    #numDic[idlDic[idl]['first']] =- 1 

def on_message(ws, message):
    ws.send('2')
    if message != "3":
        pass
        #print message
    if message[:2]=="42":
        try:
            locate = message.index("[")
            msg = message[locate:]
            msgDict = json.loads(msg)
            currentIdl = msgDict[1]['data'].split("\n")[0]
            #print currentIdl
            if len(currentIdl) == 4:
                #global firstIdl
                #sendMsg = raw_input().decode("utf-8").encode("unicode-escape")
                #ws.send(sendMsg)
                debug_info(currentIdl)
                print "s: " + currentIdl
                #used.append(currentIdl)
                
                #warn = genWarnList()
                sendMsg = idlDict.deal(currentIdl,used,idlDic)
                print "c: " + sendMsg
                #used.append(sendMsg)
                
                dealUsed(currentIdl)
                dealUsed(sendMsg)
                ws.send('42["go",{"data":"%s"}]' % sendMsg)
            else:
                print "s: " + currentIdl
                if "flag" in currentIdl :
                    global idlDic,used
                    firstIdl,lastIdl,idlDic,numDic = idlDict.genDict()
                    used = []
                    
        except:
            pass
    '''
    else:
        print message
    '''

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")



if __name__ == "__main__":
    with open("used.txt","w") as f:
        pass
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://202.38.73.168:8081/socket.io/?EIO=3&transport=websocket",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              cookie = "_593da=http://172.31.0.10:5000; token=%s" % TOKEN)
    #ws.on_open = on_open
    firstIdl,lastIdl,idlDic,numDic = idlDict.genDict()
    
    if ws.run_forever(ping_interval=0):
        print "FUCK!"