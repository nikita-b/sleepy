from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm, bcrypt
from .cfilter import nl2br
from .forms import LoginForm, EditForm, PostForm, RegistrationForm, ArticleAddForm, CategoryAddForm
from .models import User, Post, Article, Category
from config import POSTS_PER_PAGE


@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    posts = Post.query.filter_by(yourself=False,
                                 anonymously=False) \
                                .order_by(Post.id.desc()).paginate(page, POSTS_PER_PAGE, True)
    return render_template('index.html', title='Новые сны', posts=posts)


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
    u = User.query.filter_by(nickname=form.nickname.data).first()
    if u:  # if username is exist
        flash('Такое имя пользователя уже сущесвует. Попробуйте выбрать другое.')

    u2 = User.query.filter_by(email=form.email.data).first()
    if u2:
        flash('Пользователь с таким e-mail уже зарегистрирован. \
            Если это вы, то восстановите пароль.')

    if (not u) and (not u2) and request.method == 'POST' and form.validate():
        user = User(email=form.email.data,
                    password=form.password.data,
                    nickname=form.nickname.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Спасибо за регистрацию! Вы сразу можете пользоваться своим дневником.')
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
    if user is None:
        flash('Пользователь %s не существует.' % nickname)
        return redirect(url_for('index'))
    if user.isPrivate(g.user):
        flash('К сожалению профиль данного пользователя приватный :(')
        return redirect(url_for('index'))
    posts = user.posts.order_by(Post.id.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(request.form)
    if form.validate_on_submit():
        g.user.about_me = form.about_me.data
        g.user.email = form.email.data
        g.user.last_name = form.last_name.data
        g.user.first_name = form.first_name.data
        g.user.anonymous = form.anonymous.data
        db.session.add(g.user)
        db.session.commit()
        flash('Изменения профиля сохранены')
        return redirect(url_for('edit'))
    form.first_name.data = g.user.first_name
    form.last_name.data = g.user.last_name
    form.email.data = g.user.email
    form.about_me.data = g.user.about_me
    form.anonymous.data = g.user.anonymous
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
        post = Post(description=form.description.data,
                    timestamp=datetime.utcnow(),
                    author=author,
                    datesleep=form.datesleep.data,
                    anonymously=form.anonymously.data,
                    yourself=form.yourself.data)
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


@app.route('/dream/<int:num>/up')
@login_required
def voteup(num):
    post = Post.query.filter_by(id=num).first()
    p = post.voteup(current_user)
    if p is None:
        flash('Вы уже голосовали!')
        return redirect(url_for('index'))  # Add other redirect
    db.session.add(p)
    db.session.commit()
    flash('Спасибо за ваш голос!')
    return redirect(url_for('index'))


@app.route('/dream/<int:num>/down')
@login_required
def votedown(num):
    post = Post.query.filter_by(id=num).first()
    p = post.votedown(current_user)
    if p is None:
        flash('Вы еще не голосовали!')
        return redirect(url_for('index'))  # Add other redirect
    db.session.add(p)
    db.session.commit()
    flash('Ваш голос удален!')
    return redirect(url_for('index'))


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
    if dream is None:
        flash('Сна с номером #%s не существует :(' % num)
        return redirect(url_for('index'))
    return render_template('dream.html', dream=dream)


@app.route('/article')
def list_article():
    list_article = Article.query.all()
    return render_template('list_article.html', lst=list_article)


@app.route('/article/<title>')
def article(title):
    article = Article.query.filter_by(url=title).first()
    allarticle = Article.query.order_by(Article.id.desc()).all()
    article.inc_views()
    db.session.add(article)
    db.session.commit()
    if article is None:
        flash('Такой статьи не существует')
        return redirect(url_for('index'))
    return render_template('article.html', article=article, all=allarticle)


# ADMIN ARTICLE

@app.route('/admin/add')
def admin_add():
    category = Category.query.all()
    formArticle = ArticleAddForm()
    formArticle.category.choices = [(c.id, c.name) for c in category]
    return render_template('admin_article.html',
                           formArticle=formArticle,
                           formCategory=CategoryAddForm())


@app.route('/admin/add/category', methods=['POST'])
def admin_add_category():
    category_form = CategoryAddForm(request.form)

    if category_form.validate_on_submit():
        category = Category(name=category_form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Успешно')
        return redirect(url_for('admin_add'))


@app.route('/admin/add/article', methods=['POST'])
def admin_add_article():
    category = Category.query.all()
    form = ArticleAddForm(request.form)
    form.category.choices = [(c.id, c.name) for c in category]
    if form.validate_on_submit():
        article = Article(title=form.title.data,
                          content=form.content.data,
                          category=Category.query.filter_by(id=form.category.data).first())
        db.session.add(article)
        db.session.commit()
        flash('Статья опубликована')
        return redirect(url_for('admin_add'))
    flash('Ошибка заполнения')
    return redirect(url_for('admin_add'))
