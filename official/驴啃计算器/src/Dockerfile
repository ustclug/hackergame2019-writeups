FROM debian:buster-slim
COPY requirements.txt /tmp/
RUN apt update && apt install -y python3-dev python3-pip && rm -rf /var/lib/apt/lists/* \
&& pip3 install -r /tmp/requirements.txt && mkdir /app && mkdir /var/log/gunicorn
WORKDIR /app
CMD ["gunicorn", "-w", "8", "-k", "eventlet", "-b", "0:8000", "--error-logfile", "/var/log/gunicorn/error.log", "--access-logfile", "/var/log/gunicorn/access.log", "app:app"]
