from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.constants.employee_role import EmployeeRole


class RegisterEmployeeCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 4)
        super().__init__(app_data)
        self._params = params
        self._requires_login = False

    def execute(self):
        self._throw_if_employee_logged_in()

        username, firstname, lastname, password, *rest = self._params

        if not rest:
            employee_role = EmployeeRole.REGULAR
        else:
            employee_role = EmployeeRole.from_string(rest[0])

        employee = self._app_data.create_employee(username, firstname, lastname, password, employee_role)
        self._app_data.login(employee)

        self.logger.info('User {employee.username} registered successfully!')

        return f'Employee {employee.username} registered successfully!'