from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

history = Blueprint('history', __name__)


@history.route('/history')
def match_history():
    for url in session['urls']:
        print(url)
    return f'{session["urls"]}'


