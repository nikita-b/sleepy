from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, SelectField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, InputRequired, Length, Email, Optional
from wtforms.fields.html5 import DateField


class LoginForm(Form):
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(min=6)],
                             widget=PasswordInput())


class RegistrationForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('Password',
                             validators=[InputRequired(), Length(min=6)],
                             widget=PasswordInput())


class EditForm(Form):
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    password = PasswordField('Password')
    email = StringField('email', validators=[InputRequired(), Email()])
    first_name = StringField('email')
    last_name = StringField('email')
    anonymous = BooleanField('Anonymous', default=False)


class PostForm(Form):
    description = TextAreaField('description')
    datesleep = DateField('datesleep', format='%Y/%m/%d')
    anonymously = BooleanField('Anonymously', default=False)
    yourself = BooleanField('checked', default=True)


# Admin

class ArticleAddForm(Form):
    title = StringField('Title')
    content = TextAreaField('Text')
    category = SelectField('Category', coerce=int, validators=[Optional()])


class CategoryAddForm(Form):
    name = StringField('Name')
