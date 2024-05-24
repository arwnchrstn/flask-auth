from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
api = Api()
jwt = JWTManager()
cors = CORS(origins=['http://localhost:3000'])
migrate = Migrate()