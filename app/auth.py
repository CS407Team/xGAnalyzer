from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return redirect('/')
    data = request.form
    print(data['username'])
    print(data['password'])
    for item in data:
        print(item)
    print(data['remember'])

    # Perform user check
    return f'User not found'
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return 'user does not exist'

    login_user(user)
    return render_template('userpage.html', user=data['username'])


@auth.route('/signup', methods=["POST", "GET"])
def signup():
    # TODO: other stuff with adding users to database
    if request.method == "GET":
        return render_template('signup.html')

    if request.method == "POST":
        return render_template('signup.html')


@auth.route('/auth')
def authenticated():
    if current_user.is_authenticated:
        return f'{current_user.name}'
    else:
        return f'{current_user.is_authenticated}'
