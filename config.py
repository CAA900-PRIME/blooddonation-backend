import os

class Config:
    # The following can be left as it is for now, since we are still at development. Later will ensure to use environemt variables.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    
    # MySQL configuration for SQLAlchemy
    MYSQL_HOST = 'localhost'  # Container name or hostname of MySQL service (in the Docker network)
    MYSQL_USER = 'flask_user'
    MYSQL_PASSWORD = 'flask_password'
    MYSQL_DB = 'blooddonation'
    
    # SQLAlchemy Database URI
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}'
    )
    
    # Disable track modifications to avoid overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False
