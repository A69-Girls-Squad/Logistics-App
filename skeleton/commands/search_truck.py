from errors.application_error import ApplicationError
from commands.validation_helpers import try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class SearchTruckCommand(BaseCommand):
    """
     A command to search for available trucks based on their status, capacity, and maximum range.

     This command takes a route ID as a parameter, searches for trucks that are suitable
     for the specified route, and returns a formatted list of available trucks grouped by
     their type (Scania, Man, Actros). Each group includes the truck IDs, capacity, and
     maximum range.

     Attributes:
         params (list): A list of parameters passed to the command. The first parameter
                        should be the route ID.
         app_data (ApplicationData): The application data object containing the state
                                     of the application.

     Constants:
         SCANIA_NAME (str): Name of the Scania truck type.
         MAN_NAME (str): Name of the Man truck type.
         ACTROS_NAME (str): Name of the Actros truck type.
         SCANIA_CAPACITY (int): Capacity of Scania trucks.
         MAN_CAPACITY (int): Capacity of Man trucks.
         ACTROS_CAPACITY (int): Capacity of Actros trucks.
         SCANIA_MAX_RANGE (int): Maximum range of Scania trucks.
         MAN_MAX_RANGE (int): Maximum range of Man trucks.
         ACTROS_MAX_RANGE (int): Maximum range of Actros trucks.

     Methods:
         execute(): Executes the command to search for suitable trucks and returns a
                    formatted string with the results.
         _requires_login(): Specifies that the command requires the user to be logged in.
         _expected_params_count(): Specifies the expected number of parameters (1).

     Raises:
         ApplicationError: If no route is found with the provided ID.
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

        scania_ids = []
        man_ids = []
        actros_ids = []

        route_id = try_parse_int(self._params[0])
        route = self.app_data.find_route_by_id(route_id)
        if not route:
            raise ApplicationError("No Route found!" + BaseCommand.ROW_SEP)

        for truck in self.app_data.trucks:
            if truck.is_suitable(route):
                if truck.name == self.SCANIA_NAME:
                    scania_ids.append(truck.id)
                elif truck.name == self.MAN_NAME:
                    man_ids.append(truck.id)
                elif truck.name == self.ACTROS_NAME:
                    actros_ids.append(truck.id)

        if not (scania_ids or man_ids or actros_ids):
            return "No available Truck found" + BaseCommand.ROW_SEP

        return (f"AVAILABLE SCANIA TRUCKS:\n{BaseCommand.TABLE_SEP}"
                f"\nIDs:            | {", ".join(map(str, scania_ids))}\n{BaseCommand.TABLE_SEP}"
                f"\nCapacity:       | {self.SCANIA_CAPACITY}\n{BaseCommand.TABLE_SEP}"
                f"\nMax Range:      | {self.SCANIA_MAX_RANGE}\n{BaseCommand.TABLE_SEP}"
                f"{self.ROW_SEP}"
              
                f"\nAVAILABLE MAN TRUCKS:\n{BaseCommand.TABLE_SEP}"
                f"\nIDs:            | {", ".join(map(str, man_ids))}\n{BaseCommand.TABLE_SEP}"
                f"\nCapacity:       | {self.MAN_CAPACITY}\n{BaseCommand.TABLE_SEP}"
                f"\nMax Range:      | {self.MAN_MAX_RANGE}\n{BaseCommand.TABLE_SEP}"
                f"{self.ROW_SEP}"
                
                f"\nAVAILABLE ACTROS TRUCKS:\n{BaseCommand.TABLE_SEP}"
                f"\nIDs:            | {", ".join(map(str, actros_ids))}\n{BaseCommand.TABLE_SEP}"
                f"\nCapacity:       | {self.ACTROS_CAPACITY}\n{BaseCommand.TABLE_SEP}"
                f"\nMax Range:      | {self.ACTROS_MAX_RANGE}\n{BaseCommand.TABLE_SEP}"
               )

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 1