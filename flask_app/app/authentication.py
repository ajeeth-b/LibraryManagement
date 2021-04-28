from flask import Blueprint, render_template, session, request, redirect, current_app as app, g
from .user_manager import get_user_as_dict, create_user
from werkzeug.security import check_password_hash


def login_required(func):
	def wrapper(*args, **kwargs):
		user = g.get('user', None)
		if (user is None) or ('email' not in user) or ('name' not in user) or ('member_id' not in user):
			return redirect('/login')
		return func(*args, **kwargs)
	return wrapper


@app.before_request
def before_request():
	g.user = session.get('session', None)


auth = Blueprint('authentication', __name__)


@auth.route('/login', methods=['GET'])
def get_login_page():
	return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_user():
	email = request.form.get('email', None)
	password = request.form.get('password', None)

	if email is None or password is None:
		return render_template('login.html', message='Email and Password are required')

	user = get_user_as_dict(email)
	if user is None:
		return render_template('login.html', message='No such user.')

	if not check_password_hash(user['password'],password):
		return render_template('login.html', message='Incorrect Password.')


	del user['password']
	session['session'] = user

	return redirect('/')

@auth.route('/signup', methods=['GET'])
def get_signup_page():
	return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup():
	email = request.form.get('email', None)
	name = request.form.get('name', None)
	password = request.form.get('password', None)

	if email is None or password is None or name is None:
		return render_template('signup.html', message='Email, Name and Password are required*')

	user = get_user_as_dict(email)
	if user:
		return render_template('signup.html', message='Email already exists.')

	user = create_user(email, name, password)

	del user['password']
	session['session'] = user

	return redirect('/')