from flask import Blueprint, jsonify, session
from models import Users

user_api = Blueprint('user_api', __name__)

@user_api.route('/get-users', methods=['GET'])
def get_users():
    if 'username' not in session:
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
            "Date Of Birth": user.dob,
            "postalCode": user.postalCode,
            "createdDate": user.createdDate,
            "verifiedDate": user.verifiedDate,
            "lastLoggedIn": user.lastLoggedIn,
        }
        users_list.append(user_dict)
    return jsonify({"users": users_list}), 200       



