from datetime import datetime

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

from app import app, db, lm, bcrypt
from .cfilter import nl2br
from .forms import LoginForm, EditForm, PostForm, RegistrationForm
from .models import User, Post, Article
from config import POSTS_PER_PAGE


###REMOVE
import re
from jinja2 import evalcontextfilter, Markup, escape
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
###REMOVE



@app.route('/')
def index():
    #posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    posts = Post.query.order_by(Post.id.desc()).limit(10).all()
    return render_template('index.html', title = 'Новые сны',
    posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(request.args.get("next") or url_for("index"))
        flash('К сожалению такого пользователя нет в нашей базе данных :(')
    return render_template('login.html', title='Зайти в свой дневник', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(email=form.email.data, password=form.password.data, nickname=form.nickname.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Спасибо за регистрацию!')
        return redirect(request.args.get("next") or url_for("index"))
    return render_template('register.html', form=form, title='Создание своего дневника :)')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<nickname>/<int:page>')
@app.route('/user/<nickname>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('Пользователь %s не существует.' % nickname)
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    user = User.query.filter_by(nickname=g.user.nickname).first()
    return render_template('editProfile.html', form=form, user=user)

@app.route('/dream/add', methods=['GET', 'POST'])
def add_dream():
    form = PostForm(request.form)

    if form.validate_on_submit():
        if g.user.is_authenticated():
            author = g.user
        else:
            author = User.query.filter_by(id=0).first()
        post = Post(description=form.description.data, timestamp=datetime.utcnow(), author=author, datesleep=form.datesleep.data, rating=0)
        db.session.add(post)
        db.session.commit()
        flash('Ваш сон опубликован, спасибо!')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\t follow youself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))


@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))


@app.route('/dream/<int:num>')
def dream(num):
    dream = Post.query.filter_by(id=int(num)).first()
    if dream == None:
        flash('Сна с номером #%s не существует :(' % num)
        return redirect(url_for('index'))
    return render_template('dream.html', dream=dream)

@app.route('/article/<int:num>')
def article(num):
    article = Article.query.filter_by(id=int(num)).first()
    if article == None:
        flash('Такой статьи не существует')
        return redirect(url_for('index'))
    return render_template('article.html', article)