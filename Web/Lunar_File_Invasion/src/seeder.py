import sys
import os
import random
from models import*


class Seeder(object):
    def __init__(self):
        ...
    def create_tables(self):
        # create all the needed tables: users, contact us submissions, etc
        Base.metadata.create_all(engine)
        # ^ it's able to know which tables to create because we pass in "Base" for inheritance in 
        # our table classes like check the User one in src.database_utils.py

    def seed_users(self):
        # TODO: generate random creds from ENV, bcs ppl will just share the creds and then login
        # seed all users including their password's salted hashes            
        users_data = {
            "LunarAdmins": {
                "email": "admin@lunarfiles.muhammadali",
                "password": hash_password("jEJ&(32)DMC<!*###"),
                "pin": f"{random.randint(1111111111, 9999999999)}"
                # TODO: pull from ENV where it's randomly generated
            }
        }

        # seed all of the users:
        for key, values in users_data.items():
            try:
                user = User(email=values['email'], password=values['password'], pin=values['pin'])
                session.add(user)
                session.commit()
            except Exception as err:
                print(f"[ In seed_users() --> {err} ]")
                sys.exit(0)

    def seed_files(self):
        # this helps me for future CTFs, for example let's say I want to add functionality for file uploads dynamically from the admin
        # and stuff (always program like you're in production :WINK:)
        for id,fname in enumerate(os.listdir("./admin/templates/Internal_Lunar_Files")):
            try:
                file_record = File(name=fname)
                session.add(file_record)
                session.commit()
            except Exception as err:
                print(f"[ When seeding file \'{fname}\' --> {err}]")
                sys.exit(0)

seederObj = Seeder()
seederObj.create_tables()
seederObj.seed_users()
seederObj.seed_files()
