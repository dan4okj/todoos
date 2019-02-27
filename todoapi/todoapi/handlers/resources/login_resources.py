from flask_restful import Resource

from flask_jwt_extended import (
	create_access_token,
	get_raw_jwt,
	jwt_required
)

from todoapi.models import (
	TokenBlacklist,
	User,
)
from todoapi.handlers.resources.validators import login_parser


class Login(Resource):

	def post(self):
		data = login_parser.parse_args()

		current_user = User.query.filter_by(username=data['username']).first()
		if not current_user:
			message = 'User {} does not exist'.format(data['username'])
			return {'message': message}, 401
		if not current_user.verify_password(data['password']):
			return {'message': 'Wrong credentials'}, 401

		access_token = create_access_token(identity=current_user.username)

		return {
				'message': 'Successfully logged in',
				'access_token': access_token,
		}


class Logout(Resource):

	@jwt_required
	def post(self):
		jti = get_raw_jwt()['jti']

		try:
			TokenBlacklist(jti).add()
		except Exception:
			return {'message': 'Something went wrong'}

		return {'message': 'Successfully logged out'}
