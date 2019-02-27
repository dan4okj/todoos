import json

from flask_testing import TestCase

from todoapi import (
	create_app,
	db
)
from todoapi.models import User

class BaseFunctionalTestCase(TestCase):

	def create_app(self):
		app = create_app()
		app.config.from_object('todoapi.config.TestingConfig')
		return app

	def setUp(self):
		db.create_all()
		test_user = User('Test', '1234')
		db.session.add(test_user)
		db.session.commit()
		self.wrong_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Mzk3MjIzMTIsIm5iZiI6MTUzOTcyMjMxMiwianRpIjoiYTg4OWM1NDMtZTZjMi00Njg2LTlhNTQtZDgxNjhiOTljNmVmIiwiZXhwIjoxNTM5NzIzMjEyLCJpZGVudGl0eSI6IlRlc3QiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.d-ZLuYRzQO7dLZhXqc9KAJGIzV7cXmO689ylUVJD3gM'

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def login_user(self, username='Test', password='1234'):
		login_resp = self.client.post(
			'/login',
			content_type='application/json',
			data=json.dumps({
				'username': username,
				'password': password,
			})
		)
		return login_resp, json.loads(login_resp.data.decode())

	def logout_user(self, access_token):
		logout_resp = self.client.post(
			'/logout',
			headers={
				'Authorization': 'Bearer {}'.format(access_token)
			},
		)
		return logout_resp

	def add_item(self, access_token, description):
		todo_resp = self.client.post(
			'/todos',
			headers={
				'Authorization': 'Bearer {}'.format(access_token)
			},
			content_type='application/json',
			data=json.dumps({
				'description': description
			})
		)
		return todo_resp, json.loads(todo_resp.data.decode())

	def get_items(self, access_token):
		todo_resp = self.client.get(
			'/todos',
			headers={
				'Authorization': 'Bearer {}'.format(access_token)
			},
		)
		return todo_resp, json.loads(todo_resp.data.decode())

	def get_item(self, access_token, todo_id):
		todo_resp = self.client.get(
			'/todo/{}'.format(todo_id),
			headers={
				'Authorization': 'Bearer {}'.format(access_token)
			},
		)
		return todo_resp, json.loads(todo_resp.data.decode())

	def complete_item(self, access_token, todo_id):

		todo_resp = self.client.put(
			'/todo/{}'.format(todo_id),
			headers={
				'Authorization': 'Bearer {}'.format(access_token)
			},
		)
		return todo_resp, json.loads(todo_resp.data.decode())


	def delete_item(self, access_token, todo_id):

		todo_resp = self.client.delete(
			'/todo/{}'.format(todo_id),
			headers={
				'Authorization': 'Bearer {}'.format(access_token)
			},
		)
		return todo_resp, json.loads(todo_resp.data.decode())

