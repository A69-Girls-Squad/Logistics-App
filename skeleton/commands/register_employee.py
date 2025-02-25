from commands.base_command import BaseCommand
from core.application_data import ApplicationData
from models.constants.employee_role import EmployeeRole


class RegisterEmployeeCommand(BaseCommand):
    """
    Command to register a new employee in the application.

    This command validates the input parameters, creates a new employee, logs them in,
    and logs the action.

    Attributes:
        _requires_login (bool): Indicates whether the command requires a logged-in user (set to False for registration).
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)
        self._requires_login = False

    def execute(self) -> str:
        """
        Executes the command to register a new employee.

        Returns:
            str: A confirmation message indicating the employee was registered successfully.

        Raises:
            ApplicationError: If an employee with the same username already exists.
        """
        super().execute()
        self._throw_if_employee_logged_in()

        username, firstname, lastname, password, employee_role = self._params


        employee = self._app_data.create_employee(username, firstname, lastname, password, employee_role)
        self._app_data.login(employee)

        self.logger.info(f"User {employee.username} registered successfully!" + BaseCommand.ROW_SEP)

        return f"Employee {employee.username} registered successfully!"

    def _requires_login(self) -> bool:
        return False

    def _expected_params_count(self) -> int:
        return 5