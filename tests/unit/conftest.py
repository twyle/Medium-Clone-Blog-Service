import pytest

from api import create_app, db


@pytest.fixture()
def app():
    app = create_app("testing")
    app.config.update({
        "POSTGRES_HOST": '192.168.100.4',
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app


@pytest.fixture()
def dev_app():
    app = create_app("development")
    app.config.update({
        "POSTGRES_HOST": '0.0.0.0',
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
