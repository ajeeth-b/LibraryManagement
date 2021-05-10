import pytest
from jinja2.exceptions import UndefinedError

def test_index(app):
	assert app.get('/').status_code == 302


def test_get_available_book_list(app):
	assert app.get('/').status_code == 302
