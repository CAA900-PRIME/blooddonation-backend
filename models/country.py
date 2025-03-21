from models import db

class Countries(db.Model):
    __tablename__ = "countries"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)
    # Country has many cities
    cities = db.relationship('Cities', back_populates='country', cascade="all, delete-orphan")

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return f"<Country {self.name} ({self.code})>"

    
