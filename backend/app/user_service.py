import time
from app.utility import DBConnectivity
import bcrypt

class User:
    def __init__(self, _id="", **kwargs):
        self.__id = _id
        self.__mongo = DBConnectivity.create_mongo_connection() if 'mongo_conn' not in kwargs else kwargs['mongo_conn']
        self.user_obj = self.__mongo["users"]
        if self.__id != "":
            self.user_obj = self.__mongo["users"].find_one({'_id': self.__id})

    def create_user(self, user_data):
        user_data.update({
            "status": "active",
            "created_on": time.time(),
            "updated_on": time.time()
        })
        hashed_password = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt())
        user_data.update({"password": hashed_password})
        result = self.user_obj.insert_one(user_data)
        inserted_id = result.inserted_id
        return inserted_id

    def get_user_by_id(self, user_id):
        data = self.user_obj.find_one({'_id': user_id})
        if data:
            return data
        return []
    
    def get_user_by_email(self, email):
        data = self.user_obj.find_one({'email': email})
        if data:
            return data
        return []

    def update_user(self, user_id, new_data):
        if "password" in new_data:
            hashed_password = bcrypt.hashpw(new_data["password"].encode('utf-8'), bcrypt.gensalt())
            new_data.update({"password": hashed_password})
            
        result = self.user_obj.update_one({'_id': user_id}, {'$set': new_data})
        return result.modified_count > 0

    def delete_user(self, user_id):
        result = self.user_obj.delete_one({'_id': user_id})
        return result.deleted_count > 0