from flask import Flask
import config
from api import register_apis
from models import db
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(config.Config)

# Allow credentials and only allow requests from frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

# Init the database with the app
db.init_app(app)  

# Register API routes
register_apis(app)  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
