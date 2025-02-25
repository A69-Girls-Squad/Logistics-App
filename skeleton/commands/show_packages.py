from commands.base_command import BaseCommand
from core.application_data import ApplicationData
from errors.application_error import ApplicationError
from models.constants.assign_status import AssignStatus
from interface_menu import ROW_SEP


class ShowPackagesCommand(BaseCommand):
    """
    Command to display a list of packages based on their assignment status.

    This command validates the input parameter, retrieves packages based on their status,
    and returns their string representations.
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to display packages based on their assignment status.

        Returns:
            str: A formatted string containing the details of the packages.

        Notes:
            - If the status is 'assigned', only assigned packages are displayed.
            - If the status is 'unassigned', only unassigned packages are displayed.
            - If the status is 'all', all packages are displayed.
        """
        super().execute()

        requested_status = self.params[0].lower()
        result = f"{ROW_SEP}\nPACKAGES:"

        if requested_status == AssignStatus.ASSIGNED:
            packages = self.app_data.get_packages_by_assigned_status(True)
        elif requested_status == AssignStatus.UNASSIGNED:
            packages = self.app_data.get_packages_by_assigned_status(False)
        elif requested_status == AssignStatus.ALL:
            packages = self.app_data.packages
        else:
            raise ApplicationError("Invalid input!")

        result += "\n".join(str(package) for package in packages)

        self.logger.info(result)
        return result

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 1