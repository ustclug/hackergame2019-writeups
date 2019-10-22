from flask import Flask
from flask import request, session, jsonify, render_template
from flask_session import Session
from calc import Calculator, CalculatorUnknownKey

import random

FLAG = 'flag{you_are_good_at_using_calculators_by_amiya}'

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = b'V\x18\x8e\xa4c4\xbd\x07EI&\xdb\xbc\x9b\x99Q'
Session(app)


"""
Helper functions
"""


def ok(msg):
    data = {
        'code': 0,
        'msg': msg
    }
    return jsonify(data)


def fail(code, msg):
    data = {
        'code': code,
        'msg': msg
    }
    return jsonify(data)


def gen_challenges():
    return [random.uniform(0, 100) for _ in range(3)]


def get_challenges(refresh=False):
    if refresh or not session.get("challenges"):
        session["challenges"] = gen_challenges()
    return session["challenges"]


def check(x, ks):
    if not ks:
        return "empty sequence"
    if len(ks) > 100000:
        return "sequence too long."
    ka = ks.split(',')

    try:
        c = Calculator()
        for k in ka:
            c.click(k)

        if c.equal(x):
            return "passed"
        else:
            return "your result " + str(c.v) + " is not equal to " + str(x) + " (max_error = 1e-5)."

    except CalculatorUnknownKey:
        return "there're unknown key(s)."
    except ValueError:
        return "value error"
    except ZeroDivisionError:
        return "float division by zero"
    except Exception as e:
        print(e)
        return "system error"


"""
Routes
"""


@app.route('/challenges')
def app_challenges():
    ret = get_challenges()
    return ok(ret)


@app.route('/submit', methods=['POST'])
def app_answer():
    ans = [request.form.get("a1"),
           request.form.get("a2"),
           request.form.get("a3")]

    if not session.get('challenges'):
        return fail(-2, 'No challenges for current session. GET /challenges first.')

    cha = get_challenges()

    resp = [check(cha[0], ans[0]),
            check(cha[1], ans[1]),
            check(cha[2], ans[2])]

    if all([x == "passed" for x in resp]):
        return ok(FLAG)
    else:
        get_challenges(refresh=True)
        return fail(-1, resp)


@app.route('/')
def app_index():
    return render_template('index.html')


@app.route('/try', methods=['GET', 'POST'])
def app_try():
    if request.form.get("a"):
        cha = get_challenges()
        new_cha = get_challenges(refresh=True)
        ans = [request.form.get("a1"),
               request.form.get("a2"),
               request.form.get("a3")]
        resp = [check(cha[0], ans[0]),
                check(cha[1], ans[1]),
                check(cha[2], ans[2])]
        flag = None
        if all([x == "passed" for x in resp]):
            flag = FLAG
        return render_template('try.html', submitted=True, cha=new_cha, resp=resp, flag=flag)
    else:
        cha = get_challenges()
        return render_template('try.html', submitted=False, cha=cha)


if __name__ == '__main__':
    app.run("0.0.0.0", 8000, debug=False)
