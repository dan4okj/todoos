import json
import unittest

from tests.base import BaseFunctionalTestCase


class TestUserLogin(BaseFunctionalTestCase):

	def test_login(self):
		login_resp, data = self.login_user()
		self.assertEqual(login_resp.status_code, 200)
		self.assertIsNotNone(data['access_token'])

	def test_login_user_twice(self):
		login_resp_1, data_1 = self.login_user()
		login_resp_2, data_2 = self.login_user()
		self.assertEqual(login_resp_2.status_code, 200)
		self.assertNotEqual(data_1['access_token'], data_2['access_token'])

	def test_login_no_username(self):
		response = self.client.post(
			'/login',
			content_type='application/json',
			data=json.dumps({
				'password': '1234'
			})
		)
		data = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)

	def test_login_no_password(self):
		response = self.client.post(
			'/login',
			content_type='application/json',
			data=json.dumps({
				'username': '1234'
			})
		)
		data = json.loads(response.data.decode())
		self.assertEqual(response.status_code, 400)

	def test_wrong_username(self):
		login_resp, data = self.login_user(username='BananaUser')
		self.assertEqual(login_resp.status_code, 401)
		self.assertNotIn('access_token', data)

	def test_wrong_password(self):
		login_resp, data = self.login_user(password='BananaPassword')
		self.assertEqual(login_resp.status_code, 401)
		self.assertNotIn('access_token', data)


class TestUserLogout(BaseFunctionalTestCase):

	def test_logout(self):
		_, data = self.login_user()
		logout_resp = self.logout_user(data['access_token'])
		self.assertEqual(logout_resp.status_code, 200)

	def test_logout_no_token(self):
		logout = self.client.post('/logout')
		self.assertEqual(logout.status_code, 401)

	def test_logout_wrong_token(self):
		logout_resp = self.logout_user('Bananahash')
		self.assertEqual(logout_resp.status_code, 422)

	def test_logout_twice_same_token(self):
		_, data = self.login_user()
		self.logout_user(data['access_token'])
		second_resp = self.logout_user(data['access_token'])
		self.assertEqual(second_resp.status_code, 401)
