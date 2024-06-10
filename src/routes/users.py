from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.schemas import PlainUserSchema
from flask import jsonify, request
from src.models import UsersModel, RevokedTokensModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies, unset_jwt_cookies, decode_token
from datetime import timedelta
from flask_jwt_extended.exceptions import JWTDecodeError
from dotenv import load_dotenv
from os import getenv

load_dotenv()

users_blp = Blueprint('Users', __name__)

@users_blp.route('/users/signup')
class UserSignup(MethodView):
  @users_blp.arguments(PlainUserSchema)
  @users_blp.response(201)
  @users_blp.alt_response(409, description='User already exists')
  @users_blp.alt_response(500, description='Server error')
  def post(self, userData):
    try:
      user = UsersModel(**userData)
      
      if user.check_username_if_exists():
        abort(409, message='Username already exists')
        
      user.save_user()
      
      return jsonify({'message': 'User created'}), 201
    except SQLAlchemyError as e:
      abort(500, message='Database error - An error occured while creating an account', errors=repr(e))

@users_blp.route('/users/signin')
class UserSignin(MethodView):
  @users_blp.arguments(PlainUserSchema)
  @users_blp.response(200)
  @users_blp.alt_response(404, description='User not found')
  @users_blp.alt_response(401, description='Invalid credentials')
  def post(self, userData):
    try:
      user = UsersModel(**userData)
      
      if not user.check_username_if_exists():
        abort(404, message='User not found')
        
      if not user.verify_password():
        abort(401, message='Invalid credentials')
        
      existing_user_data = user.get_user_data()
        
      accessToken = create_access_token(identity=existing_user_data.id, expires_delta=timedelta(minutes=10))
      refresh_token = create_refresh_token(identity=existing_user_data.id, expires_delta=timedelta(days=7))
      
      response = jsonify({'username': existing_user_data.username, 'id': existing_user_data.id, 'accessToken': accessToken})
      
      set_refresh_cookies(response, refresh_token, max_age=timedelta(days=7))
      
      return response, 200
    except SQLAlchemyError as e:
      abort(500, message='Database error - An error occured while creating an account', errors=repr(e))

@users_blp.route('/users/signout')
class UserLogout(MethodView):
  def post(self):
    response = jsonify({'message': 'Logged out'})
    
    try:
      cookie = request.cookies.get(getenv('FLASK_JWT_REFRESH_COOKIE_NAME'))
      accessToken = request.headers.get('Authorization').split(' ')[1]
      
      if not cookie:
        return jsonify({'message': 'Logged out'}), 204
      
      decodedRefreshToken = decode_token(cookie, allow_expired=True)
      if 'jti' in decodedRefreshToken:
        RevokedTokensModel.add_to_blocklist(decodedRefreshToken['jti'])
        
      decodedAccessToken = decode_token(accessToken, allow_expired=True)
      if 'jti' in decodedAccessToken:
        RevokedTokensModel.add_to_blocklist(decodedAccessToken['jti'])
    
      return response 
    except SQLAlchemyError as e:
      abort(500, message='Database error', errors=repr(e))
    except JWTDecodeError as e:
      abort(400, message='Cannot decode JWT', errors=repr(e))
    except Exception as e:
      abort(500, message='Server error - Something went wrong', errors=repr(e))
    finally:
      unset_jwt_cookies(response)