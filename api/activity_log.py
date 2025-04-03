from models import Users, ActivityLog, Users
from flask import Blueprint, jsonify, session

log_api = Blueprint('log_api', __name__)

@log_api.route("/get-logs", methods=["GET"])
def get_activity_logs():
    if "username" not in session:
        return jsonify({"error": "Unauthorized access. Please log in."}), 401

    username = session["username"]
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    logs = ActivityLog.query.filter_by(user_id=user.id).all()
    if len(logs) < 1:
        return jsonify({"error": "No logs yet."}), 200
    logs_contents = []
    for log in logs:
        logs_content = {
                "id": log.id,
                "action_type": log.action_type,
                "action_description": log.action_description,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "timestamp": log.timestamp
        }
        logs_contents.append(logs_content)
    return jsonify(logs_contents), 200

