from skeleton.commands.base_command import BaseCommand
from skeleton.commands.validation_helpers import validate_params_count
from skeleton.core.application_data import ApplicationData
from skeleton.models.route import Route


class SearchRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        super().__init__(app_data)
        self._params = params

    def execute(self):
        suitable_routes = []
        package_id = self._params[0]
        package = self._app_data.find_package_by_id(package_id)
        for route in self._app_data.routes:
            if route.status == Route.STATUS_CREATED and route.free_capacity > package.weight:
                locations = route.locations
                if package.start_location in locations and package.end_location in locations:
                    if locations.index(package.start_location) < locations.index(package.end_location):
                        suitable_routes.append(str(route))
        return f"Suitable Routes:\n"+"\n".join(suitable_routes)