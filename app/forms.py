from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField, TextAreaField, StringField
from wtforms.validators import DataRequired


class LoginForm(Form):
    nickname = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SubmitEntry(Form):
    body = TextAreaField('body', [DataRequired()])


class SearchTitle(Form):
    search = StringField('search', [DataRequired()])