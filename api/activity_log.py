from models import Users, db
from flask import Blueprint

log_api = Blueprint('log_api', __name__)

@log_api.route("/get-logs", methods=["GET"])
def get_activity_logs():
    pass


