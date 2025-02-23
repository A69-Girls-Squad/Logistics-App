from commands.base_command import BaseCommand
from core.application_data import ApplicationData
from commands.validation_helpers import validate_params_count
from errors.application_error import ApplicationError


class RemoveTruckFromRouteCommand(BaseCommand):
    """
    Removes a truck from a route.
    Truck status is changed back to free.
    
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self):
        validate_params_count(self.params, 2)
        truck_id, route_id = self.params

        truck = self.app_data.find_truck_by_id(truck_id)
        if not truck:
            raise ApplicationError("No truck found!")

        route = self._app_data.find_route_by_id(route_id)
        if not route:
            raise ApplicationError("No route found!")

        if truck.assigned_route != route:
                raise ApplicationError(f"The selected truck is not assigned to the specified route")
        
        truck.remove_from_route()

        self.logger.info(
             f"Truck with ID {truck_id} has been removed from Route {route_id}, "
             f"truck status changed to free. | Executed by: {self.app_data.logged_in_employee}")

        return f"Truck with ID {truck_id} has been removed from Route {route_id}, truck status changed to free."

