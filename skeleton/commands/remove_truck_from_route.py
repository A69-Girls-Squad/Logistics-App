from errors.application_error import ApplicationError
from commands.validation_helpers import try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class RemoveTruckFromRouteCommand(BaseCommand):
    """
    A command to remove a truck from a route and change its status back to 'free'.

    This command takes a truck ID as a parameter, finds the corresponding truck,
    and removes it from its assigned route. The truck's status is then updated to 'free'.

    Attributes:
        params (list): A list of parameters passed to the command. The first parameter
                       should be the truck ID.
        app_data (ApplicationData): The application data object containing the state
                                    of the application.

    Methods:
        execute(): Executes the command to remove the truck from the route and updates
                    its status. Returns a success message.
        _requires_login(): Specifies that the command requires the user to be logged in.
        _expected_params_count(): Specifies the expected number of parameters (1).

    Raises:
        ApplicationError: If no truck is found with the provided ID.
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        super().execute()
        truck_id = try_parse_int(self.params[0])

        truck = self.app_data.find_truck_by_id(truck_id)

        if not truck:
            raise ApplicationError("No Truck found!" + BaseCommand.ROW_SEP)

        route_id = truck.assigned_route_id

        if route_id is None:
            raise ApplicationError("Truck is not assigned to any route!" + BaseCommand.ROW_SEP)

        self.app_data.unassign_truck_from_route(truck.id)

        self.logger.info(f"Truck with ID {truck_id} has been removed from Route with ID {route_id}, "
                         f"Truck status changed to \"free\". | "
                         f"Executed by: {self.app_data.logged_in_employee.username}" + BaseCommand.ROW_SEP)

        return (f"Truck with ID {truck_id} has been removed from Route ID {route_id}, "
                f"Truck status changed to \"free\".")

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 1