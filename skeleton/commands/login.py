from errors.application_error import ApplicationError
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class LoginCommand(BaseCommand):
    """
    Command to log in an employee.

    This command validates the input parameters, checks the employee's credentials,
    and logs the employee into the system.
        _requires_login (bool): Indicates whether the command requires a logged-in user (set to False for login).
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to log in an employee.

        Returns:
            str: A confirmation message indicating the employee was successfully logged in.

        Raises:
            ApplicationError: If no employee is found with the provided username or if the password is incorrect.
        """
        super().execute()
        self._throw_if_employee_logged_in()

        username, password = self._params
        employee = self._app_data.find_employee_by_username(username)
        if not employee:
            raise ApplicationError("No Employee found!" + BaseCommand.ROW_SEP)

        if employee.password != password:
            raise ApplicationError("Wrong password!")
        else:
            self._app_data.login(employee)

            self.logger.info(f"User {employee.username} successfully logged in!" + BaseCommand.ROW_SEP)
            
            return f"Employee {employee.username} successfully logged in!"

    def _requires_login(self) -> bool:
        return False

    def _expected_params_count(self) -> int:
        return 2