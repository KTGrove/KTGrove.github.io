#Test logic for DB connection and main functionality
#will be updated accordingly 

from app.database.animal_shelter import AnimalShelter
from config.database_config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

def main():
    #Added runtime feedback for database connectivity
    print("Starting AnimalShelter CRUD test...\n")
   
    try:
        shelter = AnimalShelter(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)

        # Read all test
        print("Reading records...")
        animals = shelter.read_all()
        print(f"Total records found: {len(animals)}\n")

        # Create method test
        print("Creating test record...")
        test_animal = {
            "animal_id": "Test1",
            "name": "Samwise",
            "animal_type": "Dog",
            "breed": "Golden Retriever",
            "color": "Brown",
            "outcome_type": "Available",
            "sex_upon_outcome": "Neutered Male",
            "age_upon_outcome_in_weeks": 85,
            "location_lat": 30.69,
            "location_long": -97.42
            }

        inserted_id = shelter.create(test_animal)
        print(f"Inserted record ID: {inserted_id}\n")

        # Read one method test
        print("Reading test record...")
        results = shelter.read({"animal_id": "Test1"})
        print(f"Records returned: {len(results)}")
        for animal in results:
            print(animal)
        print()

        # Update method test
        print("Updating test record...")
        update_result = shelter.update(
            {"animal_id": "Test1"},
            {"$set": {"outcome_type": "Adoption Pending"}}
        )
        print(f"Update result: {update_result}\n")

        # Verifies update
        print("Verifying updated record...")
        updated_results = shelter.read({"animal_id": "Test1"})
        for animal in updated_results:
            print(animal)
        print()

        # Delete method test
        print("Deleting test record...")
        deleted_count = shelter.delete({"animal_id": "Test1"})
        print(f"Deleted records: {deleted_count}\n")

        # Verifies delete
        print("Verifying deletion...")
        final_check = shelter.read({"animal_id": "Test1"})
        print(f"Remaining records with animal_id Test1: {len(final_check)}")

        # Test read_by_animal_type and read_by_adoption_status methods
        print("\n=== Animal Type Tests ===")

        dogs = shelter.read_by_animal_type("Dog")
        print(f"Dogs found: {len(dogs)}")
        for dog in dogs:
            print(f"Dog: {dog.get('name')}")

        cats = shelter.read_by_animal_type("Cat")
        print(f"Cats found: {len(cats)}")
        for cat in cats:
            print(f"Cat: {cat.get('name')}")

        print("\n=== Outcome Type Tests ===")
        
        adopted = shelter.read_by_adoption_status("Adoption")
        print(f"Adoption records: {len(adopted)}")
        for animal in adopted:
            print(f"{animal.get('name')} - {animal.get('outcome_type')}")

        rescue = shelter.read_by_adoption_status("Rescue")
        print(f"Rescue records: {len(rescue)}")
        for animal in rescue:
            print(f"{animal.get('name')} - {animal.get('outcome_type')}")


    except Exception as e:
        print("Application failed to run.")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()