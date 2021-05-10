import pytest


def test_index(app):
	assert app.get('/').status_code == 302


def test_get_available_book_list(app):
	assert app.get('/').status_code == 302
