from flask import Flask, render_template, request, send_from_directory
import requests  # well, requests is designed for humans, and I like it.


app = Flask(__name__)
whitelist_hostname = ["example.com",
                     "www.example.com"]
whitelist_scheme = ["http://"]


def check_hostname(url):
    for i in whitelist_scheme:
        if url.startswith(i):
            url = url[len(i):]  # strip scheme
            url = url[url.find("@") + 1:]  # strip userinfo
            if not url.find("/") == -1:
                url = url[:url.find("/")]  # strip parts after authority
            if not url.find(":") == -1:
                url = url[:url.find(":")]  # strip port
            if url not in whitelist_hostname:
                return (False, "hostname {} not in whitelist".format(url))
            return (True, "ok")
    return (False, "scheme not in whitelist, only {} allowed".format(whitelist_scheme))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/request")
def req_route():
    url = request.args.get('url')
    status, msg = check_hostname(url)
    if status is False:
        # print(msg)
        return msg
    try:
        r = requests.get(url, timeout=2)
        if not r.status_code == 200:
            return "We tried accessing your url, but it does not return HTTP 200. Instead, it returns {}.".format(r.status_code)
        return r.text
    except requests.Timeout:
        return "We tried our best, but it just timeout."
    except requests.RequestException:
        return "While accessing your url, an exception occurred. There may be a problem with your url."


@app.route("/source")
def get_source():
    return send_from_directory("/static/", "app.py", as_attachment=True)


if __name__ == '__main__':
    app.run("0.0.0.0", 8000, debug=False)
