from flask import Blueprint, request, jsonify, session
import traceback
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
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "firstName": user.firstName,
            "lastName": user.lastName,
            "dob": user.dob.strftime("%Y-%m-%d") if user.dob else None,
            "home_address": user.home_address,
            "country": user.country if user.country else None,
            "city": user.city if user.city else None,
            "sex": user.sex,
            "blood_type": user.blood_type,
            "postalCode": user.postalCode,
            "createdDate": user.createdDate.strftime("%Y-%m-%d %H:%M:%S") if user.createdDate else None,
            "verifiedDate": user.verifiedDate.strftime("%Y-%m-%d %H:%M:%S") if user.verifiedDate else None,
            "lastLoggedIn": user.lastLoggedIn.strftime("%Y-%m-%d %H:%M:%S") if user.lastLoggedIn else None
        }

        return jsonify({"message": "Logged in successfully", "user": user_data}), 200
    return jsonify({"error": "Invalid username or password"}), 401




@auth_api.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) ## because we saved the username in the sessions when the user loggedIn
    return jsonify({"message": "You have been logged out successfully."}), 200



@auth_api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()  # Expecting JSON payload
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
    sex = data.get("sex")
    blood_type = data.get("blood_type")

    print(username, password, email, phone_number, firstName, lastName, homeAddress, country, city, sex, blood_type)
    # Validate form inputs
    if not username or not password or not email or not phone_number or not firstName or not lastName or not homeAddress or not country or not city:
        return {"error": "Missing required fields"}, 400

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
                postalCode=postalCode,
                country=country,
                city=city,
                homeAddress=homeAddress,
                sex=sex,
                blood_type=blood_type
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Signup successful! Please login."}), 201

    except Exception as e:
        # Rollback the session in case of an error and log it
        db.session.rollback()
        print(f"Error creating user: {e}")
        return jsonify({"error": "An error occurred. Please try again."}), 500


@auth_api.route('/edit-profile', methods=['POST'])
def edit_profile():
    if "username" not in session:
        return jsonify({"error": "Unauthorized access"}), 403

    username = session["username"]
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        user.email = data.get("email", user.email)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.firstName = data.get("firstName", user.firstName)
        user.lastName = data.get("lastName", user.lastName)
        user.dob = data.get("dob", user.dob)
        user.postalCode = data.get("postalCode", user.postalCode)
        user.home_address = data.get("homeAddress", user.home_address)
        user.country = data.get("country", user.country)
        user.city = data.get("city", user.city)

        db.session.commit()
        return jsonify({"success": "Profile updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        print("Database Update Failed:", traceback.format_exc())  
        return jsonify({"error": str(e)}), 500
