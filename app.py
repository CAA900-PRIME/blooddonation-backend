from flask import Flask
import config
from api import register_apis # Import the function to register routes
from models import db
from flask_cors import CORS
app = Flask(__name__)


app.config.from_object(config.Config)

# Enable CORS for all domains (Will need to modify later) only accept traffic from a specific port number
CORS(app, resources={r"/api/*": {"origins": "*"}})
# i.ie : CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

db.init_app(app)  # Initialize the db with the app

register_apis(app) # Register API routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
