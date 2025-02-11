from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData


class LogoutCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        super().__init__(app_data)
        self._params = params

    def execute(self):
        self._app_data.logout()

        return 'You logged out!'
