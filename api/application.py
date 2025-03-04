from typing import Optional, Dict
from flask import Blueprint, request, jsonify, session
from models import Applications, db, Users

app_api = Blueprint('app_api', __name__)

@app_api.route("/create-application", methods=["POST"])
def create_application():
    data: Optional[Dict] = request.json  # Get JSON payload once
    if "username" in session:
        # Get current user account - requester_id
        username = session["username"]
        requester_user = Users.query.filter_by(username=username).first()
        if not requester_user:
            return jsonify({"error": "User not found, can't create the application."}), 404
        
        requester_id = requester_user.id

        # Extract values from request JSON
        blood_type = data.get("bloodType")
        hospital_name = data.get("hospitalName")
        hospital_address = data.get("hospitalAddress")
        country = data.get("country")
        city = data.get("city")
        phone_number = data.get("phone_number")

        # Validate required fields
        if not hospital_name or not blood_type or not phone_number or not country or not city:
            return jsonify({"error": "Missing required fields"}), 400

        try:
            # Create and add new application
            new_application = Applications(
                requester_id=requester_id,
                blood_type=blood_type,
                hospital_name=hospital_name,
                hospital_address=hospital_address,
                city=city,
                country=country,
                contact_phone_number=phone_number
            )
            db.session.add(new_application)
            db.session.commit()
            return jsonify({"message": "Application created successfully!"}), 201

        except Exception as e:
            # Rollback the session in case of an error
            db.session.rollback()
            print(f"Error creating application: {e}")
            return jsonify({"error": "An error occurred. Please try again."}), 500

    return jsonify({"error": "Unauthorized access"}), 401

