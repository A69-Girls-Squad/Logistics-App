from commands.validation_helpers import validate_params_count
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class CreateRouteCommand(BaseCommand):
    """
    Command to create a new route in the application.

    This command validates the input parameters, creates a route, and logs the action.
    """
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 2)
        super().__init__(params, app_data)


    def execute(self) -> str:
        """
        Executes the command to create a new route.

        Returns:
            str: A formatted string containing the details of the created route.

        Notes:
            - The `locations` parameter should be a string of locations separated by commas.
            - The `departure_time` parameter should be a string in ISO format.
        """
        locations, departure_time = self._params


        route = self._app_data.create_route(locations, departure_time)
        
        self.logger.info(f"Route with ID {route.id} was created!"
                         f"\nLocations: {route.locations}\n"
                         f"\nDeparture Time: {route.departure_time.isoformat(sep=" ", timespec="minutes")}"
                         f"\nExecuted by: username" + BaseCommand.ROW_SEP)
        self.logger.info(f"Route with ID {id} was created!"
                         f"\nLocations: {route.locations}"
                         f"\nDeparture Time: {route.departure_time.isoformat(sep=" ", timespec="minutes")} "
                         f"| Executed by: {self.app_data.logged_in_employee}" + BaseCommand.ROW_SEP)

        return (f"Route with ID {route.id} was created!"
                f"\n{BaseCommand.TABLE_SEP}"
                f"\nLocations:      | {locations}"
                f"\n{BaseCommand.TABLE_SEP}"
                f"\nDeparture Time: | {route.departure_time.isoformat(sep=" ", timespec="minutes")}"
                f"\n{BaseCommand.TABLE_SEP}") + BaseCommand.ROW_SEP*2