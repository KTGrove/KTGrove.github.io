#Test logic for DB connection and main functionality
#will be updated accordingly 

from app.database.animal_shelter import AnimalShelter
from config.database_config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

def main():
    #Added runtime feedback for database connectivity
    print("Starting AnimalShelter test...")

    try:
        shelter = AnimalShelter(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)

        print("Reading records...")
        animals = shelter.read_all()

        print(f"Total records found: {len(animals)}")

        for animal in animals[:5]:
            print(animal)

    except Exception as e:
        print("Application failed to run.")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()