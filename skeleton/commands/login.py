from errors.application_error import ApplicationError
from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData


class LoginCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        super().__init__(params, app_data)
        self._requires_login = False


    def execute(self):
        self._throw_if_employee_logged_in()

        username, password = self._params
        employee = self._app_data.find_employee_by_username(username)
        if not employee:
            raise ApplicationError("No employee found!" + self.SEP)

        if employee.password != password:
            raise ApplicationError("Wrong username or password!" + self.SEP)
        else:
            self._app_data.login(employee)

            self.logger.info("User {employee.username} successfully logged in!" + self.SEP)
            
            return f"Employee {employee.username} successfully logged in!" + self.SEP