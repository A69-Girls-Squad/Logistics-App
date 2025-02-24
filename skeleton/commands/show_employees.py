from errors.application_error import ApplicationError
from commands.validation_helpers import validate_params_count
from commands.base_command import BaseCommand
from core.application_data import ApplicationData
from models.constants.employee_role import EmployeeRole


class ShowEmployeesCommand(BaseCommand):

    ONLY_ADMIN_CAN_SHOW_EMPLOYEES = "You are not an admin!"

    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        super().__init__(params, app_data)

    def execute(self):
        if self._app_data.logged_in_employee.employee_role == EmployeeRole.MANAGER:
            if self._app_data.employees:
                employees = [f"{i + 1}. {str(employee)}" for i, employee in enumerate(self._app_data.employees)]
                return "\n".join(["--EMPLOYEES--"] + employees + self.ROW_SEP*2)
        else:
            raise ApplicationError(self.ONLY_ADMIN_CAN_SHOW_EMPLOYEES)