from .db import client


def with_client_context(func):
    def wrapper(*args, **kwargs):
        with client.context():
            return func(*args, **kwargs)

    return wrapper