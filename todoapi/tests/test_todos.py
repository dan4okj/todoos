import json
import unittest

from todoapi.models import User
from tests.base import BaseFunctionalTestCase


class LoggedInFunctionalTestCase(BaseFunctionalTestCase):

	def setUp(self):
		super(LoggedInFunctionalTestCase, self).setUp()
		_, data = self.login_user()
		self.access_token = data['access_token']

	def add_test_todo_to_db(self, description, user='Test'):
		return User.add_todo_item(user, description)


class TestTodoListPost(LoggedInFunctionalTestCase):

	def test_insert_todo_item(self):
		resp, todo_d = self.add_item(self.access_token, 'Eat bananas')
		self.assertEqual(resp.status_code, 200)

	def test_insert_128_char_description(self):
		resp, data = self.add_item(
			self.access_token,
			''.join(['Eat ', '0' * 116, ' bananas'])
		)
		self.assertEqual(resp.status_code, 200)

	def test_insert_todo_name_too_long(self):
		resp, data = self.add_item(
			self.access_token,
			'Eat 10000000000000000000000000000000000000000000000000000000000' + \
			'000000000000000000000000000000000000000000000000000000000000000' + \
			'000000000000000000000000000000000000000000000000000000000000000' + \
			'Bananas'
		)
		self.assertEqual(resp.status_code, 400)

	def test_insert_empty_description(self):
		resp, data = self.add_item(
			self.access_token,
			''
		)
		self.assertEqual(resp.status_code, 400)

	def test_insert_no_description(self):
		todo_resp = self.client.post(
			'/todos',
			headers={
				'Authorization': 'Bearer {}'.format(self.access_token)
			}
		)
		self.assertEqual(todo_resp.status_code, 400)


class TestTodoListPostUnauth(BaseFunctionalTestCase):

	def test_insert_todo_item_with_no_auth(self):
		todo_resp = self.client.post(
			'/todos',
			data=json.dumps({
				'description': 'Eat bananas'
			})
		)
		self.assertEqual(todo_resp.status_code, 401)

	def test_insert_todo_item_with_non_existing_token(self):
		resp, data = self.add_item(self.wrong_token, 'Eat Bananas')
		self.assertEqual(resp.status_code, 401)


class TestTodoListGet(LoggedInFunctionalTestCase):
	def test_get_todo_items(self):
		todo = self.add_test_todo_to_db('Eat bananas')

		resp, todos_data = self.get_items(self.access_token)
		expected = {
			'message': "Test's Todo list",
		 	'todolist': {
				'incomplete': [
					{'id': todo.id, 'description': 'Eat bananas'}
				],
				'completed': [],
				}
		}
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(todos_data, expected)


class TestTodoGet(LoggedInFunctionalTestCase):

	def test_get_one_todo_item(self):
		todo = self.add_test_todo_to_db('Eat bananas')

		resp, todo_data = self.get_item(self.access_token, todo.id)
		expected = {
			'todoitem': {
				'id': todo.id,
				'description': 'Eat bananas',
				'is_completed': False
			}
		}
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(todo_data, expected)


class TestTodoPut(LoggedInFunctionalTestCase):

	def test_complete_todo_item(self):
		todo = self.add_test_todo_to_db('Eat bananas')

		resp, todo_data = self.complete_item(self.access_token, todo.id)
		expected = {
			'todoitem': {
				'id': todo.id,
				'description': 'Eat bananas',
				'is_completed': True
			}
		}
		self.assertEqual(resp.status_code, 200)
		self.assertEqual(todo_data, expected)


class TestTodoDelete(LoggedInFunctionalTestCase):

	def test_delete_todo_item(self):
		todo = self.add_test_todo_to_db('Eat bananas')
		resp, todo_data = self.delete_item(self.access_token, todo.id)
