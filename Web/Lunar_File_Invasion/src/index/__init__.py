from flask import Blueprint

index_blueprint = Blueprint(
    "index",
    # ~~~ this is useful for templates like instead of {{ url_for('login') }} we do 
    # {{ url_for('index.login') }}, super cool.
    __name__,
    static_folder="static",
    static_url_path="/index/static",
    template_folder="templates"
)
from . import views