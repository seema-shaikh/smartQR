import datetime
import uuid
from dotenv import load_dotenv

import bcrypt
import jwt

from flask import jsonify
from flask_jwt_extended import get_jwt_identity 

from app.conf.config import app
from app.user_service import User
from app.utility import DBConnectivity 
from app.utility import response

load_dotenv()
class UserOps():
    
    def _register(self, data):

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

    def _login(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        print("DDD")
        mongo = DBConnectivity.create_mongo_connection()
        existing_user = User(mongo_conn=mongo).get_user_by_email(email)
        if existing_user and bcrypt.checkpw(password.encode('utf-8'), existing_user['password']):
            payload = {
                'sub': str(existing_user['_id']),  
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
            }

            token = jwt.encode(payload, str(app.config['SECRET_KEY']), algorithm='HS256')
            return jsonify({"message": "User logged in successfully", 'token': token })
        
        return jsonify({'message': 'Authentication failed'}), 401

    def _delete_user(self, data):
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

    def _user_details(self):

        current_user_id= get_jwt_identity()
        mongo = DBConnectivity.create_mongo_connection()
        existing_user = User(mongo_conn=mongo).get_user_by_id(current_user_id)
        if not existing_user:
            return {"message" : "Error"}
        
        selected_keys = ["_id", "created_on", "updated_on", "password"]
        user_info = {key: value for key, value in existing_user.items() if key not in selected_keys}
        return {"message": "Successful Response", "data": user_info}

    def _update_user(self, data):
        mongo = DBConnectivity.create_mongo_connection()
        current_user_id= get_jwt_identity()
        existing_user = User(mongo_conn=mongo).update_user(current_user_id, data)
        if not existing_user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify({'message': 'User updated successfully', "data": existing_user}), 200
