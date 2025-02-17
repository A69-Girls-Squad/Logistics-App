from skeleton.commands.base_command import BaseCommand
from skeleton.commands.validation_helpers import validate_params_count
from skeleton.core.application_data import ApplicationData


class CreateRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 3)
        super().__init__(app_data)
        self._params = params

    def execute(self):
        locations, departure_time = self._params
        route = self._app_data.create_route(locations, departure_time)
        
        self.logger.info(f"Route with id {route.id} was created!\n"
                         f"Locations: {locations}\n"
                         f"Departure Time: {departure_time} | Executed by: username")
        
        return f'Route with id {route.id} was created!\nLocations: {locations}\nDeparture Time: {departure_time}'