from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

import os
from flask.ext.login import LoginManager
from config import basedir

app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config')
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
db = SQLAlchemy(app)

from app import views, models
