import logging
from models.package import Package
from models.route import Route
from models.truck import Truck
from models.all_trucks import AllTrucks

logger = logging.getLogger(__name__)
class SearchTruckCommand:
    def __init__(self, all_trucks:AllTrucks):
        self.all_trucks = all_trucks
        
    def execute(self, package: Package, route: Route):
        self.logger.info(f'{self.__class__.__name__} executed by user: username')
        for truck in self.all_trucks.get_all_trucks():
            if truck.is_free() and truck.capacity >= package.weight and truck.max_range >= route.distance:
                return truck
            else:
                return f"No available truck found"
        