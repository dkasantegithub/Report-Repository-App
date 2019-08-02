from flask_wtf import FlaskForm
from passlib.hash import pbkdf2_sha256
from wtforms import StringField, PasswordField,SelectField,SubmitField
from wtforms.validators import InputRequired,Length, EqualTo, ValidationError
from models import *


# Custom Validators for Login Form
def invalid_credentials(form, field):
    """Username and Password Checker"""

    username_entered = form.username.data
    password_entered = form.password.data

    # Check if username is valid
    username_object = User.query.filter_by(username=username_entered).first()
    if username_object is None:
        raise ValidationError('Username or Password is incorrect')

    # Verify for the hashed password
    elif not pbkdf2_sha256.verify(password_entered, username_object.password):
        raise ValidationError('Username or Password is incorrect')



class RegistrationForm(FlaskForm):
    """Registration Form"""

    username = StringField('username', validators=[InputRequired(message='Username Required'),
     Length(min=4, max=25, message='username must be between 4 anad 25 characters')
     ])

    password = PasswordField('password',validators=[InputRequired(message='Password Required'),
    Length(min=8, message='password must be atleast 8 characters')
    ])

    confirm_pwd = PasswordField('confirm_pwd',validators=[InputRequired(message='Password Required'),
    EqualTo('password', message='Password must match')
    ])
    portfolios = SelectField('portfolios',
                choices=[('select', 'Select Ur Portfolio'),
                        ('psd', 'President'),
                        ('vice-psd', 'Vice President'),
                        ('gen-sec', 'General Secretary'),
                        ('fina-sec', 'Financial Secretary'),
                        ('ld-head', 'Ladies Head'),
                        ('org-head', 'Organizing Head'),
                        ('msc-head', 'Music Head'),
                        ('pry-head', 'Prayer Head'),
                        ('evg-head', 'Evangelism Head')
                        ])

    submit_btn = SubmitField('Submit')

    # Custom validation
    # Check if username exists in DB
    def validate_username(self,username):
        username_object = User.query.filter_by(username=username.data).first()
        if username_object:
            raise ValidationError('Username Already Exists in DB. Select a different username')


    #  Check if portfolio exists in DB
    def validate_portfolios(self, portfolios):
        portfolios_object = User.query.filter_by(portfolios=portfolios.data).first()
        if portfolios_object:
            raise ValidationError('Portfolio Already Exists in DB. Select a different portfolio')


# Login Form
class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('username', validators=[InputRequired(message='Username Required')])
    password = PasswordField('password', validators=[InputRequired(message='Password Required'),
               invalid_credentials])
    submit_btn = SubmitField('Login')