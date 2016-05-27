#coding:utf-8

__author__ = 'eric'

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(),Length(1,64), Email()])
    username = StringField('Username', validators=[Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only letters, number, dots or underscores')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
    def validate_username(self, field):
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Username already registered')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old Password', validators=[Required()])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField(u'确定')


class ResetPasswordRequestForm(Form):
    email = StringField('Email', validators=[Required(),Length(1,64), Email()])
    submit = SubmitField(u'确定')

    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Unknown Email.')


class ResetPasswordForm(Form):
    email = StringField('Email', validators=[Required(),Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField(u'确认')

    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Unknown Email')

class ChangeEmailRequestForm(Form):
    email = StringField('Email', validators=[Required(),Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField(u'确认')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')
