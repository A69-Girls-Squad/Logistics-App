from commands.validation_helpers import validate_params_count
from commands.base_command import BaseCommand
from core.application_data import ApplicationData
from errors.application_error import ApplicationError
from models.route import Route


class ShowRoutesCommand(BaseCommand):
    """
    Command to display all routes that are currently in progress.

    This command retrieves and displays details of all routes with the status `STATUS_IN_PROGRESS`.
    """
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
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

        requested_status = self.params[0].capitalize()

        if requested_status in [Route.STATUS_CREATED, Route.STATUS_IN_PROGRESS, Route.STATUS_FINISHED]:
            routes_to_show = self.app_data.get_routes_by_status(requested_status)

        elif requested_status.lower() == "all":
            routes_to_show = self.app_data.routes

        else:
            raise ApplicationError("Invalid input!")

        return f"{requested_status.upper()} ROUTES:\n"+"\n".join([str(route) for route in routes_to_show])
