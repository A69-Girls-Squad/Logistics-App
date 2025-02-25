from commands.validation_helpers import validate_params_count, try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class AssignPackageToRouteCommand(BaseCommand):
    """
    Command to assign a package to a specific route.

    This command validates the input parameters, assigns a package to a route,
    and logs the action.
    """
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to assign a package to a route.

        Returns:
            str: A confirmation message indicating the package was assigned to the route.

        Raises:
            ValueError: If the package ID or route ID is invalid.
        """
        super().execute()
        package_id = try_parse_int(self.params[0])
        route_id = try_parse_int(self.params[1])

        self.app_data.assign_package_to_route(package_id, route_id)
        
        self.logger.info(
            f"Package with ID {package_id} was assigned to route with ID {route_id} "
            f"| Executed by: {self.app_data.logged_in_employee}"
            )

        return f"Package with ID {package_id} was assigned to route with ID {route_id}"

    def _requires_login(self) -> bool:
        return True