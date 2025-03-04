from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .user import Users
from .application import Applications
# will add other models
