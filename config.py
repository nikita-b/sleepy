import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'top-secret'

DEBUG_TB_INTERCEPT_REDIRECTS = False  # Debug redicted off

ADMINS = ['nikita@belecky.ru']

POSTS_PER_PAGE = 3
