from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData


class BulkAssignPackagesCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        super().__init__(app_data)
        self._params = params

    def execute(self):
        bulk_assigned_packages = []
        no_more_capacity_message = ""
        route_id = self._params[0]
        route = self._app_data.find_route_by_id(route_id)
        for package in self._app_data.not_assigned_packages:
            if package.weight < route.free_capacity:
                route.assign_package(package)
                bulk_assigned_packages.append(package.id)
            else:
                no_more_capacity_message = "No more free capacity. Operation terminated"
        return f"Bulk assigned packages to Route ID {route_id}: {bulk_assigned_packages}\n{no_more_capacity_message}"