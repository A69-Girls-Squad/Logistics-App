from skeleton.commands.base_command import BaseCommand
from skeleton.core.application_data import ApplicationData
from skeleton.commands.validation_helpers import validate_params_count
from skeleton.models.all_trucks import AllTrucks
from skeleton.models.truck import Truck

class ShowTrucksCommand(BaseCommand):
    """
    Returns all trucks with the given status.
    Status can be free, busy or all.
    
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)
        validate_params_count(params, 1)

    def show_trucks(self, status):
        all_trucks = AllTrucks()
        trucks = all_trucks.get_all_trucks()

        if status != "all":
            trucks = [truck for truck in trucks if truck.status == status]

        if not trucks:
            print(f"No trucks available with status: {status}")
            self.logger.info(f"No trucks available with status: {status}")
            return
        
        print(f"\nAll Trucks Information with status: {status}:")
        print("=" * 40)
        for truck in trucks:
            print(truck) 
            print("-" * 40)

    def execute(self):
        status_param = self.params[0].lower()

        if status_param == "free":
            status = Truck.STATUS_FREE
        elif status_param == "busy":
            status = Truck.STATUS_BUSY
        elif status_param == "all":
            status = "all"
        else:
            raise ValueError('Invalid status. Enter "all", "free", or "busy".')

        self.show_trucks(status=status)

        self.logger.info(f"Executed ShowTrucksCommand for all trucks with status: {status}")

        return f"Displaying trucks with status: {status}"