from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Users, db
from typing import Optional, Dict
from datetime import datetime
import uuid
from utils.email_utils import send_email  # Make sure this exists or mock it

auth_api = Blueprint('auth_api', __name__)

# ------------------ LOGIN ------------------
@auth_api.route('/login', methods=['POST'])
def login():
    data: Optional[Dict] = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = Users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['username'] = user.username

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phoneNumber": user.phone_number,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "dob": user.dob.strftime("%Y-%m-%d") if user.dob else None,
            "homeAddress": user.home_address,
            "country": user.country,
            "city": user.city,
            "postalCode": user.postalCode,
            "createdDate": user.createdDate.strftime("%Y-%m-%d %H:%M:%S") if user.createdDate else None,
            "verifiedDate": user.verifiedDate.strftime("%Y-%m-%d %H:%M:%S") if user.verifiedDate else None,
            "lastLoggedIn": user.lastLoggedIn.strftime("%Y-%m-%d %H:%M:%S") if user.lastLoggedIn else None
        }

        return jsonify({"message": "Logged in successfully", "user": user_data}), 200

    return jsonify({"error": "Invalid email or password"}), 401

# ------------------ LOGOUT ------------------
@auth_api.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"message": "You have been logged out successfully."}), 200

# ------------------ SIGNUP + Email Verification Token ------------------
@auth_api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    phone_number = data.get("phoneNumber")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    dob = data.get("dob")
    postalCode = data.get("postalCode")
    homeAddress = data.get("homeAddress")
    country = data.get("country")
    city = data.get("city")

    if not username or not password or not email or not phone_number or not firstName or not lastName or not homeAddress or not country or not city:
        return {"error": "Missing required fields"}, 400

    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    password_hash = generate_password_hash(password)
    verification_token = str(uuid.uuid4())

    try:
        new_user = Users(
            email=email,
            username=username,
            password=password_hash,
            phone_number=phone_number,
            firstName=firstName,
            lastName=lastName,
            dob=dob,
            postalCode=postalCode,
            country=country,
            city=city,
            home_address=homeAddress,
            verification_token=verification_token
        )
        db.session.add(new_user)
        db.session.commit()




