import bcrypt

from sqlalchemy import create_engine, Column, Integer, String
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the database
engine = create_engine('sqlite:///database.db', echo=True)
# this is how SQLAlchemy tracks the tables you define via the class directive
Base = declarative_base()

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define model classes (tables)
# UserMixin -> allows it to work with the Flask-login
# for example it allows us to do stuff like current_user.password and more.
class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    pin = Column(String)
    # authed = False
    # can't do this bcs it's only persistent in current response, if we wanted it to remain 
    # in another route like 2FA after going to dashboard we'd need to .commit() it to the DB


    def __repr__(self):
        return f"<User( email='{self.email}', password='{self.password}', pin='{self.pin}' )>"

class File(Base, UserMixin):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"<File( name='{self.name}' )>"


# general functions:
def hash_password(password: str):
    # Generates salt (Bcrypt does for us), hashes password, replaces plaintext password with a secure hash.

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # Store the hashed password
    return hashed_password
def get_user_by_email(email):
    # Query for a specific email
    user = session.query(User).filter_by(email=email).first()
    return user

def get_pin_by_email(email):
    # using email query for their pin:
    user = session.query(User).filter_by(email=email).first()
    return user.pin

def get_all_files() -> list:
    # Query for all of the files in the database
    internal_files = session.query(File).all()
    if internal_files == None:
        return [{}]
    
    files_list = []
    for idx,element in enumerate(internal_files):
        files_list.append({'id': idx+1, 'name': element.name})
    return files_list