from .auth import auth_api
from .user import user_api
from .events import events_api
from .application import app_api
from .two_factor import two_factor_bp  # NEW: Import 2FA blueprint

def register_apis(app):
    app.register_blueprint(auth_api, url_prefix="/api/auth")
    app.register_blueprint(user_api, url_prefix="/api/users")
    app.register_blueprint(events_api, url_prefix="/api/events")
    app.register_blueprint(app_api, url_prefix="/api/app")
    app.register_blueprint(two_factor_bp, url_prefix="/api/2fa")  # NEW: Register 2FA routes
