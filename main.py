from flask import Flask, jsonify
from src.extensions import api, cors, db, jwt, migrate, compress
from src.routes import users_blp, refresh_blp, blogs_blp
from dotenv import load_dotenv
from src.models import RevokedTokensModel
from flask_jwt_extended import unset_jwt_cookies

load_dotenv()

def create_app():
  app = Flask(__name__)
  app.config.from_prefixed_env()
  app.config['JWT_CSRF_IN_COOKIES'] = False
  app.config['JWT_COOKIE_CSRF_PROTECT'] = False
  
  cors.init_app(app)
  db.init_app(app)
  api.init_app(app)
  jwt.init_app(app)
  migrate.init_app(app, db)
  compress.init_app(app)
  
  api.register_blueprint(users_blp, url_prefix='/api')
  api.register_blueprint(refresh_blp)
  api.register_blueprint(blogs_blp, url_prefix='/api')
  
  @jwt.expired_token_loader
  def expired_token_cb(jwtHeader, jwtPayload):
    response = jsonify({'message': 'Token expired'})
    unset_jwt_cookies(response)
    
    return response, 401
  
  @jwt.invalid_token_loader
  def invalid_token_cb(error):
    response = jsonify({'message': 'Invalid token signature'})
    unset_jwt_cookies(response)
    
    return response, 401
  
  @jwt.unauthorized_loader
  def unauthorized_token_cb(error):
    response = jsonify({'message': 'Missing token'})
    unset_jwt_cookies(response)
    
    return response, 401
  
  @jwt.token_in_blocklist_loader
  def token_blocklist_cb(jwtHeader, jwtPayload):
    return RevokedTokensModel.token_in_blocklist(jwtPayload['jti'])
  
  @jwt.revoked_token_loader
  def revoked_token_cb(jwtHeader, jwtPayload):
    response = jsonify({'message': 'Token has been revoked and not valid'})
    unset_jwt_cookies(response)
    
    return response, 401
  
  return app

create_app()