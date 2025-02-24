from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, validate_unknown_params_count, try_parse_int
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class BulkAssignPackagesCommand(BaseCommand):
    """
    Command to assign multiple packages to a route in bulk.

    This command validates the input parameters, assigns packages to the specified route,
    and logs the action. It stops assigning packages if the route's capacity is exceeded.
    """
    def __init__(self, params, app_data: ApplicationData):
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (route ID and a list of package IDs).
            app_data: The shared application data.

        Raises:
            ValueError: If the number of parameters is invalid.
        """
        validate_unknown_params_count(params, 2, 102)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to assign multiple packages to a route.

        Returns:
            str: A confirmation message indicating which packages were assigned and if the operation was terminated due to capacity constraints.

        Raises:
            ApplicationError: If the route or any package does not exist, or if the route has no assigned truck.
        """
        bulk_assigned_packages = []
        no_more_capacity_message = ""

        route_id, *packages_ids = self._params
        route_id = try_parse_int(route_id)

        route = self._app_data.find_route_by_id(route_id)
        if not route:
            raise ApplicationError(f"No route with ID {route_id}")

        truck = self._app_data.find_truck_by_id(route.assigned_truck_id)
        if not truck:
            raise ApplicationError(f"Route with ID {route_id} has no truck assigned" + self.ROW_SEP)

        free_capacity = truck.capacity - route.load
        for package_id in packages_ids:
            package_id = try_parse_int(package_id)
            package = self.app_data.find_package_by_id(package_id)
            if not package:
                raise ApplicationError(f"No package with ID {package_id}" + self.ROW_SEP)

            if package.weight < free_capacity:
                self.app_data.assign_package_to_route(package_id, route_id)
                bulk_assigned_packages.append(package.id)
            else:
                no_more_capacity_message = "No more free capacity. Operation terminated"

                no_more_capacity_message = "No more free capacity. Operation terminated" + self.ROW_SEP

        self.logger.info(f"Bulk assigned packages to route ID {route_id}:"
                         f" {bulk_assigned_packages}\n{no_more_capacity_message}"
                         f" | Executed by: {self.app_data.logged_in_employee}"
                         f" {bulk_assigned_packages}\n{no_more_capacity_message} | Executed by: username" + self.ROW_SEP)

        return f"Bulk assigned packages to route ID {route_id}: {bulk_assigned_packages}\n{no_more_capacity_message}" + self.ROW_SEP*2