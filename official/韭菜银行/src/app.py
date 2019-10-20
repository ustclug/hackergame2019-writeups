from web3.auto.infura.kovan import w3
import OpenSSL
import base64
from flask import Flask, request
import os
import hashlib

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>JCBank</title>
</head>
<body>
<form method='post'>
<label for='name'>Token:</label>
<input type="text" name="token" id="token">
<input type="submit" value="Get flag">
</form>
<script>
var token = new URLSearchParams(window.location.search).get("token");
if (token) document.getElementById("token").value = token;
</script>
</body>
</html>
"""

with open("JCBank.abi") as f:
    abi = f.read()

challenge = w3.eth.contract(address=os.environ["contract_address"], abi=abi)

with open("cert.pem") as f:
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, f.read())


def validate(token):
    try:
        id, sig = token.split(":", 1)
        sig = base64.b64decode(sig, validate=True)
        OpenSSL.crypto.verify(cert, sig, id.encode(), "sha256")
        return id
    except Exception:
        return None


def got_flag(id):
    return challenge.functions.got_flag(id).call()


def sha256(m):
    return hashlib.sha256(m.encode()).hexdigest()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form["token"].strip()
        id = validate(token)
        if id is None:
            return "Invalid token"
        user_id = int(sha256(token)[:10], 16)
        try:
            win = got_flag(user_id)
        except:
            return "There's some network issues, please try again. If this problem persists, please contact admin."
        if win:
            return (
                f"flag{{Y0U_kn0w_EVM_r33ntr4ncy_attack_{sha256('JCBank'+token)[:10]}}}"
            )
        else:
            return (
                f"You can get your flag only if got_flag({user_id}) is true in the contract. "
                f"只有合约中 got_flag({user_id}) 为真时可以获得 flag。"
            )
    else:
        return html
