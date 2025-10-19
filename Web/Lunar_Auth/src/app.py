from flask import *

app = Flask(__name__)

# instead of using SQLITE we'll keep the load simple and just use an in-memory dictionary man:
admin_credentials = {"username": "alimuhammadsecured", "password": "S3cur4_P@$$w0RD!"}


# for static directories:
@app.route("/robots.txt")
def statuc_send_as_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        return render_template("admin.html")
    # handle login logic here
    username = request.form.get("username", "NONE")
    password = request.form.get("password", "NONE")

    if (username == admin_credentials["username"]) and (
        password == admin_credentials["password"]
    ):
        flag = open("flag.txt", "r").read()
        return render_template("flag.html", flag=flag)
    # we're using client-side auth, so this should be impossible to trigger (LMAO):
    return jsonify({"err": "Invalid Credentials"})


def create_app():
    return app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
