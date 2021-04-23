from .models import User, Member
from .utils import with_client_context
from uuid import uuid4
from werkzeug.security import generate_password_hash


@with_client_context
def create_user(email, name, password):
	if User.get_by_id(email):
		return False

	member_id = str(uuid4())
	member = Member(id= member_id, name=name)
	member.put()

	user = User(id=email, name=name, password=generate_password_hash(password), member_id=member_id)
	user.put()

	return user_to_dict(user)


@with_client_context
def get_user(email):
	return User.get_by_id(email)


def user_to_dict(user):
	user_dict = user.to_dict()
	user_dict.update({'email':user.key.id()})
	return user_dict

def get_user_as_dict(email):
	user = get_user(email)
	if user is None:
		return None
	return user_to_dict(user)


@with_client_context
def delete_user(email):
	user = User.get_by_id(email)
	if user:
		user.key.delete()
		return True
	return False

