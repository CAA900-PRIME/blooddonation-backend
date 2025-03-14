from flask import Blueprint, request, jsonify, session
import pyotp
from models import db
from models.user import Users
from models.two_factor import TwoFactorAuth
from models import Applications

user_api = Blueprint("user_api", __name__)

# Enable 2FA (Generate and Store OTP Secret)
@user_api.route("/enable-2fa", methods=["POST"])
def enable_2fa():
    data = request.json
    user_id = data.get("user_id")

    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Generate OTP secret and save it to the user
    user.otp_secret = TwoFactorAuth.generate_secret()
    db.session.commit()

    return jsonify({"message": "2FA enabled", "otp_secret": user.otp_secret})

# Existing Routes
@user_api.route("/get-users", methods=["GET"])
def get_users():
    if "username" not in session:
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    users = Users.query.all()
    users_list = [
        {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "phone_number": user.phone_number,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "dob": user.dob,
            "postalCode": user.postalCode,
            "createdDate": user.createdDate,
            "verifiedDate": user.verifiedDate,
            "lastLoggedIn": user.lastLoggedIn,
        }
        for user in users
    ]
    return jsonify({"users": users_list}), 200


@user_api.route("/get-applications", methods=["GET"])
def get_dashboard():
    if "username" in session:
        username = session["username"]
        user = Users.query.filter_by(username=username).first()
        if user:
            applications = Applications.query.filter_by(city=user.city).all()
            app_list = [
                {
                    "id": app.id,
                    "requester_id": app.requester_id,
                    "doner_id": app.donor_id,
                    "hospital_name": app.hospital_name,
                    "hospital_address": app.hospital_address,
                    "country": app.country,
                    "city": app.city,
                    "contact_phone_number": app.contact_phone_number,
                    "status": app.status,
                    "created_at": app.created_at,
                }
                for app in applications
            ]
            return jsonify(app_list), 200

    return jsonify({"error": "Unauthorized or user not found"}), 401