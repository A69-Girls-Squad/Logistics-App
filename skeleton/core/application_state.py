from core.application_data import ApplicationData
import json

from models.truck import Truck

FILE_NAME = 'app_state.json'

class ApplicationState:

    @classmethod
    def save_data(cls, app_data: ApplicationData):
        data = app_data.to_json()
        with open(FILE_NAME, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_data(cls):
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)
        return ApplicationData.from_json(data)

    @classmethod
    def seed_data(cls,app_data: ApplicationData):
        for first_vehicle in range(10):
            vehicle = Truck("Scania", 42000, 8000)

        for second_vehicle in range(15):
            vehicle = Truck("Man", 37000, 10000)

        for third_vehicle in range(15):
            vehicle = Truck("Actros", 26000, 13000)



