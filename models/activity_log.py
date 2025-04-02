from datetime import datetime
from flask import request
from models import db


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)
    action_description = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('Users', foreign_keys=[user_id], backref='activity_logs', lazy=True)

    def __init__(self, user_id, action_type, action_description, ip_address=None, user_agent=None):
        self.user_id = user_id
        self.action_type = action_type
        self.action_description = action_description
        self.ip_address = ip_address
        self.user_agent = user_agent

    def __repr__(self):
        return f"<ActivityLog {self.id} - {self.action_type}>"

def log_activity(user_id, action_type, action_description):
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    
    log = ActivityLog(
        user_id=user_id,
        action_type=action_type,
        action_description=action_description,
        ip_address=ip_address,
        user_agent=user_agent
    )
    
    db.session.add(log)
    db.session.commit()
