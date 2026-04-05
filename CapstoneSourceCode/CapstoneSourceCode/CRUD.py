from pymongo import MongoClient     #1 - ObjectID is imported but not used in this file.
from bson.objectid import ObjectId  #TODO: Remove unused imports.

class AnimalShelter:
    def __init__(self, USER, PASS, HOST, PORT, DB, COL):
        #2 - Constructor accepts parameters but are overwritten below.
        #TODO: Use the parameters to load in secure credentials from an external source.
        #This will also remove the hardcoded account credentials below as well as the 
        #hardcoded database and collection.

        #initializes mongo client with the aacuser account credentials
        USER = 'aacuser'
        PASS = 'agkg1022'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 34129
        DB = 'AAC'
        COL = 'animals'
        #
        #initializes connection 
        #
        self.client = MongoClient(f'mongodb://{USER}:{PASS}@{HOST}:{PORT}')
        # 3 - There is no exception handling for database connection failures.
        #TODO: Wrap in try/except and return error messages/logs.

        self.database = self.client[DB]
        self.collection = self.database[COL]
    
    #CRUDs create method
    # 4 - Method currently returns only a BOOLEAN
    # TODO: Implement ID return and/or more descriptive result. 
    def create(self, data):
        if data is not None:
            result = self.collection.insert_one(data)
            return True if result.inserted_id else False
        else:
            raise Exception("Nothing to save, because data parameter is empty.")
    
    #CRUDs read method
    # 5 - This returns a cursor while read_all returns a list.
    # TODO: Standardize return types; consider limits for return_all to better handle scalability potential.
    def read(self, query):
        if query is not None:
            return self.collection.find(query)
        else:
            raise Exception("No data provided, please try again.")
            
    #read_all method implemented for Mod. 6 Milestone
    def read_all(self):
        return list(self.collection.find())
        
    
    # 6 - For remaining methods below:
    # Update method could be adjusted to return more detailed update results instead of success/failure.
    # Currently only have delete_one implemented, delete_many may be of use for larger operations.

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