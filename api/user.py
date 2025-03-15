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

# Generate OTP
@user_api.route("/generate-otp", methods=["POST"])
def generate_otp():
    data = request.json
    user_id = data.get("user_id")

    user = Users.query.get(user_id)
    if not user or not user.otp_secret:
        return jsonify({"error": "2FA not enabled"}), 400

    otp = TwoFactorAuth.generate_otp(user.otp_secret)
    return jsonify({"otp": otp})

# Verify OTP
@user_api.route("/verify-otp", methods=["POST"])
def verify_otp():
    data = request.json
    user_id = data.get("user_id")
    otp = data.get("otp")

    user = Users.query.get(user_id)
    if not user or not user.otp_secret:
        return jsonify({"error": "2FA not enabled"}), 400

    is_valid = TwoFactorAuth.verify_otp(user.otp_secret, otp)
    if is_valid:
        return jsonify({"message": "OTP is valid!"})
    else:
        return jsonify({"error": "Invalid OTP"}), 400

# -------------------- PASSWORD RESET FUNCTIONALITY -------------------- #

# Request Password Reset (Generate Token & Send Email)
@user_api.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    data = request.json
    email = data.get("email")

    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

 # Generate a secure reset token
    user.reset_token = secrets.token_hex(16)
    user.reset_token_expiry = datetime.utcnow() + timedelta(minutes=30)  # Token valid for 30 min
    db.session.commit()

 # Send reset token via email
    msg = Message("Password Reset Request",
                  sender=Config.MAIL_USERNAME,  # Fixed sender
                  recipients=[user.email])
    msg.body = f"Your password reset token: {user.reset_token}"
    mail.send(msg)

    return jsonify({"message": "Password reset token sent to your email."}), 200

# Reset Password
@user_api.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.json
    email = data.get("email")
    token = data.get("token")
    new_password = data.get("new_password")

    user = Users.query.filter_by(email=email, reset_token=token).first()
    if not user or user.reset_token_expiry < datetime.utcnow():
        return jsonify({"error": "Invalid or expired token"}), 400

 # Hash the new password before storing it
    user.password = generate_password_hash(new_password)
    user.reset_token = None  # Clear the token
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({"message": "Password successfully reset."}), 200)


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