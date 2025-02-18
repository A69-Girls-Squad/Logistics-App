from skeleton.commands.base_command import BaseCommand
from skeleton.commands.validation_helpers import validate_params_count, try_parse_int
from skeleton.core.application_data import ApplicationData
from skeleton.errors.application_error import ApplicationError


class AssignPackageToRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        super().__init__(params, app_data)

    def execute(self):
        package_id = try_parse_int(self.params[0])
        route_id = try_parse_int(self.params[1])

        package = self.app_data.find_package_by_id(package_id)
        if package is None:
            raise ApplicationError(f"Package with ID {package_id} does not exist")

        route = self.app_data.find_route_by_id(route_id)
        if route is None:
            raise ApplicationError(f"Route with ID {route_id} does not exist")

        route.assign_package(package)

        return f"Package with ID {package.id} was assigned to Route with ID {route.id}"