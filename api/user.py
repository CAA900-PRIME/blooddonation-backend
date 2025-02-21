from flask import Blueprint, jsonify
from models import Users

user_api = Blueprint('user_api', __name__)

# TODO: Ensure only admin users can view all users. This is only for testing
@user_api.route('/get-users', methods=['GET'])
def get_users():
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

    return jsonify(users_list)
