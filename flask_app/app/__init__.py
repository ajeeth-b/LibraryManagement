from flask import Flask


def create_app(config):
	app = Flask(__name__)
	app.config.from_object(config)

	with app.app_context():

		from .library import library as library_blueprint
		app.register_blueprint(library_blueprint)

		from .authentication import auth as auth_blueprint, login_required
		app.register_blueprint(auth_blueprint)

		from .user import user_blueprint
		app.register_blueprint(user_blueprint)

	return app
