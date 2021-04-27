from .models import User, Member
from .utils import with_client_context
from uuid import uuid4
from werkzeug.security import generate_password_hash


@with_client_context
def create_user(email, name, password):
	if User.get_by_id(email):
		return False

	member = Member(name=name)
	member.put()

	user = User(id=email, name=name, password=generate_password_hash(password), member_id=member.key.id())
	user.put()

	return {**user.to_dict(), **{'email':user.key.id()}}


@with_client_context
def get_user(email):
	return User.get_by_id(email)


def get_user_as_dict(email):
	user = get_user(email)
	if user is None:
		return None
	return {**user.to_dict(), **{'email':user.key.id()}}


@with_client_context
def delete_user(email):
	user = User.get_by_id(email)
	if user:
		user.key.delete()
		return True
	return False
