from errors.application_error import ApplicationError
from commands.validation_helpers import validate_unknown_params_count, try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class BulkAssignPackagesCommand(BaseCommand):
    """
    Command to assign multiple packages to a route in bulk.

    This command validates the input parameters, assigns packages to the specified route,
    and logs the action. It stops assigning packages if the route's capacity is exceeded.
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to assign multiple packages to a route.

        Returns:
            str: A confirmation message indicating which packages were assigned and
            if the operation was terminated due to capacity constraints.

        Raises:
            ApplicationError: If the route or any package does not exist, or if the route has no assigned truck.
        """
        validate_unknown_params_count(self._params, min_count=2, max_count=102)

        if self._requires_login() and not self._app_data.has_logged_in_employee:
            self.logger.warning("Unauthorized access attempt detected.")
            raise ValueError("You are not logged in! Please login first!" + BaseCommand.ROW_SEP)

        bulk_assigned_packages = []

        route_id, packages_ids = self._params
        route_id = try_parse_int(route_id)
        packages_ids = map(int, packages_ids)

        route = self._app_data.find_route_by_id(route_id)

        if not route:
            raise ApplicationError(f"No Route with ID {route_id}")

        for package_id in packages_ids:
            self.app_data.assign_package_to_route(package_id, route_id)
            bulk_assigned_packages.append(package_id)


        self.logger.info(f"Bulk assigned Packages to Route ID {route_id}:"
                         f" {bulk_assigned_packages}"
                         f" | Executed by: {self.app_data.logged_in_employee}")

        return (f"Bulk assigned Packages to Route ID {route_id}: "
                f"{bulk_assigned_packages}")

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 0