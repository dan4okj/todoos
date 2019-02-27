from flask_restful import (
	Resource,
	fields,
	marshal_with
)
from flask_jwt_extended import (
	jwt_required,
	get_jwt_identity
)

from todoapi.models import (
	User,
	TodoItem
)
from todoapi.handlers.resources.validators import todolist_parser

todolist_fields = {
	'message': fields.String
}


class Todo(Resource):

	@jwt_required
	def get(self, todo_id):
		username = get_jwt_identity()
		todo_item = User.get_todo_item(username, todo_id)
		return {
			'todoitem': {
				'id': todo_item.id,
				'description': todo_item.description,
				'is_completed': todo_item.completed,
			}
		}


	@jwt_required
	def put(self, todo_id):
		username = get_jwt_identity()
		todo_item = User.complete_todo_item(username, todo_id)
		return {
			'todoitem': {
				'id': todo_item.id,
				'description': todo_item.description,
				'is_completed': todo_item.completed,
			}
		}

	@jwt_required
	def delete(self, todo_id):
		username = get_jwt_identity()
		todo_item = User.delete_todo_item(username, todo_id)
		return {
			'deleted': {
				'todoitem': {
					'id': todo_id,
				}
			}
		}


class TodoList(Resource):

	@jwt_required
	@marshal_with(todolist_fields)
	def post(self):
		username = get_jwt_identity()
		data = todolist_parser.parse_args()
		todo_item = User.add_todo_item(username, data['description'])
		return {
			'todoitem': {
				'id': todo_item.id,
				'description': todo_item.description,
				'is_completed': todo_item.completed,
			}
		}



	@jwt_required
	def get(self):
		username = get_jwt_identity()
		try:
			todo_items = User.get_todo_items(username)
			response = {
				'message': '{}\'s Todo list'.format(username),
				'todolist': {
					'incomplete': [],
					'completed': []
				 }
			}
			for todo_item in todo_items:
				todo_item_resp = {
					'id': todo_item.id,
					'description': todo_item.description,
				}
				if todo_item.completed:
					response['todolist']['completed'].append(todo_item_resp)
				else:
					response['todolist']['incomplete'].append(todo_item_resp)
		except:
			return {'message': 'Something went wrong'}, 500
		return response
