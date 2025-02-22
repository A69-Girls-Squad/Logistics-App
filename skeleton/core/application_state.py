from core.application_data import ApplicationData
import json

from errors.application_error import ApplicationError

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
        try:
            with open(FILE_NAME, 'r') as f:
                data = json.load(f)
                return ApplicationData.from_json(data)
        except FileNotFoundError:
            return

    @classmethod
    def seed_data(cls, app_data: ApplicationData):
        """
        Seeds the given ApplicationData object with sample truck data.

        This method adds a set number of trucks of different types (Scania, Man, Actros) to the provided app_data instance.
        Specifically, it adds 10 Scania trucks, 15 Man trucks, and 15 Actros trucks with pre-defined weights and capacities.
        This is useful for initializing `app_data` with test data, typically for development or testing purposes.

        Args:
            app_data (ApplicationData): An instance of the ApplicationData class where the trucks will be added.

        Returns:
            None: This method modifies the app_data instance in place and does not return a value.
        """
        for i in range(10):
            app_data.create_truck("Scania", 42000, 8000)
        for i in range(15):
            app_data.create_truck("Man", 37000, 10000)
        for i in range(15):
            app_data.create_truck("Actros", 26000, 13000)
