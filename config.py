import os
from flask_mail import Mail  #  Ensure Flask-Mail is imported

class Config:
    # Secret Key (Used for session security)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

    # MySQL configuration for SQLAlchemy
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'flask_user')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'flask_password')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'blooddonation')

    # SQLAlchemy Database URI
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3306/{MYSQL_DB}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable track modifications to avoid overhead

    # Flask-Mail Configuration (Securely Using Environment Variables)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')  # SMTP Server
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))  # Usually 587 for TLS
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Get from environment
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Get from environment
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

#  Initialize Flask-Mail (this was missing before)
mail = Mail()
