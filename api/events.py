from flask import jsonify, Blueprint, session

events_api = Blueprint('events_api', __name__)

# This is an example, will be removed later.
@events_api.route('/get-events')
def load_events():
    if 'username' not in session:
        # TODO: Ensure only admin users can view all users. This is only for testing
        return jsonify({"error": "Unauthorized access. Please log in."}), 401
    events = [ ## Random data
        {'name': 'City Hospital Blood Drive', 'date': '2025-02-10'},
        {'name': 'Community Center Donation Day', 'date': '2025-02-15'},
        {'name': 'University Blood Donation Camp', 'date': '2025-02-20'}
    ]
    return jsonify({"events": events}), 200

