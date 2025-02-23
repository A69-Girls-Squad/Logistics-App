from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData


class LogoutCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        super().__init__(params, app_data)

    def execute(self):
        self._app_data.logout()

        self.logger.info("User {employee.username} successfully logged out!" + self.ROW_SEP_LONG)

        return "You logged out!" + self.ROW_SEP_LONG
