# pip3 install websocket_client
from websocket import create_connection
a = -1900000000000000000 # answer
url = ""
def ta(a):
    ws = create_connection("ws://202.38.93.241:10021/ws")
    result = ws.recv()
    ws.send("0")
    result = ws.recv()
    result = ws.recv()
    ws.send("0")
    result = ws.recv()
    result = ws.recv()
    ws.send("0")
    result = ws.recv()
    ws.send(str(a))
    result = ws.recv()
    result = ws.recv()
    ws.send("2")
    result = ws.recv()
    ws.send("0")
    result = ws.recv()
    result = ws.recv()
    result = ws.recv()
    ws.send("2")
    result = ws.recv()
    result = ws.recv()
    print(result)
    ws.close()

ta(a)