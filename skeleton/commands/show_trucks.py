from commands.validation_helpers import validate_params_count
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


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
        validate_params_count(params, 0)
        super().__init__(params, app_data)


    def execute(self) -> str:
        self.logger.info(f"{self.__class__.__name__} executed by user: {self._logged_employee}" + self.ROW_SEP)

        scania_trucks = {}
        man_trucks = {}
        actros_trucks = {}

        def truck_status(value):
            if truck.assigned_route_id:
                return f"Busy (Route ID: {truck.assigned_route_id})"
            return "Free"

        for truck in self.app_data.trucks:
            if truck.name == self.SCANIA_NAME:
                scania_trucks[truck.id] = truck_status(truck)
            elif truck.name == self.MAN_NAME:
                man_trucks[truck.id] = truck_status(truck)
            elif truck.name == self.ACTROS_NAME:
                actros_trucks[truck.id] = truck_status(truck)

        if not (scania_trucks or man_trucks or actros_trucks):
            return "No available truck found" + self.ROW_SEP

        return (f"AVAILABLE SCANIA TRUCKS:\n{self.TABLE_SEP}"
                f"\nIDs:            | {"\n                | ".join(f"{key}: {value}" 
                                                 for key, value in scania_trucks.items())}\n{self.TABLE_SEP}"
                f"\nCapacity:       | {self.SCANIA_CAPACITY}\n{self.TABLE_SEP}"
                f"\nMax Range:      | {self.SCANIA_MAX_RANGE}\n{self.TABLE_SEP}"
                f"{self.ROW_SEP}"

                f"\nAVAILABLE MAN TRUCKS:\n{self.TABLE_SEP}"
                f"\nIDs:            | {"\n                | ".join(f"{key}: {value}" 
                                                 for key, value in man_trucks.items())}\n{self.TABLE_SEP}"
                f"\nCapacity:       | {self.MAN_CAPACITY}\n{self.TABLE_SEP}"
                f"\nMax Range:      | {self.MAN_MAX_RANGE}\n{self.TABLE_SEP}"
                f"{self.ROW_SEP}"

                f"\nAVAILABLE ACTROS TRUCKS:\n{self.TABLE_SEP}"
                f"\nIDs:            | {"\n                | ".join(f"{key}: {value}" 
                                                 for key, value in actros_trucks.items())}\n{self.TABLE_SEP}"
                f"\nCapacity:       | {self.ACTROS_CAPACITY}\n{self.TABLE_SEP}"
                f"\nMax Range:      | {self.ACTROS_MAX_RANGE}\n{self.TABLE_SEP}"
                + self.ROW_SEP * 2)