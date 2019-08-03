from flask import Flask, render_template, redirect, url_for, request,flash
from werkzeug.utils import secure_filename
# Helps to login,logout,restrict users to a page,etc
from flask_login import LoginManager, login_user, current_user, logout_user


import os
from forms import *
from models import *


# Configure App
app = Flask(__name__)
app.secret_key = 'secret'

# configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://cktvjbbezjkxui:83313b7459a9e34aca734a4a9110425ef801995356ef9b3ff282a098c8f73582@ec2-174-129-194-188.compute-1.amazonaws.com:5432/d5incue9u4v8nv'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configur flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):

    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
def index():

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        portfolios = form.portfolios.data

        # Hash password
        hashed_pwd = pbkdf2_sha256.hash(password)

        # Add form fields to DB
        user = User(username=username, password=hashed_pwd, portfolios=portfolios)
        db.session.add(user)
        db.session.commit()

        flash('Registered successfully. Please login!', 'success')

        return redirect(url_for('login'))

    return render_template('index.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Allow login if validation succeed
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('report'))

    return render_template('login.html', form=login_form)


# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'ppt', 'pptx'}

# Checks whether file extension is valid / validates file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/report', methods=['GET', 'POST'])
def report():
    # if not current_user.is_authenticated:
    #     flash('Please login!', 'danger')
    #     return redirect(url_for('login'))

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            db_file = File(file_name=file.filename, file_data=file.read())
            db.session.add(db_file)
            db.session.commit()
            return 'File Upload Successful'
        else:
            flash('file extension is not allowed!!!')
            return redirect(request.url)
           

    return render_template('upload_file.html')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))



if __name__ == "__main__":
    app.run(debug=True)