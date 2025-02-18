from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, try_parse_int
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class UnassignPackageToRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        super().__init__(params, app_data)

    def execute(self):
        package_id = try_parse_int(self.params[0])
        route_id = try_parse_int(self.params[1])

        route = self.app_data.find_route_by_id(route_id)
        assigned_package = route.find_assigned_package_by_id(package_id)

        route.unassign_package(assigned_package)

        return f"Package with ID {assigned_package.id} was assigned to Route with ID {route.id}"