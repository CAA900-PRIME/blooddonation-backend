from datetime import datetime
from enum import Enum
from models import db

class ApplicationStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    COMPLETED = "Completed"


class Applications(db.Model):
    __tablename__ = 'application'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    hospital_name = db.Column(db.String(255), nullable=False)
    hospital_address = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.PENDING) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    appointment = db.Column(db.DateTime, nullable=False)
    requester = db.relationship('Users', foreign_keys=[requester_id], backref='applications_requested', lazy=True)
    donor = db.relationship('Users', foreign_keys=[donor_id], backref='applications_donated', lazy=True)
    
    def __init__(self, requester_id,
                 hospital_name,
                 hospital_address, country,
                 city, phone_number,
                 status=ApplicationStatus.PENDING,
                 donor_id=None,
                 appointment=None):
        self.requester_id = requester_id
        self.hospital_name = hospital_name
        self.hospital_address = hospital_address
        self.country = country
        self.city = city
        self.phone_number = phone_number
        self.status = status
        self.donor_id= donor_id
        self.appointment = appointment
    
    def __repr__(self):
        return f'<Application {self.id} - {self.requester} - {self.donor_id} - {self.status}>'

### Usage example:
# new_application = Application(
#     requester_id=1,  # Assume the requester has user_id=1
#     blood_type=BloodType.A_PLUS,
#     hospital_name="City Hospital",
#     hospital_address="123 Main St",
#     country="Country Name",
#     city="City Name",
#     contact_phone_number="1234567890"
# )
#
# # To add it to the database
# db.session.add(new_application)
# db.session.commit()

### When a doner applies for an application
# Assume we already have an application with id = 1, and a donor with user_id = 2
# application = Application.query.get(1)  # Fetch the application you want to update
# # Update the application to assign a donor
# application.doner_id = 2  # Assign the donor's ID
# db.session.commit()

