from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from .user import Users
from .application import Applications
from .application import ApplicationStatus
from .country import Countries
from .city import Cities
# will add other models
