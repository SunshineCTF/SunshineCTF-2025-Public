from flask import Blueprint

# this is the file that initializes the blueprint and is easily imported into the views.py

admin_blueprint = Blueprint(
    "admin",
    __name__,
    static_folder="static",
    static_url_path="/admin/static",
    template_folder="templates"
)


from . import views
# we need this because in the app.py when we do from admin import admin_blueprint
# our routes (such /dashboard) won't get included if we don't do this, bcs whatever is explicitly written in 
# __init__.py is what gets included.
# NOTE: you can't do from . import views because we're inside of __init__, it works differently, the dir is 
# treated as a package in a sense.