import os

class Config:
    # MySQL Configuration
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'password'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'inventory_db'
    
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MongoDB Configuration
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://anand123:anand123@cluster0.vyrrifu.mongodb.net/inventory_logs?retryWrites=true&w=majority&appName=Cluster0'
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
