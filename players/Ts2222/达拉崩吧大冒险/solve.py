#coding=utf-8
import websocket,json
flag = False

def on_message(ws, message):
    dic = json.loads(message)
    
    #print flag
    print "From : %s" % dic["From"]
    print "Content : %s" % dic["Content"]
    print "State : %d,Attack : %d,Money : %d,Name : %s" % (dic["State"]["Stage"],dic["State"]["Attack"],dic["State"]["Money"],dic["State"]["Name"])
    #input = raw_input()
    

        
    '''
    if dic["Content"] == u"你感觉自己浑身充满了干劲":
        ws.send("0")
    ''' 
    if dic["From"] == u"隔壁王大妈":
        ws.send("-%d" % 2**61)
        flag = True
    if u"站住！" in dic["Content"]:
        ws.send("0")
    if u"若是" in dic["Content"]:
        ws.send("0")
    if u"巨龙" in dic["From"]:
        ws.send("0")
    
    if flag:
        if dic["Content"] == u"接下来，你想去哪里呢？":
            ws.send("2")
    
    else:
        if dic["Content"] == u"接下来，你想去哪里呢？":
            ws.send("0")
    

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://202.38.93.241:10021/ws",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              cookie = "")
    ws.run_forever(ping_interval=0)

