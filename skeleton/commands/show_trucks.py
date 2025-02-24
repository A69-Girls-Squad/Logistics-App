from commands.validation_helpers import validate_params_count
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class ShowTrucksCommand(BaseCommand):
    """
    Returns all trucks with the given status.
    Status can be free, busy or all.
    
    """
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 0)
        super().__init__(params, app_data)


    def execute(self):
        #status_param = self.params[0].lower()
            pass




