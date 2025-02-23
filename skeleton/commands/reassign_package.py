from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, try_parse_int
from core.application_data import ApplicationData


class ReassignPackageCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 3)
        super().__init__(params, app_data)

    def execute(self):
        package_id = try_parse_int(self.params[0])
        unassign_from_route_id = str(self.params[1])
        assign_to_route_id = str(self.params[2])

        self.app_data.unassign_package_from_route(package_id, unassign_from_route_id)

        self.app_data.assign_package_to_route(package_id, assign_to_route_id)

        return (f"Package with ID {package_id} was unassigned from Route with ID {unassign_from_route_id}"
                f"and was assigned to Route with ID {assign_to_route_id}")
