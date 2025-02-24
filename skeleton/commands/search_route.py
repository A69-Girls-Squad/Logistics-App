from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, try_parse_int
from core.application_data import ApplicationData
from errors.application_error import ApplicationError
from models.route import Route


class SearchRouteCommand(BaseCommand):
    """
    Command to search for suitable routes for a specific package.

    This command validates the input parameters, searches for routes that can accommodate the package,
    and returns a formatted list of suitable routes.
    """
    def __init__(self, params, app_data: ApplicationData):
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (package ID).
            app_data: The shared application data.

        Raises:
            ValueError: If the number of parameters is invalid.
        """
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to search for suitable routes for a specific package.

        Returns:
            str: A formatted string containing details of suitable routes.

        Raises:
            ApplicationError: If the package does not exist or no suitable routes are found.
        """
        suitable_routes = []
        package_id = try_parse_int(self._params[0])
        package = self._app_data.find_package_by_id(package_id)
        if not package:
            raise ApplicationError("No package found!")
        for route in self._app_data.routes:

            sufficient_capacity = True
            if route.assigned_truck_id:
                truck = self._app_data.find_truck_by_id(route.assigned_truck_id)
                if not truck:
                    raise ApplicationError("No truck found!" + self.ROW_SEP)
                free_capacity = truck.capacity - route.load
                if free_capacity < package.weight:
                    sufficient_capacity = False

            if route.status == Route.STATUS_CREATED and sufficient_capacity:
                locations = route.locations
                if package.start_location in locations and package.end_location in locations:
                    if locations.index(package.start_location) < locations.index(package.end_location):
                        route_details = (f"ROUTE ID:       | {route.id}"
                                         f"\n{self.TABLE_SEP}"
                                         f"\nHubs:           |"
                                         f" {" -> ".join(f"{key}: "
                                         f"{value.isoformat(sep=" ", timespec="minutes")}" 
                                            for key, value in route.stops.items())}"
                                         f"\n{self.TABLE_SEP}"
                                         f"\nDeparture Time: | "
                                         f"{route.departure_time.isoformat(sep=" ", timespec="minutes")}"
                                         f"\n{self.ROW_SEP}")
                        suitable_routes.append(route_details)
        return f"SUITABLE ROUTES:\n{self.ROW_SEP}\n{self.TABLE_SEP}\n"+"\n".join(suitable_routes) + self.ROW_SEP