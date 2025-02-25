from errors.application_error import ApplicationError
from commands.validation_helpers import validate_params_count, try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class RemoveTruckFromRouteCommand(BaseCommand):
    """
    Removes a truck from a route.
    Truck status is changed back to free.
    
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        validate_params_count(self.params, 1)
        truck_id = try_parse_int(self.params[0])

        truck = self.app_data.find_truck_by_id(truck_id)
        route_id = truck.assigned_route_id

        if not truck:
            raise ApplicationError("No Truck found!" + BaseCommand.ROW_SEP)

        self.app_data.unassign_truck_from_route(truck.id)

        self.logger.info(f"Truck with ID {truck_id} has been removed from Route with ID {route_id}, "
                         f"Truck status changed to \"free\". | "
                         f"Executed by: {self.app_data.logged_in_employee.username}" + BaseCommand.ROW_SEP)

        return (f"Truck with ID {truck_id} has been removed from Route ID {route_id}, "
                f"Truck status changed to \"free\".")

