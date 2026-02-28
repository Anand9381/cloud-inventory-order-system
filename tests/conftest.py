import pytest
import os
from src.app import create_app
from src.extensions import db

@pytest.fixture
def app():
    # Force testing config
    os.environ['FLASK_ENV'] = 'testing'
    
    # Create the app
    app = create_app()
    
    # Override configuration for testing
    app.config.update({
        "TESTING": True,
        # Use SQLite in-memory database for faster, isolated tests
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
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
