from flask import Flask
import config
from api import register_apis # Import the function to register routes
from models import db
app = Flask(__name__)

app.config.from_object(config.Config)

db.init_app(app)  # Initialize the db with the app

register_apis(app) # Register API routes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
