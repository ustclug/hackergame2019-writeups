FROM python:3.7
RUN pip install flask web3 pyopenssl
COPY app.py JCBank.abi /
COPY cert.pem /
ENV FLASK_APP app.py
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0
CMD ["flask", "run"]
