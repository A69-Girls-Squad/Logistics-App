from errors.application_error import ApplicationError
from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData


class ShowEmployeesCommand(BaseCommand):

    ONLY_ADMIN_CAN_SHOW_EMPLOYEES = "You are not an admin!"

    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        super().__init__(params, app_data)

    def execute(self):
        if self._app_data.logged_in_employee.is_admin:
            if self._app_data.employees:
                employees = [f"{i + 1}. {str(employee)}" for i, employee in enumerate(self._app_data.employees)]
                return "\n".join(["--EMPLOYEES--"] + employees)
        else:
            raise ApplicationError(self.ONLY_ADMIN_CAN_SHOW_EMPLOYEES)