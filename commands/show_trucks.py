import logging
from core.application_data import ApplicationData
from commands.validation_helpers import validate_params_count
from base_command import BaseCommand
from models.all_trucks import AllTrucks
from models.truck import Truck

logger = logging.getLogger(__name__)

class ShowTrucksCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)
        validate_params_count(params, 1)

    def show_trucks(self, status=None):
        all_trucks = AllTrucks()
        trucks = all_trucks.get_all_trucks()

        if status:
            trucks = [truck for truck in trucks if truck.status == status]

        if not trucks:
            print(f"No trucks available with status: {status if status else 'All'}")
            logger.info(f"No trucks available with status: {status if status else 'All'}")
            return
        
        print(f"\nAll Trucks Information ({status if status else 'All'}):")
        print("=" * 40)
        for truck in trucks:
            print(truck) 
            print("-" * 40)
            logger.info(f"Truck info: {truck.name} (ID: {truck.id}, Status: {truck.status})")

    def execute(self):
        status_param = self.params[0].lower()

        if status_param == "free":
            status = Truck.STATUS_FREE
        elif status_param == "busy":
            status = Truck.STATUS_BUSY
        elif status_param == "all":
            status = None
        else:
            raise ValueError('Invalid status. Enter "all", "free", or "busy".')

        self.show_trucks(status=status)

        logger.info(f"Executed ShowTrucksCommand for all trucks with status: {status if status else 'All'}")

        return f"Displayed trucks with status: {status if status else 'All'}"