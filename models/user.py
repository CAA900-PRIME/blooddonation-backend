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
    sex = db.Column(db.String(15), nullable=False, default="NONE")
    blood_type = db.Column(db.String(3), nullable=False, default="A")
    dob = db.Column(db.Date, nullable=False, default=datetime(1970, 1, 1))
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    home_address = db.Column(db.String(20), nullable=False)
    postalCode = db.Column(db.String(7), nullable=False, default='A1A 1A1')
    createdDate = db.Column(db.DateTime, default=datetime.utcnow)
    verifiedDate = db.Column(db.DateTime, nullable=True)
    lastLoggedIn = db.Column(db.DateTime, nullable=True)
    otp_secret = db.Column(db.String(16), nullable=True)
    reset_token = db.Column(db.String(100), nullable=True)  # Store password reset token
    reset_token_expiry = db.Column(db.DateTime, nullable=True)  # Expiry time for the token
    profile_pic = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, email, username, password, phone_number, firstName, lastName, country, city, homeAddress,blood_type, sex,
                 dob=None, postalCode='A1A 1A1'):
        self.email = email
        self.username = username
        self.password = password
        self.phone_number = phone_number
        self.firstName = firstName
        self.lastName = lastName
        self.dob = dob if dob else datetime(1970, 1, 1)
        self.postalCode = postalCode
        self.country = country
        self.city = city
        self.sex = sex
        self.blood_type = blood_type
        self.home_address = homeAddress
        self.otp_secret = None  # Default to None until 2FA is enabled
        self.reset_token = None  # Default to None until password reset is requested
        self.reset_token_expiry = None  # Default to None until password reset is requested
        self.profile_pic = None

    def __repr__(self):
        return f'<User {self.username} - {self.firstName} {self.email}>'
