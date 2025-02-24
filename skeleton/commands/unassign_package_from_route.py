from commands.validation_helpers import validate_params_count, try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class UnassignPackageToRouteCommand(BaseCommand):
    """
    Command to display a list of packages based on their assignment status.

    This command validates the input parameter, retrieves packages based on their status,
    and returns their string representations.
    """
    def __init__(self, params, app_data: ApplicationData):
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (a single status string: 'assigned', 'unassigned', or 'all').
            app_data: The shared application data.

        Raises:
            ValueError: If the number of parameters is invalid.
        """
        validate_params_count(params, 2)
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
        package_id = try_parse_int(self.params[0])
        route_id = try_parse_int(self.params[1])

        self.app_data.unassign_package_from_route(package_id, route_id)

        return f"Package with ID {package_id} was unassigned from route with ID {route_id}" + self.ROW_SEP*2
