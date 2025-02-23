from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData

class CreateRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        super().__init__(params, app_data)


    def execute(self):
        locations, departure_time = self._params


        route = self._app_data.create_route(locations, departure_time)
        
        self.logger.info(f"Route with ID {route.id} was created!"
                         f"\nLocations: {locations}\n"
                         f"\nDeparture Time: {departure_time.isoformat(sep=" ", timespec="minutes")}"
                         f"\nExecuted by: username")
        self.logger.info(f"Route with ID {id} was created!"
                         f"\nLocations: {locations}"
                         f"\nDeparture Time: {departure_time.isoformat(sep=" ", timespec="minutes")} "
                         f"| Executed by: {self.app_data.logged_in_employee}")

        return (f'Route with id {route.id} was created!\nLocations: {locations}'
                f'\nDeparture Time: {departure_time.isoformat(sep=" ", timespec="minutes")}')