from datetime import datetime
from enum import Enum
from models import db

class BloodType(Enum):
    A_PLUS = "A+"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B_MINUS = "B-"
    AB_PLUS = "AB+"
    AB_MINUS = "AB-"
    O_PLUS = "O+"
    O_MINUS = "O-"

class ApplicationStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    COMPLETED = "Completed"


class Application(db.Model):
    __tablename__ = 'application'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    blood_type = db.Column(db.Enum(BloodType), nullable=False) 
    hospital_name = db.Column(db.String(255), nullable=False)
    hospital_address = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    contact_phone_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.PENDING) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    requester = db.relationship('Users', foreign_keys=[requester_id], backref='applications_requested', lazy=True)
    
    doner = db.relationship('Users', foreign_keys=[doner_id], backref='applications_donated', lazy=True)
    
    def __init__(self, requester_id, blood_type, hospital_name,
                 hospital_address, country, city, contact_phone_number, status=ApplicationStatus.PENDING, doner_id=None):
        self.requester_id = requester_id
        self.blood_type = blood_type
        self.hospital_name = hospital_name
        self.hospital_address = hospital_address
        self.country = country
        self.city = city
        self.contact_phone_number = contact_phone_number
        self.status = status
        self.doner_id = doner_id
    
    def __repr__(self):
        return f'<Application {self.id} - {self.requester} - {self.doner_id} - {self.status}>'

