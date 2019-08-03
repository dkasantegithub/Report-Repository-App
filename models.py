from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User Model """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    portfolios = db.Column(db.String, unique=True, nullable=False)

class File(UserMixin, db.Model):
    """File Model"""

    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, unique=True, nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)