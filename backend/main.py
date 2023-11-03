import json
import traceback
from dotenv import load_dotenv
from flask import jsonify, request
from flask_jwt_extended import jwt_required 
from marshmallow.exceptions import ValidationError

from app.conf.config import app
from app.conf.decorators import header_required
from app.resolvers.UserOperations import UserOps
from app.utility import Logger
from app.utility import response
from app.validators.user_validations import UserRegisterationSchema, UserLoginSchema, UpdateProfileSchema,  DeleteAccountSchema

load_dotenv()

@app.route("/user/signup", methods= ["POST"])
@header_required(request)
def user_signup():
    try:
        data = json.loads(request.data)
        schema = UserRegisterationSchema()
        validated_data = schema.load(data)
        return UserOps()._register(validated_data)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400  
    except:
        log = Logger(module_name="/user/signup", function_name="user_signup()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")
    

@app.route("/user/login", methods= ["POST"])
@header_required(request)
def user_login():
    try:
        data = json.loads(request.data)
        schema = UserLoginSchema()
        validated_data = schema.load(data)
        return UserOps()._login(validated_data)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400 
    except:
        print(traceback.format_exc())
        log = Logger(module_name="/user/login", function_name="user_login()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")
    

@app.route("/user/delete/account", methods = ["POST"])
@header_required(request)
@jwt_required()
def delete_user_account():
    try:
        data = json.loads(request.data)
        schema = DeleteAccountSchema()
        validated_data = schema.load(data)
        return UserOps()._delete_user(validated_data)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400 
    except:
        log = Logger(module_name="/user/delete/account", function_name="delete_user_account()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")
    
@app.route("/user/personal/accountsinfo", methods = ["GET"])
@header_required(request)
@jwt_required()
def get_user_info():
    try:
        return UserOps()._user_details()
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400 
    except:
        log = Logger(module_name="/user/personal/accountsinfo", function_name="get_user_info()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")

    
@app.route("/user/update/profile", methods = ["POST"])
@header_required(request)
@jwt_required()
def user_update_profile():
    try:
        data = json.loads(request.data)
        schema = UpdateProfileSchema()
        validated_data = schema.load(data)
        print(validated_data)
        return UserOps()._update_user(validated_data)
    except:
        log = Logger(module_name="/user/update/profile", function_name="user_update_profile()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5200, debug = True )

