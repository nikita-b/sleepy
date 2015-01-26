from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, PasswordField
from wtforms.widgets import PasswordInput
from wtforms.validators import DataRequired, InputRequired, Length, Email
from wtforms.fields.html5 import DateField


class LoginForm(Form):
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)], widget=PasswordInput())


class RegistrationForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    email = StringField('email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)], widget=PasswordInput())


class EditForm(Form):
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)], widget=PasswordInput())
    email = StringField('email', validators=[InputRequired(), Email()])
    first_name = StringField('email', validators=[InputRequired()])
    last_name = StringField('email', validators=[InputRequired()])


class PostForm(Form):
    description = TextAreaField('description')
    datesleep = DateField('datesleep', format='%Y/%m/%d')
    anonymously = BooleanField(False)
    yourself = BooleanField('checked', default=True)
