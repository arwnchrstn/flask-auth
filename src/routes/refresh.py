from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, create_access_token, decode_token
from flask_jwt_extended.exceptions import JWTDecodeError
from flask import request, jsonify
from dotenv import load_dotenv
from os import getenv
from datetime import timedelta
from src.schemas import RefreshTokenSchema

load_dotenv()

refresh_blp = Blueprint('Refresh', __name__)

@refresh_blp.route('/refresh')
class Refresh(MethodView):
  @jwt_required(locations=['cookies'], refresh=True)
  @refresh_blp.response(200, RefreshTokenSchema)
  def post(self):
    try:
      refreshToken = request.cookies.get(getenv('FLASK_JWT_REFRESH_COOKIE_NAME'))
      
      if not refreshToken:
        abort(401, message='Missing refresh token')
        
      decodedToken = decode_token(refreshToken)
      identity = decodedToken['sub']
      
      access_token = create_access_token(identity=identity, expires_delta=timedelta(minutes=10))
      
      return jsonify({'access_token': access_token})
    except JWTDecodeError as e:
      abort(400, message='Cannot decode token', errors=repr(e))
    except Exception as e:
      abort(500, message='Server error - Something went wrong', errors=repr(e))