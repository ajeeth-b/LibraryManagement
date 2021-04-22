from flask import Flask
from .config import TestingConfig


def create_app():
	app = Flask(__name__)
	app.config.from_object(TestingConfig())

	with app.app_context():
		from .library import library as library_blueprint

		app.register_blueprint(library_blueprint)

	return app