from flask import Blueprint, request, jsonify
from models.two_factor import TwoFactorAuth
from models import db
from models.user import User
from models.two_factor import TwoFactorCode
from datetime import datetime, timedelta
import random

two_factor_bp = Blueprint('two_factor', __name__)

@two_factor_bp.route('/2fa/generate', methods=['POST'])
def generate_2fa_code():
    data = request.json
    user_id = data.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Generate a 6-digit code
    code = str(random.randint(100000, 999999))

    # Store it in the DB
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    two_fa_code = TwoFactorCode(user_id=user_id, code=code, expires_at=expires_at)
    db.session.add(two_fa_code)
    db.session.commit()

    # In real use: send this via email or SMS
    return jsonify({'message': '2FA code generated', 'code': code})  # Don't return code in production

@two_factor_bp.route('/2fa/verify', methods=['POST'])
def verify_2fa_code():
    data = request.json
    user_id = data.get('user_id')
    code = data.get('code')

    record = TwoFactorCode.query.filter_by(user_id=user_id, code=code).first()

    if not record:
        return jsonify({'error': 'Invalid code'}), 400

    if record.expires_at < datetime.utcnow():
        return jsonify({'error': 'Code expired'}), 400

    # Optional: delete used code
    db.session.delete(record)
    db.session.commit()

    return jsonify({'message': '2FA verified successfully'})
