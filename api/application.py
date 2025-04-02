from typing import Optional, Dict
from flask import Blueprint, request, jsonify, session
from models import Applications, db, Users, ApplicationStatus
from datetime import datetime

from models.activity_log import log_activity

app_api = Blueprint('app_api', __name__)

@app_api.route("/create-application", methods=["POST"])
def create_application():
    data: Optional[Dict] = request.json
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
        
        # Check if there is already an application created
        applications = Applications.query.filter_by(requester_id=requester_user.id).all()
        if len(applications) >= 1:
            return jsonify({"error": "You can only have one blood request application at a time."}), 400

        # Check if the user has already applied to a blood request application
        applications = Applications.query.filter_by(donor_id=requester_user.id).all()
        if len(applications) >=1:
            return jsonify({"error": "You cannot create to a blood request application at this time."}), 400

        # Extract values from request JSON
        hospital_name = data.get("hospital_name")
        hospital_address = data.get("hospital_address")
        country = data.get("country")
        city = data.get("city")
        phone_number = data.get("phone_number")
        appointment_str = data.get("appointment")


        print(hospital_address, hospital_name, phone_number, country, city, appointment_str)
        # Validate required fields
        if not hospital_name or not phone_number or not country or not city or not appointment_str:
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
                hospital_name=hospital_name,
                hospital_address=hospital_address,
                city=city,
                country=country,
                phone_number=phone_number,
                appointment=appointment
            )
            db.session.add(new_application)
            db.session.commit()
            log_activity(user_id=requester_user.id, action_type="Create Blood Request Application", action_description=f"Blood Request Application was created. {new_application}")
            return jsonify({"message": "Application created successfully!"}), 201

        except Exception as e:
            # Rollback the session in case of an error
            db.session.rollback()
            print(f"Error creating application: {e}")
            return jsonify({"error": "An error occurred. Please try again."}), 500

    return jsonify({"error": "Unauthorized access"}), 401


# get all applications
@app_api.route("/get-applications", methods=["GET"])
def get_applications():
    # Retrun applications within the same city of the current user
    if "username" in session:
        username = session["username"]
        # We will ensure to execlude the logged in user created applications. And not to show anything 
        user = Users.query.filter_by(username=username).first()
        if user:
            applications = Applications.query.filter_by(city=user.city).filter(
                Applications.requester_id != user.id,
                Applications.donor_id == None
            ).all()
            app_list = []
            for app in applications:
                requester_user = Users.query.filter_by(id=app.requester_id).first()
                if requester_user:
                    blood_type = requester_user.blood_type
                else:
                    blood_type = "Unknown - Refered to a deleted user account"
                app_dict = {
                    "id": app.id,
                    "requester_id": app.requester_id,
                    "doner_id": app.donor_id,
                    "blood_type": blood_type, ## blood type coming from the user
                    "hospital_name": app.hospital_name,
                    "hospital_address": app.hospital_address,
                    "country": app.country,
                    "city": app.city,
                    "phone_number": app.phone_number, "status": app.status.value, "created_at": app.created_at,
                    "appointment": app.appointment
                }
                app_list.append(app_dict)
            return jsonify(app_list), 200 # This will return a list of all applications
    return jsonify({"error": "Unauthorized or user not found"}), 401


# Dashboard get my applications
@app_api.route("/get-my-applications", methods=["GET"])
def get_my_applications():
    # Retrun applications within the same city of the current user
    if "username" in session:
        username = session["username"]
        user = Users.query.filter_by(username=username).first()
        if user:
            applications = Applications.query.filter_by(city=user.city, requester_id=user.id).all()
            app_list = []
            for app in applications:
                app_dict = {
                    "id": app.id,
                    "requester_id": app.requester_id,
                    "doner_id": app.donor_id,
                    "blood_type": user.blood_type, # blood type coming from the user
                    "hospital_name": app.hospital_name,
                    "hospital_address": app.hospital_address,
                    "country": app.country,
                    "city": app.city,
                    "phone_number": app.phone_number,
                    "status": app.status.value,
                    "created_at": app.created_at,
                    "appointment": app.appointment
                }
                app_list.append(app_dict)
            return jsonify(app_list), 200 # This will return a list of all applications

    return jsonify({"error": "Unauthorized or user not found"}), 401


# User Appply for blood request application
@app_api.route("/apply-application", methods=["POST"])
def apply_application():
    data: Optional[Dict] = request.json  
    # I think here we are only expecting the application id, since we alraedy have the user who is applying
    if "username" in session:
        username = session["username"]
        user = Users.query.filter_by(username=username).first() # the user will be the donor.
        if user:
            applications = Applications.query.filter_by(city=user.city, requester_id=user.id).all()
            if len(applications) >= 1:
                return jsonify({"error": "You cannot apply for a blood request application at this time."}), 400
            app_id = data.get("app_id")
            application = Applications.query.filter_by(id=app_id).first()
            if application:
                requester_user = Users.query.filter_by(id=application.requester_id).first()
                if requester_user.blood_type != user.blood_type:
                    return jsonify({"error": "Blood type does not match!"}), 401
                application.donor_id = user.id
                application.status = ApplicationStatus.APPROVED
                db.session.commit()
                log_activity(
                        user_id=application.requester_id,
                        action_type="Approved Blood Request",
                        action_description=f"Application successfully Accepted. {application} - {user.firstName} {user.email}"
                )
                log_activity(
                        user_id=application.donor_id,
                        action_type="Applied Blood Request",
                        action_description=f"Application successfully applied. {application} - {requester_user.firstName} {requester_user.email}"
                )

                return jsonify({"message": "Application successfully applied."}), 200
            return jsonify({"error": "Application not found."}), 404
        return jsonify({"error": "User not found."}), 404
    return jsonify({"error": "Unauthorized or user not found"}), 401

