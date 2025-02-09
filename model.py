import json
import random

class Pet:
    def __init__(self, pet_type, last_health_check, vaccines_received):
        self.id = self.generate_pet_id()
        self.type = pet_type
        self.last_health_check = last_health_check  
        self.vaccines_received = vaccines_received

    def generate_pet_id(self):
        return random.randint(10000000, 99999999)

class Phoenix(Pet):
    def __init__(self, last_health_check, vaccines_received, fire_proof_certified):
        super().__init__("Phoenix", last_health_check, vaccines_received)
        self.fire_proof_certified = fire_proof_certified

class Dragon(Pet):
    def __init__(self, last_health_check, vaccines_received, smoke_pollution_level):
        super().__init__("Dragon", last_health_check, vaccines_received)
        self.smoke_pollution_level = smoke_pollution_level

class Owl(Pet):
    def __init__(self, last_health_check, vaccines_received, flight_distance):
        super().__init__("Owl", last_health_check, vaccines_received)
        self.flight_distance = flight_distance

def save_to_json(pet):
    file_path = "pets.json"
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            pets_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pets_data = []
    
    pets_data.append(pet.__dict__)
    
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(pets_data, file, indent=4)

def get_accepted_pets_report():
    file_path = "pets.json"
    pet_counts = {"Phoenix": 0, "Dragon": 0, "Owl": 0}
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            pets_data = json.load(file)
            for pet in pets_data:
                if pet["type"] in pet_counts:
                    pet_counts[pet["type"]] += 1
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    return pet_counts
