from app import db
from app import bcrypt

from datetime import datetime

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

    def isPrivate(self, user):
        if self.anonymous and (self != user):
            return True

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
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

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
    votes = db.relationship('User', secondary=votes, backref=db.backref('bposts', lazy='dynamic'))
    anonymously = db.Column(db.Boolean, default=False)
    yourself = db.Column(db.Boolean, default=True)


    def limit_description(self, limit):
        if len(self.description) > limit:
            return self.description[:limit] + '...'
        return self.description

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
    title = db.Column(db.String(180))
    text = db.Column(db.Text)
