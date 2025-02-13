import application_data
from application_data import ApplicationData
from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count


class ShowPackagesCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 4)
        super().__init__(params, app_data)

    def execute(self):

        package = self.app_data.find_package_by_id(application_data.Package.id)
        return str(package)


