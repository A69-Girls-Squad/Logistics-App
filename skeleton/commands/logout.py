from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class LogoutCommand(BaseCommand):
    """
    Command to log out the currently logged-in employee.

    This command logs out the employee and returns a confirmation message.
    """
    def __init__(self, params, app_data: ApplicationData):
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
        super().execute()
        username = self.app_data.logged_in_employee.username
        self._app_data.logout()

        self.logger.info(f"User {username} successfully logged out!" + BaseCommand.ROW_SEP)

        return "You logged out!"

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 0
