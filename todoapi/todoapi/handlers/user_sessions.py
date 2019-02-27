from flask import Blueprint
from flask_restful import Api

from todoapi.extensions import jwt
from todoapi.models import TokenBlacklist

from todoapi.handlers.resources.login_resources import (
	Login,
	Logout
)


user_session = Blueprint('user_session', __name__)
api = Api(user_session)
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


@jwt.token_in_blacklist_loader
def is_token_revoked(decrypted_token):
	return TokenBlacklist.is_revoked(decrypted_token['jti'])
