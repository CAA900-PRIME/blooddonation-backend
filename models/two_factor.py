import pyotp
from datetime import datetime, timedelta
from models import db

class TwoFactorCode(db.Model):
    __tablename__ = 'two_factor_codes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))

class TwoFactorAuth:
    @staticmethod
    def generate_secret():
        """Generate a new OTP secret key for a user."""
        return pyotp.random_base32()

    @staticmethod
    def generate_otp(secret):
        """Generate a time-based OTP."""
        totp = pyotp.TOTP(secret, interval=30)  # 30-second validity
        return totp.now()

    @staticmethod
    def verify_otp(secret, otp):
        """Verify an OTP against the stored secret."""
        totp = pyotp.TOTP(secret, interval=30)
        return totp.verify(otp)
