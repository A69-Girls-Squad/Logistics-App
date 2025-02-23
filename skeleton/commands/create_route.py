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
                         f"\nLocations: {route.locations}\n"
                         f"\nDeparture Time: {route.departure_time.isoformat(sep=" ", timespec="minutes")}"
                         f"\nExecuted by: username" + self.ROW_SEP)
        self.logger.info(f"Route with ID {id} was created!"
                         f"\nLocations: {route.locations}"
                         f"\nDeparture Time: {route.departure_time.isoformat(sep=" ", timespec="minutes")} "
                         f"| Executed by: {self.app_data.logged_in_employee}" + self.ROW_SEP)

        return (f"Route with ID {route.id} was created!"
                f"\n{self.TABLE_SEP}"
                f"\nLocations:      | {locations}"
                f"\n{self.TABLE_SEP}"
                f"\nDeparture Time: | {route.departure_time.isoformat(sep=" ", timespec="minutes")}"
                f"\n{self.TABLE_SEP}") + self.ROW_SEP*2