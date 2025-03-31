from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)
    action_description = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('Users', backref=db.backref('activity_logs', cascade='all, delete-orphan', lazy=True))

    def __init__(self, user_id, action_type, action_description, ip_address=None, user_agent=None):
        self.user_id = user_id
        self.action_type = action_type
        self.action_description = action_description
        self.ip_address = ip_address
        self.user_agent = user_agent

    def __repr__(self):
        return f"<ActivityLog {self.id} - {self.action_type}>"
