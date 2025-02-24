from commands.validation_helpers import validate_params_count
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class LogoutCommand(BaseCommand):
    """
    Command to log out the currently logged-in employee.

    This command logs out the employee and returns a confirmation message.
    """
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to log out the currently logged-in employee.

        Returns:
            str: A confirmation message indicating the employee was logged out.

        Notes:
            - This command does not require any parameters.
            - It logs out the currently logged-in employee and updates the application state.
        """
        self._app_data.logout()

        self.logger.info(f"User {self.app_data.logged_in_employee.username} successfully logged out!" + BaseCommand.ROW_SEP)

        return "You logged out!" + BaseCommand.ROW_SEP*2
