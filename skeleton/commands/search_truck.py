from errors.application_error import ApplicationError
from commands.validation_helpers import validate_params_count, try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData

class SearchTruckCommand(BaseCommand):
    """
    Searches for available trucks based on truck status,
    truck capacity and truck max range.
    
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
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self) -> str:
        self.logger.info(f"{self.__class__.__name__} executed by user: {self._logged_employee}" + self.ROW_SEP)

        scania_ids = []
        man_ids = []
        actros_ids = []

        route_id = try_parse_int(self._params[0])
        route = self.app_data.find_route_by_id(route_id)
        if not route:
            raise ApplicationError("No route found!" + self.ROW_SEP)

        for truck in self.app_data.trucks:
            if truck.is_suitable(route):
                if truck.name == self.SCANIA_NAME:
                    scania_ids.append(truck.id)
                elif truck.name == self.MAN_NAME:
                    man_ids.append(truck.id)
                elif truck.name == self.ACTROS_NAME:
                    actros_ids.append(truck.id)

        if not (scania_ids or man_ids or actros_ids):
            return "No available truck found" + self.ROW_SEP

        return (f"AVAILABLE SCANIA TRUCKS:\n{self.TABLE_SEP}"
                f"\nIDs:            | {", ".join(map(str, scania_ids))}\n{self.TABLE_SEP}"
                f"\nCapacity:       | {self.SCANIA_CAPACITY}\n{self.TABLE_SEP}"
                f"\nMax Range:      | {self.SCANIA_MAX_RANGE}\n{self.TABLE_SEP}"
                f"{self.ROW_SEP}"
              
                f"\nAVAILABLE MAN TRUCKS:\n{self.TABLE_SEP}"
                f"\nIDs:            | {", ".join(map(str, man_ids))}\n{self.TABLE_SEP}"
                f"\nCapacity:       | {self.MAN_CAPACITY}\n{self.TABLE_SEP}"
                f"\nMax Range:      | {self.MAN_MAX_RANGE}\n{self.TABLE_SEP}"
                f"{self.ROW_SEP}"
                
                f"\nAVAILABLE ACTROS TRUCKS:\n{self.TABLE_SEP}"
                f"\nIDs:            | {", ".join(map(str, actros_ids))}\n{self.TABLE_SEP}"
                f"\nCapacity:       | {self.ACTROS_CAPACITY}\n{self.TABLE_SEP}"
                f"\nMax Range:      | {self.ACTROS_MAX_RANGE}\n{self.TABLE_SEP}"
                + self.ROW_SEP*2)
        