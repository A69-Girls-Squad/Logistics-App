from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class ShowPackageCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self):
        package_id = self._params[0]
        package = self._app_data.find_package_by_id(package_id)
        if not package:
            raise ApplicationError("No package found!" + self.ROW_SEP_LONG)
        return str(package)