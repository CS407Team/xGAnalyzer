from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return redirect('/')
    data = request.form

    # Perform user check
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return 'User does not exist'
    if user.password != data['password']:
        return 'Incorrect password'

    login_user(user)
    session['username'] = data['username']
    session['urls'] = []
    return render_template('userpage.html', user=data['username'])


@auth.route('/signup', methods=["POST", "GET"])
def signup():
    # TODO: Add actual return pages.
    if request.method == "GET":
        return render_template('signup.html')

    if request.method == "POST":
        data = request.form
        for item in data:
            print(item)
            print(data[item])

        user = User.query.filter_by(username=data['susername']).first()
        if user:
            return 'Username already taken'

        user = User.query.filter_by(email_address=data['semail']).first()
        if user:
            return 'Email already in use'

        newUser = User(username=data['susername'], firstname=data['sfirstname'], lastname=data['slastname'],
                       password=data['spassword'], email_address=data['semail'])

        db.session.add(newUser)
        db.session.commit()
        return 'Successfully Signed up'

        #return render_template('signup.html')


@auth.route('/auth')
def authenticated():
    if current_user.is_authenticated:
        return f'{current_user.username}'
    else:
        return f'{current_user.is_authenticated}'


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')