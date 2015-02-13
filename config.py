import os
basedir = os.path.abspath(os.path.dirname(__file__))

USER_DATABASE = 'nikita'
PASS_DATABASE = '123'
NAME_DATABASE = 'testdb'

SQLALCHEMY_DATABASE_URI = 'postgresql://%s:%s@localhost/%s' % (USER_DATABASE,
                                                               PASS_DATABASE,
                                                               NAME_DATABASE)

WTF_CSRF_ENABLED = True
SECRET_KEY = 'top-secret'

DEBUG_TB_INTERCEPT_REDIRECTS = False  # Debug redicted off

ADMINS = ['nikita@belecky.ru']

POSTS_PER_PAGE = 3
