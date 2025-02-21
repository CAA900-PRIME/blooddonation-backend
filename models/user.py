from models import db
from datetime import datetime

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False, default=datetime(1970, 1, 1))
    postalCode = db.Column(db.String(7), nullable=False, default='A1A 1A1')
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    verifiedDate = db.Column(db.DateTime, nullable=True)
    lastLoggedIn = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, username, password, phone_number, firstName, lastName, dob=None, postalCode='A1A 1A1'):
        self.email = email
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.firstName = firstName
        self.lastName = lastName
        self.dob = dob if dob else datetime(1970, 1, 1)
        self.postalCode = postalCode    
    def __repr__(self):
        return f'<User {self.username}>'
