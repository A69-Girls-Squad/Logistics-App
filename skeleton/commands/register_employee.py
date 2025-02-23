from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
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
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (username, first name, last name, password, and optional role).
            app_data: The shared application data.

        Raises:
            ValueError: If the number of parameters is invalid.
        """
        validate_params_count(params, 4)
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
        self._throw_if_employee_logged_in()

        username, firstname, lastname, password, *rest = self._params

        if not rest:
            employee_role = EmployeeRole.REGULAR
        else:
            employee_role = EmployeeRole.from_string(rest[0])

        employee = self._app_data.create_employee(username, firstname, lastname, password, employee_role)
        self._app_data.login(employee)

        self.logger.info("User {employee.username} registered successfully!" + self.ROW_SEP_LONG)

        return f"Employee {employee.username} registered successfully!" + self.ROW_SEP_LONG