# User cancel a blood request application
@app_api.route("/cancel-application", methods=["POST"])
def cancel_application():
    data: Optional[Dict] = request.json  
    # I think here we are only expecting the application id, since we alraedy have the user who is canceling
    if "username" in session:
        username = session["username"]
        user = Users.query.filter_by(username=username).first()
        if user:
            app_id = data.get("app_id")
            application = Applications.query.filter_by(id=app_id).first()
            
            if application:
                application.donor_id = None
                application.status = ApplicationStatus.PENDING
                db.session.commit()
                log_activity(
                        user_id=user.id,
                        action_type="Canceled Blood Request",
                        action_description=f"Application Canceled. ID: {application}"
                )
                return jsonify({"message": "Application successfully canceled."}), 200
            return jsonify({"error": "Application not found."}), 404
        return jsonify({"error": "User not found."}), 404
    return jsonify({"error": "Unauthorized or user not found"}), 401


@app_api.route("/get-applied-applications", methods=["GET"])
def get_applied_applications():
    # Retrun applications within the same city of the current user
    if "username" in session:
        username = session["username"]
        user = Users.query.filter_by(username=username).first()
        if user:
            applications = Applications.query.filter_by(city=user.city, donor_id=user.id).all()
            app_list = []
            for app in applications:
                requester_user = Users.query.filter_by(id=app.requester_id).first()
                if requester_user:
                    blood_type = requester_user.blood_type
                else:
                    blood_type = "Unknown - Refered to a deleted user account"
                app_dict = {
                    "id": app.id,
                    "requester_id": app.requester_id,
                    "doner_id": app.donor_id,
                    "blood_type": blood_type,
                    "hospital_name": app.hospital_name,
                    "hospital_address": app.hospital_address,
                    "country": app.country,
                    "city": app.city,
                    "phone_number": app.phone_number,
                    "status": app.status.value,
                    "created_at": app.created_at,
                    "appointment": app.appointment
                }
                app_list.append(app_dict)
            return jsonify(app_list), 200 # This will return a list of all applications
    return jsonify({"error": "Unauthorized or user not found"}), 401

## Update currnet selected application
@app_api.route("/update-application/<int:app_id>", methods=["POST"])
def update_application(app_id):
    if "username" not in session:
            return jsonify({"error": "Unauthorized access"}), 403

    username = session["username"]
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    application = Applications.query.filter_by(id=app_id).first()
    if not application:
        return jsonify({"error": "Blood Request application not found"}), 404
    if application.status == ApplicationStatus.APPROVED:
        return jsonify({"error": "The blood request application cannot be modified. It has already beeen accepted."}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Update only provided fields
    for key, value in data.items():
        if hasattr(application, key):
            setattr(application, key, value)
    log_activity(
            user_id=user.id,
            action_type="Update Blood Request Application",
            action_description=f"Applicatioun {application} has been updated!"
    )
    db.session.commit()
    
    return jsonify({"success": "Updated successfully!"}), 200


## Delete created application by the logged in user.
@app_api.route("/delete-application", methods=["POST"])
def delete_application():
    data: Optional[Dict] = request.json
    print(data)
    if "username" in session:
        username = session["username"]
        user = Users.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found."}), 404
        app_id = data.get("app_id")
        application = Applications.query.filter_by(id=app_id).first()
        if not application:
            return jsonify({"error": "Application not found."}), 404
        if application.requester_id != user.id:
            return jsonify({"error": "Unauthorized to delete this application."}), 403
        db.session.delete(application)
        db.session.commit()
        log_activity(
            user_id=user.id,
            action_type="Deleted Blood Request Application",
            action_description=f"Applicatioun {application} has been deleted!"
    )
    return jsonify({"success": "Deleted successfully!"}), 200


## Get application details
@app_api.route("/get-approved-application-details", methods=["POST"])
def get_approved_application_details():
    ## First we need to get the current application that is applied for.
    data: Optional[Dict] = request.json
    username = session["username"]
    if "username" in session:
        user = Users.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found."}), 404
        app_id = data.get("app_id")
        application = Applications.query.filter_by(id=app_id).first()
        if not application:
            return jsonify({"error": "Application not found."}), 404
        requester = Users.query.filter_by(id=application.requester_id).first()
        donor = Users.query.filter_by(id=application.donor_id).first()
        app_details = {
                "id": application.id,
                "rqFirstName": requester.firstName,
                "rqLastName": requester.lastName,
                "rqPhone": requester.phone_number,
                "rqEmail": requester.email,
                "rqBloodType": requester.blood_type,
                "rqSex": requester.sex,
                "doFirstName": donor.firstName,
                "doLastName": donor.lastName,
                "doPhone": donor.phone_number,
                "doEmail": donor.email,
                "doBloodType": donor.blood_type,
                "doSex": donor.sex,
                "appHospitalName":application.hospital_name,
                "appHospitalAddress": application.hospital_address,
                "appCountry": application.country,
                "appCity": application.city,
                "appStatus": application.status.value,
                "appAppointment": application.appointment
        }

        return jsonify({"app_details": app_details}), 200
    return jsonify({"error": "Couldn't get application details"}), 400
