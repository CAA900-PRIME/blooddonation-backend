from flask import Blueprint, jsonify
from models import Cities

city_api = Blueprint("city_api", __name__)

@city_api.route("/get-cities", methods=["GET"])
def get_countries():
    cities = Cities.query.all()
    listOfCities = []
    for city in cities:
        city_dict = {
                "id": city.id,
                "name": city.name,
        }
        listOfCities.append(city_dict)
    return jsonify({"cities": listOfCities}), 200

