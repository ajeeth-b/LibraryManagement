import pytest
from config import TestConfig
from app.user_manager import *
from random import randint



def get_random_name(size=7):
	chars = map(chr, [randint(97, 122) for i in range(size)])
	return ''.join(chars)

@pytest.mark.skip
@pytest.mark.user_manager
class TestUser():

	def test_create_and_delete_user(self):
		user_mail = get_random_name()+'@gmail.com'

		user = create_user(user_mail, get_random_name(), get_random_name())

		assert user['email'] == user_mail

		''' verifying a member is created for user'''
		assert 'member_id' in user

		''' creating another user with same email '''
		with pytest.raises(UserAlreadyExists):
			create_user(user_mail, get_random_name(), get_random_name())


		''' deleting user'''
		delete_user(user_mail)

		''' deleting the non existing user'''
		with pytest.raises(UserNotFound):
			delete_user(user_mail)

