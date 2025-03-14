import pyotp
import datetime

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
