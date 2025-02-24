from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.route import Route


class ShowRoutesInProgressCommand(BaseCommand):
    """
    Command to display all routes that are currently in progress.

    This command retrieves and displays details of all routes with the status `STATUS_IN_PROGRESS`.
    """
    def __init__(self, params, app_data: ApplicationData):
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (none required).
            app_data: The shared application data.

        Raises:
            ValueError: If any parameters are provided.
        """
        validate_params_count(params, 0)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to display all routes in progress.

        Returns:
            str: A formatted string containing details of all routes in progress.

        Notes:
            - This command does not require any parameters.
            - It filters routes with the status `STATUS_IN_PROGRESS` and returns their details.
        """
        routes_in_progress = []
        for route in self._app_data.routes:
            if route.status == Route.STATUS_IN_PROGRESS:
                routes_in_progress.append(route)
        return f"Routs In Progress:\n"+"\n".join([str(route) for route in routes_in_progress]) + self.ROW_SEP_LONG
