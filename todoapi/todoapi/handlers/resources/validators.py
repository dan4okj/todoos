from flask_restful import reqparse


def description_type(s):
	if not s:
		raise ValueError('Description can not be empty')
	if len(s) > 128:
		raise ValueError('Description too big, must be =< 128 chars')
	return s


todolist_parser = reqparse.RequestParser()
todolist_parser.add_argument('description', required=True, type=description_type)

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True)
login_parser.add_argument('password', required=True)
