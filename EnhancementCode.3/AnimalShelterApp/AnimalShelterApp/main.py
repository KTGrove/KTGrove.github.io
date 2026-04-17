#Simplistic main method for time being
from app.database.animal_shelter import AnimalShelter
from config.database_config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME


def main():
    print("Starting AnimalShelter application...\n")

    try:
        shelter = AnimalShelter(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)
        animals = shelter.read_all()
        print(f"Connected successfully. Total animals in database: {len(animals)}")

    except Exception as e:
        print("Application failed to run.")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()