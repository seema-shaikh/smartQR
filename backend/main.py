import datetime
import traceback
import bcrypt
from flask import Flask, jsonify, request
from app.user_service import User
import json
from app.utility import response
from app.utility import DBConnectivity 
import time 
import uuid
from app.utility import GenericOps
import jwt
import os
from dotenv import load_dotenv

from app.utility import Logger
load_dotenv()
from flask_jwt_extended import JWTManager, jwt_required , get_jwt_identity 


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_SECRET_KEY'] = str(app.config['SECRET_KEY'])
    # app.config['DEBUG'] = os.environ.get('DEBUG', default=False)
    # app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL')
    return app

app = create_app() 
jwt_manager = JWTManager(app) 

@app.route("/user/signup", methods= ["POST"])
def user_signup():
    try:
        data = json.loads(request.data)
        if not data:
            return response.invalidRequestResponse()

        email = data.get("email")
        if not email:
            return response.emailRequiredResponse()

        mongo = DBConnectivity.create_mongo_connection()
        existing_user = User(mongo_conn=mongo).get_user_by_email(email)
        if existing_user:
            return response.existingUserResponse()

        user_data = {
            "_id": str(uuid.uuid4()),
            "full_name" : data["full_name"],
            "age" : data["age"],
            "email" : data["email"],
            "gender": data["gender"],
            "state" : data["state"] if "state" in data else "",
            "phone_number": data["phone_number"],
            "profile_pic"  : data["profile_pic"],
            "password" : data["password"]
            }

        id = User(mongo_conn = mongo).create_user(user_data)
        if id:
            return {"message": "User signed up successfully", "status": 200 }
        return {"message": "User could not be registered", 'status': 400 }
    except:
        log = Logger(module_name="/user/signup", function_name="user_signup()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")
    
@app.route("/user/login", methods= ["POST"])
def user_login():
    try:
        # verify headers
        headers = request.headers
        message, status = GenericOps.handle_content_type(request)
        if status == 400:
            return {"message": message, "status" : status }
        
        data = json.loads(request.data)
        email = data.get("email")
        password = data.get("password")

        mongo = DBConnectivity.create_mongo_connection()
        existing_user = User(mongo_conn=mongo).get_user_by_email(email)
        if existing_user and bcrypt.checkpw(password.encode('utf-8'), existing_user['password']):
            # token = jwt.encode({'user_id': str(existing_user['_id']), 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, str(app.config['SECRET_KEY']))
            payload = {
                'sub': str(existing_user['_id']),  
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
            }

            token = jwt.encode(payload, str(app.config['SECRET_KEY']), algorithm='HS256')
            return jsonify({"message": "User logged in successfully", 'token': token })
        
        return jsonify({'message': 'Authentication failed'}), 401

    except:
        log = Logger(module_name="/user/login", function_name="user_login()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")

@app.route("/user/delete/account", methods = ["POST"])
@jwt_required()
def delete_user_account():
    try:
        data = json.loads(request.data)
        email = data.get("email")
        password = data.get("password")

        if not email and password:
            return jsonify({'message': 'Username and Password is required'}), 400

        mongo = DBConnectivity.create_mongo_connection()
        existing_user = User(mongo_conn=mongo).get_user_by_email(email)
        if not existing_user:
            return jsonify({'message': 'User not found'}), 404

        existing_user = User(mongo_conn=mongo).delete_user(existing_user["_id"])
        return jsonify({'message': 'User deleted successfully'}), 200

    except:
        log = Logger(module_name="/user/delete/account", function_name="delete_user_account()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")
    
@app.route("/user/personal/accountsinfo", methods = ["GET"])
@jwt_required()
def get_user_info():
    try:
        current_user_id= get_jwt_identity()
        mongo = DBConnectivity.create_mongo_connection()
        existing_user = User(mongo_conn=mongo).get_user_by_id(current_user_id)
        if not existing_user:
            return {"message" : "Error"}
        
        selected_keys = ["_id", "created_on", "updated_on", "password"]
        user_info = {key: value for key, value in existing_user.items() if key not in selected_keys}
        return {"message": "Successful Response", "data": user_info}
    except:
        log = Logger(module_name="/user/personal/accountsinfo", function_name="get_user_info()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")
    
@app.route("/user/update/profile", methods = ["POST"])
@jwt_required()
def user_update_profile():
    try:
        data = json.loads(request.data)

        mongo = DBConnectivity.create_mongo_connection()
        current_user_id= get_jwt_identity()
        existing_user = User(mongo_conn=mongo).update_user(current_user_id, data)
        if not existing_user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({'message': 'User updated successfully', "data": existing_user}), 200
    except:
        log = Logger(module_name="/user/update/profile", function_name="user_update_profile()")
        log.log(traceback.format_exc())
        return response.errorResponse("Some error occured please try again!")

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5200, debug = True )

