from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .user import Users
from .application import Applications
from .application import ApplicationStatus
from .city import Cities
from .country import Countries
# will add other models
