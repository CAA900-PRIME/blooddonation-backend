from .auth import auth_api
from .user import user_api
from .events import events_api
from .application import app_api
from .two_factor import two_factor_bp
from .reset_password import reset_password_bp
from .verify_user import verify_user_bp


def register_apis(app):
    app.register_blueprint(auth_api, url_prefix="/api/auth")
    app.register_blueprint(user_api, url_prefix="/api/users")
    app.register_blueprint(events_api, url_prefix="/api/events")
    app.register_blueprint(app_api, url_prefix="/api/app")

    # New features
    app.register_blueprint(two_factor_bp, url_prefix="/api/2fa")
    app.register_blueprint(reset_password_bp, url_prefix="/api/password")
    app.register_blueprint(verify_user_bp, url_prefix="/api/verify")
