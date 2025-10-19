# asgi.py
from asgiref.wsgi import WsgiToAsgi
from app import app as wsgi_app  # imports your Flask app instance

app = WsgiToAsgi(wsgi_app)  # ASGI callable