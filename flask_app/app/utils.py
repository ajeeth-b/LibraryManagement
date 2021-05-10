from .db import ndb_client


def with_client_context(func):
    def wrapper(*args, **kwargs):
        with ndb_client.context():
            return func(*args, **kwargs)

    return wrapper
