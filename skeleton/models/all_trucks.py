import json
from skeleton.models.truck import Truck

class AllTrucks:
    def __init__(self):
        self.mydata = "trucks.json"
        self.trucks = self.load_trucks()

    def load_trucks(self):
        with open(self.mydata, 'r') as file:
            all_trucks = json.load(file)
            return [Truck.from_json(truck) for truck in all_trucks["trucks"]]
        
    def save_trucks(self):
        with open(self.mydata, "w") as file:
            json.dump({"trucks": [truck.to_json() for truck in self.trucks]}, file, indent=4)

    def get_all_trucks(self):
        return self.trucks