import os.path as op

from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.contrib.fileadmin import FileAdmin

from app import db, admin
from .models import Post, User, Article, Category


class ArticleModelView(ModelView):
    def create_model(self, form):
        article = Article(title=form.title.data,
                          content=form.content.data,
                          category=form.category.data,
                          meta_description=form.meta_description.data)
        self.session.add(article)
        self._on_model_change(form, article, True)
        self.session.commit()
        self.after_model_change(form, article, True)
        return True

admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ArticleModelView(Article, db.session))
admin.add_view(ModelView(Category, db.session))
path = op.join(op.dirname(__file__), 'static/upload/')
admin.add_view(FileAdmin(path, '/static/upload/', name='Static Files'))
