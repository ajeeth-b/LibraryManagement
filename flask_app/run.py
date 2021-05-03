from app import create_app
from config import DebugConfig


if __name__ == '__main__':
	app = create_app(DebugConfig())
	app.run()
