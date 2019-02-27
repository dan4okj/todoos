from passlib.hash import pbkdf2_sha256 as pwd_hasher

from todoapi.extensions import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(32), index=True, nullable=False)
	password = db.Column(db.String(128), nullable=False)
	todo_items = db.relationship('TodoItem', backref='user', lazy='dynamic')

	def __init__(self, username, password):
		self.username = username
		self.password = self._enc_pwd(password)

	def _enc_pwd(self, pwd):
		return pwd_hasher.hash(pwd)

	def verify_password(self, password):
		return pwd_hasher.verify(password, self.password)

	@classmethod
	def add_todo_item(cls, username, todo_item_desc):
		user = cls.query.filter_by(username=username).one()
		todo_item = TodoItem(todo_item_desc, user.id)
		user.todo_items.append(todo_item)
		db.session.merge(user)
		db.session.commit()
		return todo_item

	@classmethod
	def get_todo_items(cls, username):
		user = cls.query.filter_by(username=username).one()
		return user.todo_items

	@classmethod
	def get_todo_item(cls, username, todo_id):
		user = cls.query.filter_by(username=username).one()
		return user.todo_items.filter_by(id=todo_id).one()

	@classmethod
	def complete_todo_item(cls, username, todo_id):
		todo_item = cls.get_todo_item(username, todo_id)
		todo_item.complete()
		return todo_item

	@classmethod
	def delete_todo_item(cls, username, todo_id):
		todo_item = cls.get_todo_item(username, todo_id)
		db.session.delete(todo_item)
		db.session.commit()


class TodoItem(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	description = db.Column(db.String(128), nullable=False)
	completed = db.Column(db.Boolean, default=False, nullable=False)

	def __init__(self, description, user_id, completed=False):
		self.description = description
		self.user_id = user_id
		self.completed = completed
		db.session.add(self)
		db.session.commit()

	def complete(self):
		self.completed = True
		db.session.add(self)
		db.session.commit()


# Would use something like Redis to store these, but for the purposes of this
# exercise, that should do
class TokenBlacklist(db.Model):
	"""
	List of revoked tokens, usually added by logging out a user
	"""

	id = db.Column(db.Integer, primary_key=True)
	jti = db.Column(db.String(120), nullable=False)

	def __init__(self, token):
		self.jti = token

	def add(self):
		db.session.add(self)
		db.session.commit()

	@classmethod
	def is_revoked(cls, token):
		"""
		Returns:
			bool: True if the token has been revoked
		"""
		qry = cls.query.filter_by(jti=token).first()
		return qry is not None
