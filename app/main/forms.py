#!/usr/bin/env python
# coding:utf8

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(Form):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired()])
    submit = SubmitField(u'Login')


class RegisterForm(Form):
    username = StringField(u'Username', validators=[DataRequired()])
    password = PasswordField(u'Password', validators=[DataRequired(), EqualTo('password_confirm', message=u'两次密码不匹配')])
    password_confirm = PasswordField(u'密码(确认)')
    submit = SubmitField()
