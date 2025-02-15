from skeleton.core.application_data import ApplicationData
from skeleton.commands.validation_helpers import validate_params_count
from base_command import BaseCommand

class RemoveTruckFromRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)
        self.params = params
        self._app_data = app_data
        

    def execute(self):
        validate_params_count(self.params, 2)
        truck_id, route_id = self.params

        truck = self.app_data.find_truck_by_id(truck_id)
        route = self._app_data.find_route_by_id(route_id)

        if truck.assigned_route != route:
                raise ValueError(f'The selected truck is not assigned to the specified route')
        
        truck.remove_from_route()

        self.logger.info(f"Truck with ID {truck_id} has been removed from Route {route_id}, truck status changed to free. | Executed by: username")

        return f"Truck with ID {truck_id} has been removed from Route {route_id}, truck status changed to free."

