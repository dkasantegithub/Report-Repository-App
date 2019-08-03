import os
from flask import Flask
from models import *

# configure app
app = Flask(__name__)

# configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://cktvjbbezjkxui:83313b7459a9e34aca734a4a9110425ef801995356ef9b3ff282a098c8f73582@ec2-174-129-194-188.compute-1.amazonaws.com:5432/d5incue9u4v8nv'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()