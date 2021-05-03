from app import create_app
from config import TestingConfig


if __name__ == '__main__':
	app = create_app(TestingConfig())
	app.run()
