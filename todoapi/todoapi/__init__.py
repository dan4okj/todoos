import os

from flask import Flask

from todoapi.extensions import (
	db,
	jwt
)

from todoapi.handlers.user_sessions import is_token_revoked


def create_app(script_info=None):

	app = Flask(__name__)

	# Set config
	app.config.from_object(os.getenv('APP_SETTINGS'))

	# Init extensions
	db.init_app(app)
	jwt.init_app(app)

	# Register blueprints
	from todoapi.handlers.user_sessions import user_session
	from todoapi.handlers.todos import todos
	app.register_blueprint(user_session)
	app.register_blueprint(todos)

	@app.shell_context_processor
	def ctx():
		return {'app': app, 'db': db}

	return app
