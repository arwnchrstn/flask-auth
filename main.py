from flask import Flask, jsonify, make_response
from src.extensions import api, cors, db, jwt, migrate
from src.routes.users import users_blp
from src.routes.refresh import refresh_blp
from dotenv import load_dotenv
from src.models.revoked_tokens import RevokedTokens
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
  
  api.register_blueprint(users_blp, url_prefix='/api/users')
  api.register_blueprint(refresh_blp)
  
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
    return RevokedTokens.token_in_blocklist(jwtPayload['jti'])
  
  @jwt.revoked_token_loader
  def revoked_token_cb(jwtHeader, jwtPayload):
    response = jsonify({'message': 'Token has been revoked and not valid'})
    unset_jwt_cookies(response)
    
    return response, 401
  
  return app

create_app()