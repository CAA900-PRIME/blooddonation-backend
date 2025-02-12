from flask import jsonify, Blueprint

events_api = Blueprint('events_api', __name__)

# This is an example, will be removed later.
@events_api.route('/get-events')
def load_events():
    events = [
        {'name': 'City Hospital Blood Drive', 'date': '2025-02-10'},
        {'name': 'Community Center Donation Day', 'date': '2025-02-15'},
        {'name': 'University Blood Donation Camp', 'date': '2025-02-20'}
    ]
    return jsonify(events)

