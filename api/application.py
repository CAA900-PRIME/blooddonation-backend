from typing import Optional, Dict
from flask import Blueprint, request, jsonify, session
from models import Applications, db, Users
from datetime import datetime

app_api = Blueprint('app_api', __name__)

@app_api.route("/create-application", methods=["POST"])
def create_application():
    data: Optional[Dict] = request.json  # Get JSON payload once
    if "username" in session:
        username = session["username"]
        requester_user = Users.query.filter_by(username=username).first()
        if not requester_user:
            return jsonify({"error": "User not found, can't create the application."}), 404
        
        # Additional Check
        requester_id = requester_user.id
        user_id = data.get("requester_id")
        if requester_id != user_id:
            return jsonify({"error": "Incorrect match. Wrong cookie"}), 404

        # Extract values from request JSON
        blood_type = data.get("blood_type")
        hospital_name = data.get("hospital_name")
        hospital_address = data.get("hospital_address")
        country = data.get("country")
        city = data.get("city")
        phone_number = data.get("contact_phone_number")
        appointment_str = data.get("appointment")
        
        print(hospital_address, hospital_name, blood_type, phone_number, country, city, appointment_str)
        # Validate required fields
        if not hospital_name or not blood_type or not phone_number or not country or not city or not appointment_str:
            return jsonify({"error": "Missing required fields"}), 400

        # Validate and parse appointment datetime
        try:
            appointment = datetime.strptime(appointment_str, "%Y-%m-%dT%H:%M")  # Make sure format matches the frontend
        except ValueError:
            return jsonify({"error": "Invalid appointment date format. Use YYYY-MM-DDTHH:MM"}), 400

        try:
            # Create and add new application
            new_application = Applications(
                requester_id=requester_id,
                blood_type=blood_type,
                hospital_name=hospital_name,
                hospital_address=hospital_address,
                city=city,
                country=country,
                contact_phone_number=phone_number,
                appointment=appointment
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

