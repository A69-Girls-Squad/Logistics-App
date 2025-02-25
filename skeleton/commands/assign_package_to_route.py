from commands.validation_helpers import try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class AssignPackageToRouteCommand(BaseCommand):
    """
    A command to assign a package to a specific route.

    This command takes a package ID and a route ID as parameters, validates them,
    and assigns the package to the specified route. The action is logged, and a
    confirmation message is returned.

    Attributes:
        params (list): A list of parameters passed to the command. The first parameter
                       should be the package ID, and the second should be the route ID.
        app_data (ApplicationData): The application data object containing the state
                                    of the application.

    Methods:
        execute(): Executes the command to assign the package to the route and logs
                   the action. Returns a confirmation message.
        _requires_login(): Specifies that the command requires the user to be logged in.
        _expected_params_count(): Specifies the expected number of parameters (2).
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        super().execute()

        route_id = try_parse_int(self.params[0])
        package_id = try_parse_int(self.params[1])

        self.app_data.assign_package_to_route(package_id, route_id)
        
        self.logger.info(
            f"Package with ID {package_id} was assigned to Route with ID {route_id} "
            f"| Executed by: {self.app_data.logged_in_employee}"
            )

        return f"Package with ID {package_id} was assigned to Route with ID {route_id}"

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 2