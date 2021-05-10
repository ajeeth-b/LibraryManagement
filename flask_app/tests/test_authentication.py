import pytest
import mock
from app.user_manager import *


def test_get_login_page(app):
	resp = app.get('/login')
	assert resp.status_code == 200


def test_get_signup_page(app):
	resp = app.get('/signup')
	assert resp.status_code == 200


@pytest.mark.current
@mock.patch('app.authentication.check_password_hash')
@mock.patch('app.authentication.get_user')
def test_login_user(mocker_get_user, mocker_check_password_hash, app):

	""" Testing with insufficient form data """
	data = {'email': 'a@b.c'}
	resp = app.post('/login', data=data)
	assert resp.status_code == 200

	''' Testing with user not in application '''
	data = {'email': 'a@b.c', 'password': 'password'}
	mocker_get_user.side_effect = UserNotFound()
	resp = app.post('/login', data=data)
	mocker_get_user.assert_called_once()
	assert resp.status_code == 200

	''' Testing with invalid credentials '''
	data = {'email': 'a@b.c', 'password': 'password'}
	mocker_get_user.return_value = data
	mocker_check_password_hash.return_value = False
	resp = app.post('/login', data=data)
	assert mocker_check_password_hash.called_once()
	assert resp.status_code == 200
