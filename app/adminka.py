import os.path as op

from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin

from app import db, admin
from .models import Post, User, Article, Category

admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Article, db.session))
admin.add_view(ModelView(Category, db.session))
path = op.join(op.dirname(__file__), 'static/upload/')
admin.add_view(FileAdmin(path, '/static/upload/', name='Static Files'))
