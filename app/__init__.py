import os

from flask import Flask
# from config import basedir

from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.bcrypt import Bcrypt
from flask.ext.migrate import Migrate, MigrateCommand
from flask_debugtoolbar import DebugToolbarExtension

from .momentjs import momentjs

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')
app.jinja_env.globals['momentjs'] = momentjs


db = SQLAlchemy(app)

# bcrypt
bcrypt = Bcrypt(app)

# migrate
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# DebugToolbar

toolbar = DebugToolbarExtension(app)
# LOG DEBUG
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/blog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s \
                                                 [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog statup')



from app import views, models