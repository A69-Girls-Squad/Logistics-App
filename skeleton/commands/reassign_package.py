from commands.assign_package_to_route import AssignPackageToRouteCommand
from commands.base_command import BaseCommand
from commands.unassign_package_from_route import UnassignPackageToRouteCommand
from commands.validation_helpers import validate_params_count, try_parse_int
from core.application_data import ApplicationData


class ReassignPackageCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 3)
        super().__init__(params, app_data)

    def execute(self):
        package_id = try_parse_int(self.params[0])
        unassign_from_route_id = try_parse_int(self.params[1])
        assign_to_route_id = try_parse_int(self.params[2])

