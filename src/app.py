from flask import Flask
from src.config import Config
from src.extensions import db, init_mongo
from src.routes import api, main
from src.models import User, Product, Inventory, Order, OrderItem
import os

def create_app():
    print("Starting application with configuration:")
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    init_mongo(app)

    # Register Blueprints
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(main)

    # Create Database Tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
