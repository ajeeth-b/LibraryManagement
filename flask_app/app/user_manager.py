from .models import User, Member
from .utils import with_client_context
from werkzeug.security import generate_password_hash
from google.cloud.ndb.exceptions import BadValueError


class UserAlreadyExists(Exception):
	pass


class UserNotFound(Exception):
	pass


@with_client_context
def create_user(email, name, password):
	if type(email) != str or type(name) != str or type(password) != str:
		raise BadValueError()
	if User.get_by_id(email):
		raise UserAlreadyExists()

	member = Member(name=name)
	member.put()

	user = User(id=email, name=name, password=generate_password_hash(password), member_id=member.key)
	user.put()

	return user.get_dict()


@with_client_context
def get_user(email):
	user = User.get_by_id(email)
	if user is None:
		raise UserNotFound()
	return user.get_dict()


@with_client_context
def delete_user(email):
	user = User.get_by_id(email)
	if user is None:
		raise UserNotFound()
	member = Member.get_by_id(user.member_id.id())
	user.key.delete()
	if member:
		member.key.delete()
