from core.application_data import ApplicationData
import json


FILE_NAME = 'app_state.json'

class ApplicationState:

    @classmethod
    def save_data(cls, app_data: ApplicationData):
        """
        Saves the application data to a file in JSON format.

        Args:
            app_data (ApplicationData): An instance of ApplicationData containing the data to be saved.
        """
        data = app_data.to_json()
        with open(FILE_NAME, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_data(cls):
        """
        Loads application data from a JSON file and returns an ApplicationData instance.

        Returns:
            ApplicationData: An instance of ApplicationData populated with the loaded data.
        """
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)
        return ApplicationData.from_json(data)

    @classmethod
    def seed_data(cls,app_data: ApplicationData):
        for first_vehicle in range(10):
            app_data.create_truck("Scania", 42000, 8000)
        for second_vehicle in range(15):
            app_data.create_truck("Man", 37000, 10000)
        for third_vehicle in range(15):
            app_data.create_truck("Actros", 26000, 13000)

