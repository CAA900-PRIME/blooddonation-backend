from flask import Blueprint, request, jsonify
from models.user import User
from models import db
from datetime import datetime, timedelta
import secrets

reset_password_bp = Blueprint('reset_password_bp', __name__)

@reset_password_bp.route('/api/request-reset', methods=['POST'])
def request_reset():
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    token = secrets.token_urlsafe(32)
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()

    # Placeholder: Send token via email
    print(f"Reset link for {email}: http://localhost:5173/reset-password?token={token}")

    return jsonify({"message": "Reset link sent."})


