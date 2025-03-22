from flask import Blueprint, request, jsonify
from models.user import User
from models import db
import secrets

verify_user_bp = Blueprint('verify_user_bp', __name__)

@verify_user_bp.route('/api/send-verification', methods=['POST'])
def send_verification():
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    token = secrets.token_urlsafe(16)
    user.verification_token = token
    db.session.commit()

    # Simulate sending verification
    print(f"Verification link: http://localhost:5173/verify?token={token}")

    return jsonify({"message": "Verification email sent."})

@verify_user_bp.route('/api/verify-email', methods=['POST'])
def verify_email():
    token = request.get_json().get("token")
    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return jsonify({"error": "Invalid token"}), 400

    user.is_verified = True
    user.verification_token = None
    db.session.commit()
    return jsonify({"message": "Email verified!"})
