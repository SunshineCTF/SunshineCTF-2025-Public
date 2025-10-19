import urllib
import os


from flask import*
from flask_login import login_required, logout_user

from models import*
from . import admin_blueprint
# ~~~ import the Blueprint from __init__.py

@admin_blueprint.route('/lunar_files')
@login_required
def lunar_files():
    # we're using URL encoding to squash any XSS
    err_msg = request.args.get("err_msg") 
    err_msg = err_msg if err_msg != None else ""
    dict_list: list = get_all_files()
    return render_template('lunar_files.html', dict_list=dict_list, err_msg=err_msg)

@admin_blueprint.route('/download/<path:fname>')
@login_required
def download(fname):
    try:
        base_dir = admin_blueprint.root_path+'/'+'templates/Internal_Lunar_Files'
        fname = fname.strip().rstrip()
        
        # we had to URL encode the names in the front-end to prevent any XSS, this is needed
        # this is exactly what allows the LFI to work too >:) ^^^ (keeping it realistic)
        # NOTE: ^ not true, I just tested it, Python will implicitly URLDecode the fname variables
        # as it's configured to be a <path>

        fname = urllib.parse.unquote(base_dir+'/'+fname)
        print(f"[ Fname we are checking ]: {fname}")
        if not os.path.isfile(fname):
            return redirect(url_for("admin.lunar_files", err_msg="[ Resource Does not Exist! ]"))
        # Return the file
        if fname.count("../../") != 0:
            return redirect(url_for("admin.lunar_files", err_msg="[ Succession of \'../../\' detected, forbidden ]"))
        return send_file(fname, as_attachment=True)
    except Exception as err:
        return jsonify({"ERR": f"An Error Occured ! "})




@admin_blueprint.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return redirect(url_for('admin.help'))

@admin_blueprint.route('/help', methods=['GET'])
@login_required
def help():
    return render_template('help.html')

@admin_blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index.login'))