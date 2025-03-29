from flask import Flask
from dotenv import load_dotenv  # ✅ NEW: To load .env file
import config
from api import register_apis
from models import db
from flask_cors import CORS
from flask_migrate import Migrate

load_dotenv()  # ✅ NEW: Load environment variables from .env

app = Flask(__name__)
app.config.from_object(config.Config)

# Allow credentials and only allow requests from frontend
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173", "supports_credentials": True}})

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Register all backend APIs
register_apis(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
