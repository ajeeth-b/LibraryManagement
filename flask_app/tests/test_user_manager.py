import pytest
import mock
from app.user_manager import *
from app.models import User
from google.cloud.ndb.exceptions import BadValueError



def test_create_user(mocker):


	mocker_query_count = mocker.patch('google.cloud.ndb.query.Query.count', return_value=0)
	mocker_model_put = mocker.patch('google.cloud.ndb.Model.put')
	mocker_user_get_dict = mocker.patch('app.models.User.get_dict', return_value = {'name':'name', "email":'emaiil'})

	# Testing by creating duplicate user
	mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=User())
	with pytest.raises(UserAlreadyExists):
		create_user('email', 'name', 'password')

	# testing for creating valid user
	mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=None)
	try:
		create_user('name', 'email', 'password')
		assert True
	except Exception as e:
		pytest.fail('Error in creating a valid user '+str(e))

	# Testing by giving bad value
	with pytest.raises(BadValueError):
		create_user('email', 'name', 1)
	with pytest.raises(BadValueError):
		create_user('email', 1, 'password')
	with pytest.raises(BadValueError):
		create_user(1, 'name', 'password')



def test_get_user(mocker):
	mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=None)
	mocker_user_get_dict = mocker.patch('app.models.User.get_dict', return_value = {'name':'name', "email":'emaiil'})
	with pytest.raises(UserNotFound):
		get_user('email@e.com')


def test_delete_user(mocker):
	mocker_model_get_by_id = mocker.patch('google.cloud.ndb.Model.get_by_id', return_value=None)
	mocker_user_get_dict = mocker.patch('app.models.User.get_dict', return_value = {'name':'name', "email":'emaiil'})
	with pytest.raises(UserNotFound):
		delete_user('email@e.com')