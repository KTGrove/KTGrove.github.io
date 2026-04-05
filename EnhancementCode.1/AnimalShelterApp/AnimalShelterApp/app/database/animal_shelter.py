from pymongo import MongoClient
from pymongo.errors import PyMongoError

class AnimalShelter:
    def __init__(self,mongo_uri, db_name, collection_name):
        #
        #3/20/2026 - changed the credentials to pull from mongo_uri instead of being hardcoded
        #Added exception handling for connection attempt, will throw error code at failure
        #
        try:
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)

            #connection test
            self.client.admin.command("ping")
            print("Successfully connected to MongoDB.")

            self.database = self.client[db_name]
            self.collection = self.database[collection_name]

        except PyMongoError as e:
            print("Database connection failed.")
            print(f"Error: {e}")
            raise
    
    #CRUDs create method
    def create(self, data):
        if data is not None:
            result = self.collection.insert_one(data)
            return True if result.inserted_id else False
        else:
            raise Exception("Nothing to save, because data parameter is empty.")
    
    #CRUDs read method
    def read(self, query):
        if query is not None:
            return self.collection.find(query)
        else:
            raise Exception("No data provided, please try again.")
            
    #read_all method
    def read_all(self):
        return list(self.collection.find())
        
    
    #CRUDs update method
    def update(self, query_update, new_data): 
        if query_update is not None and new_data is not None:
            result = self.collection.update_many(query_update, new_data)
            return result.modified_count > 0
        else: 
            raise Exception("No data provided to update.")
       
    #CRUDs delete method
    def delete(self, query):
        if query is not None:
            delete_result = self.collection.delete_one(query) 
            return delete_result.deleted_count  
        else:
            raise ValueError("No data provided for deletion.")