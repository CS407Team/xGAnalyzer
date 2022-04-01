from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

history = Blueprint('history', __name__)


@history.route('/history')
def match_history():
    urls_split = []
    for url in session['urls']:
        print(url)
        print(url.split('match/'))
        urls_split.append(url.split('match/')[1])
    print(urls_split)
    return render_template('history.html', history=session['urls'], current_user=current_user, urls_split=urls_split)


