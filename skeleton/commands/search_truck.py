from commands.validation_helpers import validate_params_count, try_parse_int
from commands.base_command import BaseCommand
from errors.application_error import ApplicationError
from core.application_data import ApplicationData

class SearchTruckCommand(BaseCommand):
    """
    Searches for available trucks based on truck status,
    truck capacity and truck max range.
    
    """
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self):
        self.logger.info(f"{self.__class__.__name__} executed by user: {self._logged_employee}")

        suitable_trucks = []
        route_id = try_parse_int(self._params[0])
        route = self.app_data.find_route_by_id(route_id)
        if not route:
            raise ApplicationError("No route found!")

        for truck in self.app_data.trucks:
            if truck.is_suitable(route):
                suitable_trucks.append(truck)

        if not suitable_trucks:
            return "No available truck found"

        return "\n".join([str(truck) for truck in suitable_trucks])
        