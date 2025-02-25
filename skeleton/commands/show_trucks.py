from commands.base_command import BaseCommand
from core.application_data import ApplicationData
from models.truck import Truck


class ShowTrucksCommand(BaseCommand):
    """
    Returns all trucks with the given status.
    Status can be free, busy or all.
    
    """
    SCANIA_NAME = "Scania"
    MAN_NAME = "Man"
    ACTROS_NAME = "Actros"

    SCANIA_CAPACITY = 42000
    MAN_CAPACITY = 37000
    ACTROS_CAPACITY = 26000

    SCANIA_MAX_RANGE = 8000
    MAN_MAX_RANGE = 10000
    ACTROS_MAX_RANGE = 13000

    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)


    def execute(self) -> str:
        super().execute()

        self.logger.info(f"{self.__class__.__name__} executed by user: {self.app_data.logged_in_employee}" + BaseCommand.ROW_SEP)

        scania_trucks = {}
        man_trucks = {}
        actros_trucks = {}

        def truck_status(value):
            if truck.assigned_route_id:
                return f"{Truck.STATUS_BUSY} (Route ID: {truck.assigned_route_id})"
            return f"{Truck.STATUS_FREE}"

        for truck in self.app_data.trucks:
            if truck.name == self.SCANIA_NAME:
                scania_trucks[truck.id] = truck_status(truck)
            elif truck.name == self.MAN_NAME:
                man_trucks[truck.id] = truck_status(truck)
            elif truck.name == self.ACTROS_NAME:
                actros_trucks[truck.id] = truck_status(truck)

        if not (scania_trucks or man_trucks or actros_trucks):
            return "No available Truck found" + self.ROW_SEP

        return (f"AVAILABLE SCANIA TRUCKS:\n{BaseCommand.TABLE_SEP}"
                f"\nIDs:            | {"\n                | ".join(f"{key}: {value}" 
                                                 for key, value in scania_trucks.items())}\n{BaseCommand.TABLE_SEP}"
                f"\nCapacity:       | {self.SCANIA_CAPACITY}\n{BaseCommand.TABLE_SEP}"
                f"\nMax Range:      | {self.SCANIA_MAX_RANGE}\n{BaseCommand.TABLE_SEP}"
                f"{BaseCommand.ROW_SEP}"

                f"\nAVAILABLE MAN TRUCKS:\n{BaseCommand.TABLE_SEP}"
                f"\nIDs:            | {"\n                | ".join(f"{key}: {value}" 
                                                 for key, value in man_trucks.items())}\n{BaseCommand.TABLE_SEP}"
                f"\nCapacity:       | {self.MAN_CAPACITY}\n{BaseCommand.TABLE_SEP}"
                f"\nMax Range:      | {self.MAN_MAX_RANGE}\n{BaseCommand.TABLE_SEP}"
                f"{BaseCommand.ROW_SEP}"

                f"\nAVAILABLE ACTROS TRUCKS:\n{BaseCommand.TABLE_SEP}"
                f"\nIDs:            | {"\n                | ".join(f"{key}: {value}" 
                                                 for key, value in actros_trucks.items())}\n{BaseCommand.TABLE_SEP}"
                f"\nCapacity:       | {self.ACTROS_CAPACITY}\n{BaseCommand.TABLE_SEP}"
                f"\nMax Range:      | {self.ACTROS_MAX_RANGE}\n{BaseCommand.TABLE_SEP}"
               )

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 0