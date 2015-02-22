import os

from flask import Flask

from flask.ext.admin import Admin
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel
from flask.ext.script import Manager
from flask.ext.bcrypt import Bcrypt
from flask.ext.migrate import Migrate, MigrateCommand
from flask_debugtoolbar import DebugToolbarExtension

from .momentjs import momentjs

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, instance_relative_config=True)

app.config.from_object('config')
app.config.from_pyfile('config.py')
app.jinja_env.globals['momentjs'] = momentjs


db = SQLAlchemy(app)

# bcrypt
bcrypt = Bcrypt(app)

# admin
admin = Admin(app, name='Sheephappens')

# migrate
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# babel
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'

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
    file_handler = RotatingFileHandler(basedir + '/tmp/sleep.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s \
                                                 [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog statup')

from app import views, models, adminka