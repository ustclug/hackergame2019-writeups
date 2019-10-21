from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect
import ctypes
import copy
import random
import binascii
import base64
import OpenSSL
import os
import fcntl
from hashlib import sha256

idl = open("idlist.txt").read().split()
pyl = []
for p in open("pinyinlist.txt").read().splitlines():
    pyl.append(tuple(map(int, p.split())))
with open("cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())

pinyindict = {}
iddict = {}
for i in range(len(idl)):
    pinyindict[idl[i]] = pyl[i]
    if pyl[i] not in iddict:
        iddict[pyl[i]] = []
    iddict[pyl[i]].append(idl[i])

"""
    Ladder* ladder_init(int cur, int seed){return new Ladder(cur,1,seed);}
    int ladder_search(Ladder* l){return l->LadderSearch(playouts);}
    void ladder_move(Ladder* l, int n){l->LadderMove(n);}
    int ladder_result(Ladder* l){return l->GetLadderResult();}
    void ladder_destroy(Ladder* l){delete l;}
"""
lib = ctypes.cdll.LoadLibrary('./libladder.so')
lib.ladder_init.argtypes = [ctypes.c_int, ctypes.c_int]
lib.ladder_init.restype = ctypes.c_void_p
lib.ladder_search.argtypes = [ctypes.c_void_p]
lib.ladder_search.restype = ctypes.c_int
lib.ladder_result.argtypes = [ctypes.c_void_p]
lib.ladder_result.restype = ctypes.c_int
lib.ladder_move.argtypes = [ctypes.c_void_p, ctypes.c_int]
lib.ladder_destroy.argtypes = [ctypes.c_void_p]
class Ladder:
    def __init__(self, success, token):
        self.cur = 72   #flxg
        self.l = lib.ladder_init(self.cur, random.randint(0, 65536))
        self.id = copy.deepcopy(iddict)
        self.success = success
        self.token = token
    def search(self):
        r = lib.ladder_search(self.l)
        return random.choice(self.id[(self.cur,r)])
    def result(self):
        return lib.ladder_result(self.l)
    def move(self, s):
        n = pinyindict[s][1]
        self.id[(self.cur,n)].remove(s)
        lib.ladder_move(self.l, n)
        self.cur = n
    def __del__(self):
        lib.ladder_destroy(self.l)

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['SECRET_KEY'] = '--Secret.key.idiom--'
socketio = SocketIO(app)

statusdict = {}

check_path = "/data"
def check_connecntions(uid):
    fd = os.open(os.path.join(check_path, uid), os.O_CREAT | os.O_RDWR)
    fcntl.flock(fd, fcntl.LOCK_EX)
    with os.fdopen(fd, "r+") as f:
        data = f.read()
        num = 0
        if data:
            num = int(data)
            if num > 3:
                return True
        f.seek(0)
        f.write(str(num+1))
        return False

def remove_connections(uid):
    fd = os.open(os.path.join(check_path, uid), os.O_CREAT | os.O_RDWR)
    fcntl.flock(fd, fcntl.LOCK_EX)
    with os.fdopen(fd, "r+") as f:
        data = f.read()
        num = 1
        if data:
            num = int(data)
        f.seek(0)
        f.write(str(num-1))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('go')
def do_message(message):
    if request.sid not in statusdict:
        disconnect()
    l = statusdict[request.sid]
    s = message['data'].strip()
    if s not in pinyindict:
        emit('reply', {'data': "未识别的成语!"})
        return
    cur, n = pinyindict[s]
    if cur != l.cur:
        emit('reply', {'data': "错误的拼音!"})
        return
    if s not in l.id[(cur,n)]:
        emit('reply', {'data': "已经使用过的成语!"})
        return
    l.move(s)
    if l.result() != 0:
        l.success += 1
        emit('reply', {'data': "成功领取红包! 你已收集 flag 碎片 %d/4" % l.success})
        if l.success < 4:
            l = Ladder(l.success, l.token)
            statusdict[request.sid] = l
            response = "废理兴工"
            l.move(response)
            emit('reply', {'data': "服务器给你发送了一个接龙红包:"})
            emit('reply', {'data': response})
            return
        else:
            emit('reply', {'data': "恭喜你, 你成功获得 flag 红包奖励~"})
            flag = "flag{True_Virtuoso_of_Chinese_Idioms_" + f"{sha256(('id'+l.token).encode()).hexdigest()[:10]}" + "}"
            emit('reply', {'data': flag})
            return
    response = l.search()
    l.move(response)
    if l.result() != 0:
        response += """
            <img style="width: 30px; height: 30px;" src="data:image/png;base64, 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"/>
            """
    emit('reply', {'data': response})

@socketio.on('connect')
def do_connect():
    try:
        token = request.cookies.get("token")
        uid, sig = token.split(":", 1)
        sig = base64.b64decode(sig, validate=True)
        OpenSSL.crypto.verify(cert, sig, uid.encode(), "sha256")
    except:
        emit('error', {'data': "错误的 token! 请从比赛平台进入."})
        return
    if check_connecntions(uid):
        emit('error', {'data': "并发数过高!"})
        return
    l = Ladder(0, token)
    statusdict[request.sid] = l
    response = "废理兴工"
    l.move(response)
    emit('reply', {'data': "服务器给你发送了一个接龙红包:"})
    emit('reply', {'data': response})

@socketio.on('disconnect')
def do_disconnect():
    try:
        uid, sig = statusdict[request.sid].token.split(":", 1)
        remove_connections(uid)
        del statusdict[request.sid]
    except Exception:
        pass

if __name__ == '__main__':
    socketio.run(app)