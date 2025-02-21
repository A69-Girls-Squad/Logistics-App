from models.truck import Truck
from commands.base_command import BaseCommand
from core.application_data import ApplicationData
from commands.validation_helpers import validate_params_count, try_parse_int
from errors.application_error import ApplicationError

class AssignTruckToRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        """
        Assigns available truck to a route.

        """
        validate_params_count(self.params, 2)
        truck_id = try_parse_int(self.params[0])
        route_id = try_parse_int(self.params[1])
        
        self.app_data.assign_truck_to_route(truck_id, route_id)

        username = self._app_data.logged_in_employee

        self.logger.info(f"Truck with id {truck_id} assigned to route {route_id} | Executed by: {username} ")

        return f"Truck with id {truck_id} assigned to route {route_id}"

    
