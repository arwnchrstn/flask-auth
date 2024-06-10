from flask_sqlalchemy import SQLAlchemy
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_compress import Compress
from dotenv import load_dotenv
from os import getenv

load_dotenv()

db = SQLAlchemy()
api = Api()
jwt = JWTManager()
cors = CORS(origins=getenv('FLASK_ALLOWED_ORIGIN'), supports_credentials=True)
migrate = Migrate()
compress = Compress()