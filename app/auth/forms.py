#coding:utf-8

__author__ = 'eric'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Length(1,64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住密码')
    submit = SubmitField(u'登录')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码', validators=[Required()])
    password = PasswordField(u'新密码', validators=[Required(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'确定')


class ResetPasswordRequestForm(Form):
    email = StringField(u'邮件', validators=[Required(),Length(1,64), Email()])
    submit = SubmitField(u'确定')

    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Unknown Email.')


class ResetPasswordForm(Form):
    email = StringField(u'邮件', validators=[Required(),Length(1,64), Email()])
    password = PasswordField(u'密码', validators=[Required(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField(u'确认密码', validators=[Required()])
    submit = SubmitField(u'确认')

    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Unknown Email')

class ChangeEmailRequestForm(Form):
    email = StringField(u'邮件', validators=[Required(),Length(1,64), Email()])
    password = PasswordField(u'密码', validators=[Required()])
    submit = SubmitField(u'确认')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
