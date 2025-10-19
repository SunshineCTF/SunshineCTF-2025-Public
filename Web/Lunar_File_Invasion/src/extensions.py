from flask_bcrypt import Bcrypt
from flask_wtf import CSRFProtect

bcrypt_object = Bcrypt()
csrf = CSRFProtect()