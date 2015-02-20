from app import db
from app import bcrypt

from .utils import translate_url

from datetime import datetime


from flask.ext.login import current_user


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )

votes = db.Table('votes',
                 db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                 )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nickname = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    anonymous = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, nickname, password, email):
        self.nickname = nickname
        self.password = bcrypt.generate_password_hash(password)
        self.email = email

    def is_private(self, user):
        if self.anonymous and (self != user):
            return True

    def is_admin(self):
        return self.id == 1

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)) \
                                            .filter(followers.c.follower_id == self.id) \
                                            .order_by(Post.timestamp.desc())

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.Text)
    datesleep = db.Column(db.DateTime)
    rating = db.Column(db.Integer)
    anonymously = db.Column(db.Boolean, default=False)
    yourself = db.Column(db.Boolean, default=True)
    votes = db.relationship('User', secondary=votes, backref=db.backref('bposts', lazy='dynamic'))

    def voteup(self, user):
        if not self.is_voted(user):
            self.votes.append(user)
            return self

    def votedown(self, user):
        if self.is_voted(user):
            self.votes.remove(user)
            return self

    def is_voted(self, user):
        return user in self.votes

    def voted(self):
        return len(self.votes)

    def __repr__(self):
        return '<Dream %r>' % (self.id)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    url = db.Column(db.String(180), unique=True, nullable=False)
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('article', lazy='dynamic'))
    views = db.Column(db.Integer, default=0)

    def __init__(self, title, content, category):
        self.title = title
        self.url = translate_url(title)
        self.category = category
        self.content = content

    def inc_views(self):
        self.views += 1

    def __repr__(self):
        return '<%s>' % (self.title)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<%s>' % (self.name)


# class MyView(ModelView):
#     def is_accessible(self):
#         return current_user.is_admin()


# class MyFileView(FileAdmin):
#     def is_accessible(self):
#         return current_user.is_admin()


# class IndexAdmin(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('index.html')

#     def is_accessible(self):
#         return current_user.is_admin()


# MODELS ADMIN
