from .auth import auth_api
from .user import user_api
from .events import events_api
from .application import app_api
from .country import country_api
from .city import city_api
from .activity_log import log_api


def register_apis(app):
    app.register_blueprint(auth_api, url_prefix="/api/auth")
    app.register_blueprint(user_api, url_prefix="/api/users")
    app.register_blueprint(events_api, url_prefix="/api/events")
    app.register_blueprint(app_api, url_prefix="/api/app")
    app.register_blueprint(country_api, url_prefix="/api/country")
    app.register_blueprint(city_api, url_prefix="/api/city")
    app.register_blueprint(log_api, url_prefix="/api/log")
