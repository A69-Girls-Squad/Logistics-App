from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, try_parse_int
from core.application_data import ApplicationData


class AssignPackageToRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        super().__init__(params, app_data)

    def execute(self):
        package_id = try_parse_int(self.params[0])
        route_id = try_parse_int(self.params[1])

        self.app_data.assign_package_to_route(package_id, route_id)

        return f"Package with ID {package_id} was assigned to Route with ID {route_id}"
