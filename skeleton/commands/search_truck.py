from skeleton.commands.base_command import BaseCommand
from skeleton.models.package import Package
from skeleton.models.route import Route
from skeleton.models.all_trucks import AllTrucks
from skeleton.core.application_data import ApplicationData

class SearchTruckCommand(BaseCommand):
    """
    Searches for available trucks based on truck status,
    truck capacity and truck max range.
    
    """
    def __init__(self, params, app_data: ApplicationData, all_trucks:AllTrucks):
        super().__init__(params, app_data)
        self.all_trucks = all_trucks
        
    def execute(self, package: Package, route: Route):
        self.logger.info(f"{self.__class__.__name__} executed by user: {self._logged_employee}")
        for truck in self.all_trucks.get_all_trucks():
            if truck.is_free() and truck.capacity >= package.weight and truck.max_range >= route.distance:
                return truck
        return f"No available truck found"
        