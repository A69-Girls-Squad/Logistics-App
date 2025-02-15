from skeleton.commands.base_command import BaseCommand
from skeleton.commands.validation_helpers import validate_params_count
from skeleton.core.application_data import ApplicationData


class ShowRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        super().__init__(app_data)
        self._params = params

    def execute(self):
        route_id = self._params[0]
        route = self._app_data.find_route_by_id(route_id)
        return str(route)