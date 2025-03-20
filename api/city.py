from flask import Blueprint, jsonify
from models import Cities, Countries

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


@city_api.route("/get-cities-with-code/<string:country_code>", methods=["GET"])
def get_cities_by_country_code(country_code):
    country = Countries.query.filter_by(code=country_code).first()
    if not country:
        return jsonify({"error": "Country not found"}), 404

    cities = Cities.query.filter_by(country_id=country.id).all()
    listOfCities = []
    for city in cities:
        city_dict = {
            "id": city.id,
            "name": city.name,
        }
        listOfCities.append(city_dict)
    
    return jsonify({"cities": listOfCities}), 200
