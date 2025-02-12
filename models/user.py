from models import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    def __init__(self, username,password):
      self.username = username
      self.password = password
    def __repr__(self):
        return f'<User {self.username}>'
