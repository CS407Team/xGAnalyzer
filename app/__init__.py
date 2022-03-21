from flask import Flask, redirect, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    connection = "mysql+pymysql://{0}:{1}@{2}/{3}".format('root', 'V3z?RnzC', '35.225.215.107',
                                                          'analyzer')
    app.config['SQLALCHEMY_DATABASE_URI'] = connection
    app.url_map.strict_slashes = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .models import User

    @login_manager.user_loader
    def load_user(userid):
        return User.query.get(int(userid))

    @app.before_request
    def clear_trailing():
        rp = request.path
        if rp != '/' and rp.endswith('/'):
            return redirect(rp[:-1])

    return app


