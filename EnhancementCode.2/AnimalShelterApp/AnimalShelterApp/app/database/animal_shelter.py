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
    # Updated create method
    def create(self, data):
        if data is None:
            raise ValueError("Nothing to save, because data parameter is empty.")

        try:
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except PyMongoError as e:
            print(f"Create operation failed: {e}")
            return None
    
    #CRUDs read method
    # Updated read methods
    def read(self, query):
        if query is None:
            raise ValueError("No query provided, please try again.")

        try:
            return list(self.collection.find(query))
        except PyMongoError as e:
            print(f"Read operation failed: {e}")
            return []
            
    #read_all method
    def read_all(self):
        try:
            return list(self.collection.find())
        except PyMongoError as e:
            print(f"Read all operation failed {e}")
            return []
        
    
    #CRUDs update method
    # Updated update method
    def update(self, query_update, new_data): 
        if query_update is None or new_data is None:
            raise ValueError("No data provided to update.")

        try:
            result = self.collection.update_many(query_update, new_data)
            return {
                "matched_count": result.matched_count,
                "modified_count": result.modified_count
                }
        except PyMongoError as e:
            print(f"Update operation failed: {e}")
            return {"matched_count": 0, "modified_count": 0}
       
    #CRUDs delete method
    # Updated delete method
    def delete(self, query):
        if query is None:
            raise ValueError("No data provided for deletion.")

        try:
            delete_result = self.collection.delete_one(query) 
            return delete_result.deleted_count  
        except PyMongoError as e:
            print(f"Delete operation failed: {e}")
            return 0

    #Implemented read by animal type method
    def read_by_animal_type(self, animal_type):
        if not animal_type:
            raise ValueError("Animal type must be provided.")

        try:
            return list(self.collection.find({
                "animal_type": {"$regex": f"^{animal_type}$", "$options": "i"}
                }))
        except PyMongoError as e:
            print(f"Read by animal type failed: {e}")
            return []

    #Implemented read by adoption status method -
    # This filters the outcome_type
    def read_by_adoption_status(self, outcome_type):
        if not outcome_type:
            raise ValueError("Outcome type must be provided.")

        try:
            return list(self.collection.find({
                "outcome_type": {"$regex": f"^{outcome_type}$", "$options": "i"}
                }))
        except PyMongoError as e:
            print(f"Read by adoption status failed: {e}")
            return []

