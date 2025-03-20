from models import db
# from .country import Countries

class Cities(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country = db.relationship('Countries', back_populates='cities')

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id

    def __repr__(self):
        return f"<City {self.name} ({self.country_id})>"
