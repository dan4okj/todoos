from flask import Blueprint
from flask_restful import Api

from todoapi.handlers.resources.todos_resources import (
	Todo,
	TodoList
)

todos = Blueprint('todos', __name__)
api = Api(todos)

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todo/<string:todo_id>')
