from errors.application_error import ApplicationError
from commands.validation_helpers import try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class ShowRouteCommand(BaseCommand):
    """
    Command to display details of a specific route.

    This command validates the input parameter, retrieves the route by its ID,
    and returns its string representation.
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to display details of a specific route.

        Returns:
            str: The string representation of the route.

        Raises:
            ApplicationError: If no route is found with the provided ID.
        """
        super().execute()

        route_id = try_parse_int(self._params[0])
        route = self._app_data.find_route_by_id(route_id)
        if not route:
            raise ApplicationError("No Route found!")
        return str(route)

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 1