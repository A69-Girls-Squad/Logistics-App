from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, try_parse_int
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class ShowRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self):
        route_id = try_parse_int(self._params[0])
        route = self._app_data.find_route_by_id(route_id)
        if not route:
            raise ApplicationError("No route found!")
        return str(route)