from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, try_parse_int
from core.application_data import ApplicationData
from errors.application_error import ApplicationError
from models.route import Route


class SearchRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self):
        suitable_routes = []
        package_id = try_parse_int(self._params[0])
        package = self._app_data.find_package_by_id(package_id)
        if not package:
            raise ApplicationError("No package found!")
        for route in self._app_data.routes:

            sufficient_capacity = True
            if route.assigned_truck_id:
                truck = self._app_data.find_truck_by_id(route.assigned_truck_id)
                if not truck:
                    raise ApplicationError("No truck found!")
                free_capacity = truck.capacity - route.load
                if free_capacity < package.weight:
                    sufficient_capacity = False

            if route.status == Route.STATUS_CREATED and sufficient_capacity:
                locations = route.locations
                if package.start_location in locations and package.end_location in locations:
                    if locations.index(package.start_location) < locations.index(package.end_location):
                        route_details = (f"Route Details:"
                                         f"\nID: {route.id}"
                                         f"\nHubs:\n{" -> ".join(f"{key}: {value}" for key, value in route.stops.items())}"
                                         f"\nDeparture Time: {route.departure_time.isoformat(sep=" ", timespec="minutes")}"
                                         f"\n============")
                        suitable_routes.append(route_details)
        return f"Suitable Routes:\n"+"\n".join(suitable_routes)