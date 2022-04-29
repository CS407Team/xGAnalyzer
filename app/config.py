from flask import Flask

UPLOAD_FOLDER = 'static/uploads/'

appl = Flask(__name__)
appl.secret_key = "secret key"
appl.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
appl.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024