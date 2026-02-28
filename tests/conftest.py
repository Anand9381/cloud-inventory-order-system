import pytest
import os
from src.app import create_app
from src.extensions import db

@pytest.fixture
def app():
    # Use testing config
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use SQLite for unit tests for speed/simplicity or mock
    # OR better: use the mysql service in CI?
    # For simplicity in CI without complex setup:
    # app = create_app()
    # But mysql connection might fail if service not up or schemas not created.
    # Let's mock db or use sqlite if possible.
    # The models rely on mysql dialect features... let's try to stick to mysql service.
    
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
