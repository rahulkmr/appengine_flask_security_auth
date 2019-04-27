import os

import pytest

from appengine_flask_security_auth.tests import settings
from appengine_flask_security_auth import create_app


@pytest.fixture(scope='session')
def app():
    _app = create_app(settings)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def db(app):
    from appengine_flask_security_auth import db as _db

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.remove()
    _db.drop_all()


@pytest.fixture(scope='function')
def client(app, db):
    return app.test_client()
