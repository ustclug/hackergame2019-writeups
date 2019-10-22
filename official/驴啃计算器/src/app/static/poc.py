import json
import requests

host = "http://202.38.93.241:10024"


def solve(x):
    return 'sin,cos,x^2' or 'magic'


with requests.session() as sess:
    r = sess.get(host + '/challenges')
    X = json.loads(r.text)["msg"]
    print(X)
    data = {
        "a1": solve(X[0]),
        "a2": solve(X[1]),
        "a3": solve(X[2])
    }
    r = sess.post(host + "/submit", data=data)
    resp = json.loads(r.text)
    print(resp["msg"])