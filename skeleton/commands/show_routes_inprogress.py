from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from models.route import Route


class ShowRoutesInProgressCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        super().__init__(params, app_data)

    def execute(self):
        routes_in_progress = []
        for route in self._app_data.routes:
            if route.status == Route.STATUS_IN_PROGRESS:
                routes_in_progress.append(route)
        return f"Routs In Progress:\n"+"\n".join([str(route) for route in routes_in_progress])
