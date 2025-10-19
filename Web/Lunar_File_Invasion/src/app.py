import os

with open("./FLAG/flag.txt", "r") as f:
    FLAG = f.read()

from flask import *
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_wtf.csrf import CSRFError

# blueprint stuff:
from models import *
from admin import admin_blueprint
from index import index_blueprint
# ^^ this is what I meant by:
# "the dir is"
# treated as a package in a sense.

# global
from extensions import *


# clean up the login page and make it functional then we can start piecing together the LFI dashboard
# functionality too

# Initializing the app-specific stuff:
app = Flask(__name__)

# registering the blueprint
app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(index_blueprint, url_prefix="/")
# app.static_folder = 'global_static'

app.config["SECRET_KEY"] = os.urandom(64).hex()
bcrypt_object.init_app(app)

# since we're directly pass in the app object we can directly use it in our templates with JINJA2 syntax
csrf.init_app(app)

# I know for a fact ppl will try to bruteforce the pin which is millions of requests,
# we're stopping that before it begins with the default rate-limit being set to 5 requests/second.

# TODO: remove this, just use NGINX, kills 2 birds with 1 stone bcs we can also config passwd for kev's test instance.

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = (
    "index.login"  # Redirect to admin login page if not logged in
)
# the way this works is it checks if current_user.is_authenticated is set to True, this value is retrieved from
# the load_user() function (so it's called everytime implicitly on routes that have the @login_required() decorator


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(user_id)


################################################################


# Wrapper for Error handling any invalid CSRF tokens.
@app.errorhandler(CSRFError)
def handle_csrf_error(error):
    return render_template(
        "error.html",
        err_msg=f"[ Invalid CSRF Token, if this persists please enable JavaScript. ]",
    ), 400


################################################################
def create_app():
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=False)
