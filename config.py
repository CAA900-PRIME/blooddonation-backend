import os


class Config:
    # Secret Key (Used for session security)
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

    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com'  # Your email provider's SMTP server
    MAIL_PORT = 587  # Usually 587 for TLS
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@example.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-email-password'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
