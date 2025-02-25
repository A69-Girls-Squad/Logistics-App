from commands.validation_helpers import try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class UnassignPackageFromRouteCommand(BaseCommand):
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

        package_id = try_parse_int(self.params[0])
        package = self.app_data.find_package_by_id(package_id)
        route_id = package.route_id

        self.app_data.unassign_package_from_route(package_id)

        return f"Package with ID {package_id} was unassigned from Route with ID {route_id}"

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 1