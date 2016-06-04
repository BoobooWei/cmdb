__author__ = 'eric'


from .import api
from flask import jsonify, g
from .errors import forbidden, unauthorized
from ..models import User
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@api.route('/token')
def get_token():
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})


@auth.verify_password
def verify_password(email_or_token,password):
    if email_or_token and password:
        user = User.query.filter_by(email=email_or_token).first()
        if not user:
            return False
        g.current_user = user
        return user.verify_password(password)
    if email_or_token and not password:
        g.current_user = User.verify_auth_token(email_or_token)
        return g.current_user is not None



# @auth.verify_password
# def verify_password(email_or_token, password):
#     if email_or_token == '':
#         g.current_user = AnonymousUser()
#         return True
#     if password == '':
#         g.current_user = User.verify_auth_token(email_or_token)
#         g.token_used = True
#         return g.current_user is not None
#     user = User.query.filter_by(email=email_or_token).first()
#     if not user:
#         return False
#     g.current_user = user
#     g.token_used = False
#     return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')




@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


