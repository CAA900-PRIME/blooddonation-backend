from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
from models import Users
from werkzeug.security import check_password_hash
from typing import Optional, Dict
from models import Users, db

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/login', methods=['POST'])
def login():
    data: Optional[Dict] = request.json
    # Updating to use email instead of username
    email = data.get('email')
    password = data.get('password')

    # Validate inputs
    if not email or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Query the user from the database
    user = Users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['username'] = user.username
        return jsonify({"message": "Logged in successfully", "username": user.username}), 200
    
    return jsonify({"error": "Invalid username or password"}), 401




@auth_api.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"message": "You have been logged out successfully."}), 200



@auth_api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Expecting JSON payload
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phone_number = data.get('phoneNumber')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    dob = data.get('dob')
    postalCode = data.get('postalCode')


    # Validate form inputs
    if not username or not password or not email or not phone_number or not firstName or not lastName:
        return {"error": "Missing required fields"}, 400
    # if not username or not password:
    #     return jsonify({"error": "Both username and password are required"}), 400

    # Hash the password
    password_hash = generate_password_hash(password)

    # Check if the username already exists
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    try:
        # Create and add new user
        new_user = Users(
                email=email,
                username=username,
                password=password_hash,
                phone_number=phone_number,
                firstName=firstName,
                lastName=lastName,
                dob=dob,
                postalCode=postalCode
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Signup successful! Please login."}), 201

    except Exception as e:
        # Rollback the session in case of an error and log it
        db.session.rollback()
        print(f"Error creating user: {e}")
        return jsonify({"error": "An error occurred. Please try again."}), 500


