#!/usr/bin/python3

from datetime import datetime
from flask import request, Flask, Response

app = Flask(__name__)

def wrapped(res):
    date = datetime.utcfromtimestamp(3400272000)
    format_str = '%a, %d %b %Y %H:%M:%S GMT'
    res.headers['Content-Type'] = 'text/plain; charset=utf-8'
    res.headers['Last-Modified'] = date.strftime(format_str)
    return res

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/flag.txt', methods = ['POST'])
def flag():
    date = request.if_unmodified_since
    text = 'flag{Welc0me_to_competit1on_in_2077}'
    cond = date is not None and 3400272000 <= date.timestamp()
    return wrapped(Response(text)) if cond else wrapped(Response(status=412))

