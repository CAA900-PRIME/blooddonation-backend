from flask import Blueprint, jsonify
from models import Countries

country_api = Blueprint("country_api", __name__)

@country_api.route("/get-countries", methods=["GET"])
def get_countries():
    countries = Countries.query.all()
    print(countries)
    listOfCountries = []
    for country in countries:
        country_dict = {
                "id": country.id,
                "name": country.name,
                "code": country.code
        }
        listOfCountries.append(country_dict)
    return jsonify({"countries": listOfCountries}), 200
