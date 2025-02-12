from .auth import auth_api
from .user import user_api
from .events import events_api

def register_apis(app):
    app.register_blueprint(auth_api, url_prefix='/api/auth')
    app.register_blueprint(user_api, url_prefix='/api/users')
    app.register_blueprint(events_api, url_prefix='/api/events')
