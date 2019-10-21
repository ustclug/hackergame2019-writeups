FROM ubuntu:rolling

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update
RUN apt upgrade -y
RUN apt install -y cmake python3-pip libssl-dev
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple flask-socketio gevent-websocket gunicorn numpy pyopenssl

COPY . /tmp
COPY ./app /app
WORKDIR /tmp

RUN python3 gen.py
RUN cmake .
RUN make
RUN cp libladder.so /app
RUN cp idlist.txt /app
RUN cp pinyinlist.txt /app
RUN cp idl.json /app/static

EXPOSE 5000

WORKDIR /app
CMD gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 --bind 0.0.0.0:5000 --log-file access.log --log-level info app:app