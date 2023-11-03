from datetime import datetime
import uuid
from app.utility import DBConnectivity


class Logger:

    def __init__(self,module_name,function_name, user_id= ""):
        self.__module_name = module_name
        self.__function_name = function_name
        self.__log_id = str(uuid.uuid4())
        self.__user_id = user_id
        self.__mongo = DBConnectivity.create_mongo_connection()
        self.__log = self.__mongo["logs"]

    def log(self,error,priority='high'):
        log_event = {
                "log_id": self.__log_id,
                "message": error,
                "priority" : priority, 
                "module_name" : self.__module_name,
                "function_name": self.__function_name,
                "created_at": datetime.now().isoformat(),
                "user_id" : self.__user_id
            }
        
        return self.__mongo["logs"].insert_time_series([log_event])

