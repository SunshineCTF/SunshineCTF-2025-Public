import os
import json
from markupsafe import escape
from flask import Flask, request, make_response
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)
KEY = os.urandom(16)  # fixed per server run

def encrypt_cookie(data: dict) -> str:
    cipher = AES.new(KEY, AES.MODE_ECB)
    pt = pad(json.dumps(data).encode(), 16)
    ct = cipher.encrypt(pt)
    return ct.hex()

def decrypt_cookie(cookie_hex: str) -> dict:
    ct = bytes.fromhex(cookie_hex)
    cipher = AES.new(KEY, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ct), 16)
    return json.loads(pt.decode())


def read_flag():
    with open("/flag", "r") as fl: return fl.readline()

@app.route("/", methods=["GET", "POST"])
def index():
    cookie_hex = request.cookies.get("clicker")

    if not cookie_hex:
        # First visit: ask for name
        if request.method == "POST":
            name = request.form.get("name", "anon")
            data = {"name": name, "count": 0}
            cookie_hex = encrypt_cookie(data)
            resp = make_response(render_game(name, 0))
            resp.set_cookie("clicker", cookie_hex)
            return resp

        return '''
            <html>
            <head>
                <title>Moon Clicker</title>
                <link rel="icon" type="image/png" href="/static/moon.png">
                <style>
                    body { font-family: sans-serif; text-align: center; margin-top: 100px; }
                    input { padding: 8px; font-size: 1em; }
                    button { padding: 8px 16px; font-size: 1em; }
                </style>
            </head>
            <body>
                <h1> Welcome to Moon Clicker!</h1>
                <form method="post">
                    <input name="name" placeholder="Enter your name">
                    <button type="submit">Start</button>
                </form>
            </body>
            </html>
        '''

    try:
        data = decrypt_cookie(cookie_hex)
    except Exception:
        return "Invalid cookie!"

    return render_game(data["name"], data["count"])

@app.route("/click", methods=["POST"])
def click():
    cookie_hex = request.cookies.get("clicker")
    try:
        data = decrypt_cookie(cookie_hex)
    except Exception:
        return "Invalid cookie!"

    data["count"] += 1
    cookie_hex = encrypt_cookie(data)

    resp = make_response(render_game(data["name"], data["count"]))
    resp.set_cookie("clicker", cookie_hex)
    return resp

def render_game(name: str, count: int) -> str:
    name = escape(name)
    flag = ""
    if count >= 0x13371337:
        flag = f'<script>alert("{read_flag()}")</script>'
    return f'''
    <html>
    <head>
        <title>Moon Clicker</title>
        <link rel="icon" type="image/png" href="/static/moon.png">
        <style>
            body {{
                font-family: 'Comic Sans MS', sans-serif;
                color: #222;
                text-align: center;
                padding-top: 50px;
            }}
            h1 {{ font-size: 2.5em; }}
            h2 {{ margin-top: 10px; }}
            form {{ margin-top: 20px; }}
            button.moon {{
                background: none;
                border: none;
                cursor: pointer;
            }}
            img {{
                width: 200px;
                transition: transform 0.1s;
            }}
            img:active {{
                transform: scale(0.9);
            }}
        </style>
    </head>
    <body>
        <h1> Moon Clicker</h1>
        <h2>Hello, {name}!<br>You have <b>{count}</b> moons.</h2>
        <form action="/click" method="post">
            <button class="Moon">
                <img src="/static/moon.png" alt="Moon">
            </button>
        </form>
        {flag}
    </body>
    </html>
    '''

def create_app():
    return app

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=25402,debug=False)
