import logging
from core.application_data import ApplicationData
from commands.validation_helpers import validate_params_count
from base_command import BaseCommand

logger = logging.getLogger(__name__)
class AssignTruckToRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)
        self.params = params
        self._app_data = app_data
        

    def execute(self):
        validate_params_count(self.params, 2)
        truck_id, route_id = self.params
        
        truck = self.app_data.find_truck_by_id(truck_id)
        route = self._app_data.find_route_by_id(route_id)
        
        if not truck.is_free():
            raise ValueError(f'The selected truck is not free')
    
        if route.load > truck.capacity:
            raise ValueError(f'Not enough capacity')
    
        if route.distance > truck.max_range:
            raise ValueError(f'Truck range exceeded.')
        
        route.assign_truck(truck)
        truck.assign_to_route(route)
        
        logger.info(f"Truck with id {truck_id} assigned to route {route_id}")
        return f"Truck with id {truck_id} assigned to route {route_id}"
        

