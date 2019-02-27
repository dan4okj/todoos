from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

#from todoapi.models import TokenBlacklist


# App's Extension
db = SQLAlchemy()
jwt = JWTManager()

@jwt.token_in_blacklist_loader
def is_token_revoked(decrypted_token):
	return TokenBlacklist.is_revoked(decrypted_token['jti'])

