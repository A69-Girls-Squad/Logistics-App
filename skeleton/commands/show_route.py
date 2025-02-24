from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, try_parse_int
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class ShowRouteCommand(BaseCommand):
    """
    Command to display details of a specific route.

    This command validates the input parameter, retrieves the route by its ID,
    and returns its string representation.
    """
    def __init__(self, params, app_data: ApplicationData):
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (a single route ID).
            app_data: The shared application data.

        Raises:
            ValueError: If the number of parameters is invalid.
        """
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to display details of a specific route.

        Returns:
            str: The string representation of the route.

        Raises:
            ApplicationError: If no route is found with the provided ID.
        """
        route_id = try_parse_int(self._params[0])
        route = self._app_data.find_route_by_id(route_id)
        if not route:
            raise ApplicationError("No route found!")
        return str(route)