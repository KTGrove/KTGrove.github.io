from pymongo import MongoClient

def seed_database():
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["animal_shelter"]
        collection = db["animals"]

        # Clear existing data - to avoid duplicates
        collection.delete_many({})

        # Seed data (LOTR themed for fun)
        # Lat and long coordinates are changed by .01 each -
        # this indicates animals are in the same shelter, just different kennels/cages
        # Animal IDs have been simplified for the purposes of test data - 
        # could be better improved for future functionality and scalability
        animals = [
            {
                "animal_id": "A1",
                "name": "Frodo",
                "animal_type": "Dog",
                "breed": "Shi Tzu",
                "color": "Black",
                "outcome_type": "Adoption",
                "sex_upon_outcome": "Neutered Male",
                "age_upon_outcome_in_weeks": 104,
                "location_lat": 30.75,
                "location_long": -97.48
                },
            {
                "animal_id": "A2",
                "name": "Aragorn",
                "animal_type": "Dog",
                "breed": "German Shepherd",
                "color": "Brown/Black",
                "outcome_type": "Adoption",
                "sex_upon_outcome": "Neutered Male",
                "age_upon_outcome_in_weeks": 143,
                "location_lat": 30.74,
                "location_long": -97.47
                },
            {
                "animal_id": "A3",
                "name": "Arwen",
                "animal_type": "Cat",
                "breed": "Domestic Shorthair Mix",
                "color": "Gray",
                "outcome_type": "Transfer",
                "sex_upon_outcome": "Spayed Female",
                "age_upon_outcome_in_weeks": 54,
                "location_lat": 30.73,
                "location_long": -97.46
                },
            {
                "animal_id": "A4",
                "name": "Legolas",
                "animal_type": "Cat",
                "breed": "Ragdoll",
                "color": "White/Gray",
                "outcome_type": "Adoption",
                "sex_upon_outcome": "Neutered Male",
                "age_upon_outcome_in_weeks": 88,
                "location_lat": 30.72,
                "location_long": -97.45
                },
            {
                "animal_id": "A5",
                "name": "Bomber",
                "animal_type": "Dog",
                "breed": "Corgi",
                "color": "Orange/White",
                "outcome_type": "Rescue",
                "sex_upon_outcome": "Neutered Male",
                "age_upon_outcome_in_weeks": 67,
                "location_lat": 30.71,
                "location_long": -97.44
                },
            {
                "animal_id": "A6",
                "name": "Gimli",
                "animal_type": "Dog",
                "breed": "French Bulldog",
                "color": "Black/White",
                "outcome_type": "Adoption",
                "sex_upon_outcome": "Neutered Male",
                "age_upon_outcome_in_weeks": 97,
                "location_lat": 30.70,
                "location_long": -97.43
                },
            ]

        # Prevents duplicate animal IDs
        collection.create_index("animal_id", unique=True)
        
        # Insert data
        result = collection.insert_many(animals)

        print(f"Inserted {len(result.inserted_ids)} records into animal_shelter.animals")
        print("Database reset and seeded successfully.")

    except Exception as e:
        print("Error seeding database:", e)

if __name__=="__main__":
    seed_database()