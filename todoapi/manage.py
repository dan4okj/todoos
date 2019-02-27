import unittest
import sys
from flask.cli import FlaskGroup

from todoapi import create_app
from todoapi.models import (
	TodoItem,
	TokenBlacklist,
	User
)
from todoapi.extensions import db


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command()
def recreate_db():
	db.drop_all()
	db.create_all()
	db.session.commit()


@cli.command()
def create_test_user():
	test_user = User('Test', '1234')
	db.session.add(test_user)
	db.session.commit()


@cli.command()
def test():
	sys.path.append('./todoapi')
	tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
	result = unittest.TextTestRunner(verbosity=2).run(tests)
	if result.wasSuccessful():
		return 0
	return 1


if __name__ == '__main__':
	cli()
