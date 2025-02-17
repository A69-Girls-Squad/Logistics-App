from core.application_data import ApplicationData
import json

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


