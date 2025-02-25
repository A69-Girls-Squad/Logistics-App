from errors.application_error import ApplicationError
from commands.base_command import BaseCommand
from core.application_data import ApplicationData
from models.constants.employee_role import EmployeeRole
from interface_menu import TABLE_SEP, ROW_SEP


class ShowEmployeesCommand(BaseCommand):
    """Command for displaying a list of employees.

    Only users with the 'MANAGER' role can execute this command.
    If the logged-in user is not a manager, an ApplicationError is raised.

    Attributes:
        ONLY_MANAGER_CAN_SHOW_EMPLOYEES (str): Error message when a non-manager tries to access employees.
    """

    ONLY_MANAGER_CAN_SHOW_EMPLOYEES = "You are not a Manager!"

    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        """Execute the command to show employees.

        If the logged-in employee has a 'MANAGER' role and employees exist,
        it returns a formatted list of employees. Otherwise, raises an ApplicationError.

        Returns:
            str: A formatted string listing employees.

        Raises:
            ApplicationError: If the logged-in user is not a manager.
        """
        super().execute()

        if self._app_data.logged_in_employee.employee_role == EmployeeRole.MANAGER:
            if self._app_data.employees:
                employees = [f"{ROW_SEP}\n{str(employee)}\n{ROW_SEP}"
                             for i, employee in enumerate(self._app_data.employees)]
                return f"{ROW_SEP}\n" + "\n".join(["EMPLOYEES:"] + employees)
        else:
            raise ApplicationError(self.ONLY_MANAGER_CAN_SHOW_EMPLOYEES)

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 0
