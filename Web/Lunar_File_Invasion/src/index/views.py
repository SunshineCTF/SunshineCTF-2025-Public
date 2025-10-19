import os
from flask_login import login_user, login_required, current_user

from flask import*
from models import*
from . import index_blueprint
# using a dot because in the current directory we have a __init__.py file treated as a package, so cool
# finally used it for once.

from extensions import*
# this has the bcrypt_object for check_password_hash

# NOTE: Now test to see if /login works since we did some login page changes and then start working on the LFI dashboard

@index_blueprint.route('/robots.txt', methods=['GET'])
@index_blueprint.route('/.gitignore_test', methods=['GET'])
def return_as_root_static():
    # return a static file from the root instead of needing to do /static/FNAME
    return send_from_directory(os.path.join(index_blueprint.root_path, 'static'), request.path[1:])


@index_blueprint.route('/', methods=['GET'])
@index_blueprint.route('/index', methods=['GET'])
@index_blueprint.route('/home', methods=['GET'])
def index():
    return render_template('index.html')


@index_blueprint.route('/login', methods=['GET', 'POST'])
def login():    
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    elif request.method == 'GET':
        return render_template('login.html')

    # is a POST request if it's not GET:
    email = request.form.get('email').strip().rstrip()
    attempted_password = request.form.get('password').strip().rstrip()
    
    user_object = get_user_by_email(email)
    if user_object == None:
        # user does not exist
        print(f"[ ****** NO USER FOUND ****** ]")
        return render_template("login.html", err_msg="[ Invalid Logins! ]")
    
    stored_hash = user_object.password
    # now we're going to see if the hashes match
    if bcrypt_object.check_password_hash(stored_hash, attempted_password):
        # this is where the vulnerability occurs (valid session before 2FA pin is validated)
        login_user(user_object)
        return redirect(url_for("index.two_factor_authentication"))
    print(f"[ ****** Actual WRONG CREDENTIALS !  ****** ]")
    return render_template("login.html", err_msg="[ Invalid Logins! ]")


@index_blueprint.route('/2FA', methods=['GET', 'POST'])
@login_required
def two_factor_authentication():
    '''
    this route needs to be logged in so we can get the authenticated user's email
    to pull their 10 digit 2FA pin to verify
    but this is what causes the vulnerability in itself LOL.
    finish this up ^^^

    Reason why I love the login_manager.login_view = 'login'
    '''

    if request.method == "GET":
        return render_template("2FA.html")
    
    attempted_pin = request.form.get('pin').strip().rstrip()
    stored_pin = get_pin_by_email(current_user.email)
    
    # ensure the returned pin isn't None
    if stored_pin != None and attempted_pin == stored_pin:
        return redirect(url_for('admin.dashboard'))
    else:
        # need to be careful to make sure the returned pin is not None
        # AND it's equal to the one the user inputted, we have to do this check
        # bcs the user may be able to force the DBMS to return None and then pass in 
        # no value in &pin=
        # because if there's no 2FA pin somehow stored in DB and user passes in None
        # then it would be a true condition
        return render_template("2FA.html", err_msg="[ Invalid Pin Entered! ]")