from flask import Blueprint, jsonify, session
from models import Users, Applications

user_api = Blueprint("user_api", __name__)

# Get All Users (Dangerous)
@user_api.route("/get-users", methods=["GET"])
def get_users():
    if "username" not in session:
        # TODO: Ensure only admin users can view all users. This is only for testing
        return jsonify({"error": "Unauthorized access. Please log in."}), 401
    users = Users.query.all()
    users_list = []
    for user in users:
        user_dict = {
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
        users_list.append(user_dict)
    return jsonify({"users": users_list}), 200       

# Dashboard
@user_api.route("/get-applications", methods=["GET"])
def get_dashboard():
    # Retrun applications within the same city of the current user
    if "username" in session:
        username = session["username"]
        user = Users.query.filter_by(username=username).first()
        if user:
            applications = Applications.query.filter_by(city=user.city).all()
            app_list = []
            for app in applications:
                app_dict = {
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
                app_list.append(app_dict)
            return jsonify(app_list), 200 # This will return a list of all applications

    return jsonify({"error": "Unauthorized or user not found"}), 401
