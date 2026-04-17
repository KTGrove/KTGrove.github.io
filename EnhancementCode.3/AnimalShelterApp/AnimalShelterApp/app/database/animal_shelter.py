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
    # Updated create method - now required to work with data validation
    def create(self, data):
        """Insert a new animal record after validation."""
        if data is None:
            raise ValueError("Nothing to save, because data parameter is empty.")

        try:
            self.validate_animal_data(data)
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except (PyMongoError, ValueError) as e:
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

    #Implemented data validation method - 
    # this ensures no empty data fields are entered
    def validate_animal_data(self, data):
        """Validate required animal fields before database insertion or update."""
        required_fields = [
            "animal_id",
            "name",
            "animal_type",
            "breed",
            "color",
            "outcome_type",
            "sex_upon_outcome",
            "age_upon_outcome_in_weeks",
            "location_lat",
            "location_long"
            ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

            if isinstance(data[field], str) and not data[field].strip():
                raise ValueError(f"Field '{field}' cannot be empty.")

        if not isinstance(data["age_upon_outcome_in_weeks"], (int, float)):
            raise ValueError("age_upon_outcome_in_weeks must be numeric.")

        if not isinstance(data["location_lat"], (int, float)):
            raise ValueError("location_lat must be numeric.")

        if not isinstance(data["location_long"], (int, float)):
            raise ValueError("location_long must be numeric.")

        return True

    #New filter implementations to sort by age and name
    def read_with_filters(self, animal_type=None, outcome_type=None):
        """Return records filtered by optional animal type and/or outcome type."""
        query = {}

        if animal_type:
            query["animal_type"] = {"$regex": f"^{animal_type.strip()}$", "$options": "i"}

        if outcome_type:
            query["outcome_type"] = {"$regex": f"^{outcome_type.strip()}$", "$options": "i"}

        try:
            return list(self.collection.find(query))
        except PyMongoError as e:
            print(f"Composite filter query failed: {e}")
            return []

    def read_all_sorted_by_name(self):
        """Return all records sorted alphabetically by name."""
        try:
            return list(self.collection.find().sort("name", 1))
        except PyMongoError as e:
            print(f"Read all sorted by name failed: {e}")
            return []

    def read_all_sorted_by_age(self):
        """Return all records sorted by age in weeks."""
        try:
            return list(self.collection.find().sort("age_upon_outcome_in_weeks", 1))
        except PyMongoError as e:
            print(f"Read all sorted by age failed: {e}")
            return []
