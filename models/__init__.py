from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()  # Initialize db here
from .user import Users
# will add other models
# i.e from .post import Post

