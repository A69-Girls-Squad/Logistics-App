from datetime import datetime
from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from core.application_time import ApplicationTime


class SetTimeCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self):
        chosen_time = datetime.fromisoformat(self.params[0])
        ApplicationTime.set_current(chosen_time)

        return f"Current application time set to: {chosen_time.strftime("%Y-%m-%dT%H:%M")}"
