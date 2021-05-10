from app import create_app
from config import TestConfig
import pytest


@pytest.fixture
def app():
    client = create_app(TestConfig()).test_client()
    return client

# @pytest.fixture(autouse=True)
# def ndb_client():
# 	from unittest import mock
# 	from google.cloud.ndb import context as context_module
# 	client = mock.Mock(
# 		project="testing",
# 		namespace=None,
# 		stub=mock.Mock(spec=()),
# 		spec=("project", "namespace", "stub"),
# 		)
# 	context = context_module.Context(client).use()
# 	context.__enter__()
# 	return context
