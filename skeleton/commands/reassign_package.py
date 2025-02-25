from commands.validation_helpers import validate_params_count, try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class ReassignPackageCommand(BaseCommand):
    """
    Command to reassign a package from one route to another.

    This command validates the input parameters, unassigns the package from the current route,
    assigns it to the new route, and logs the action.
    """
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to reassign a package from one route to another.

        Returns:
            str: A confirmation message indicating the package was reassigned.

        Raises:
            ApplicationError: If the package or routes do not exist, or if the package cannot be reassigned.
        """
        package_id = try_parse_int(self.params[0])
        package = self.app_data.find_package_by_id(package_id)
        unassign_from_route_id = package.route_id
        assign_to_route_id = try_parse_int(self.params[1])

        self.app_data.unassign_package_from_route(package_id)

        self.app_data.assign_package_to_route(package_id, assign_to_route_id)

        self.logger.info(f"Package with ID {package_id} reassigned from Route {unassign_from_route_id} "
                         f"to Route {assign_to_route_id} | Executed by: {self.app_data.logged_in_employee}")

        return (f"Package with ID {package_id} was unassigned from Route with ID {unassign_from_route_id}"
                f"and was assigned to Route with ID {assign_to_route_id}")
