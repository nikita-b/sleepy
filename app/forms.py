from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, PasswordField, validators
from wtforms.validators import DataRequired, InputRequired, Length, Email
from wtforms.fields.html5 import DateField

class LoginForm(Form):
    email = StringField('email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired(), Length(min=6)])


class RegistrationForm(Form):
    nickname = StringField('nickname', validators = [InputRequired()])
    email = StringField('email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired(), Length(min=6)])


class EditForm(Form):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname


    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).firts()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one')
            return False
        return True

class PostForm(Form):
    description = TextAreaField('description')
    datesleep = DateField('datesleep', format='%Y/%m/%d')
