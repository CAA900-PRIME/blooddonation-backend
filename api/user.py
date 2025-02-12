from flask import Blueprint, jsonify
from models import Users

user_api = Blueprint('user_api', __name__)

@user_api.route('/get-users', methods=['GET'])

# TODO: Ensure only admin users can view all users. This is only for testing
def get_users():
    users = Users.query.all()
    users_list = []
    for user in users:
        user_dict = {
            "id": user.id,
            "username": user.username
        }
        users_list.append(user_dict)

    return jsonify(users_list)
