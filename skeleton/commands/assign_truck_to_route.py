from commands.validation_helpers import try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class AssignTruckToRouteCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        super().execute()

        truck_id = try_parse_int(self.params[0])
        route_id = try_parse_int(self.params[1])
        
        self.app_data.assign_truck_to_route(truck_id, route_id)

        self.logger.info(
            f"Truck with ID {truck_id} assigned to Route with ID {route_id} "
            f"| Executed by: {self.app_data.logged_in_employee}"
            )

        return f"Truck with ID {truck_id} assigned to Route with ID {route_id}"

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 2
