from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, validate_unknown_params_count, try_parse_int
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class BulkAssignPackagesCommand(BaseCommand):
    """
    Assigns multiple packages to a route.
    param: route: int
    return: str
    """
    def __init__(self, params, app_data: ApplicationData):
        validate_unknown_params_count(params, 2, 102)
        super().__init__(params, app_data)

    def execute(self):

        bulk_assigned_packages = []
        no_more_capacity_message = ""

        route_id, *packages_ids = self._params
        route_id = try_parse_int(route_id)

        route = self._app_data.find_route_by_id(route_id)
        if not route:
            raise ApplicationError(f"No route with ID {route_id}")

        truck = self._app_data.find_truck_by_id(route.assigned_truck_id)
        if not truck:
            raise ApplicationError(f"Route with ID {route_id} has no Truck assigned")

        free_capacity = truck.capacity - route.load
        for package_id in packages_ids:
            package_id = try_parse_int(package_id)
            package = self.app_data.find_package_by_id(package_id)
            if not package:
                raise ApplicationError(f"No package with ID {package_id}")

            if package.weight < free_capacity:
                self.app_data.assign_package_to_route(package_id, route_id)
                bulk_assigned_packages.append(package.id)
            else:
                no_more_capacity_message = "No more free capacity. Operation terminated"
        
        self.logger.info(f"Bulk assigned packages to Route ID {route_id}:"
                         f" {bulk_assigned_packages}\n{no_more_capacity_message}"
                         f" | Executed by: {self.app_data.logged_in_employee}")

        return f"Bulk assigned packages to Route ID {route_id}: {bulk_assigned_packages}\n{no_more_capacity_message}"