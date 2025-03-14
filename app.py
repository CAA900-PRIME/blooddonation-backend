from flask import Flask
import config
from api import register_apis  # Import the function to register routes
from models import db
from flask_cors import CORS
from flask_migrate import Migrate  # Add this

app = Flask(__name__)
app.config.from_object(config.Config)

# Allow credentials and only allow requests from frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

db.init_app(app)  # Initialize the database with the app

# Initialize Flask-Migrate
migrate = Migrate(app, db)  # ✅ Add this line

register_apis(app)  # Register API routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
