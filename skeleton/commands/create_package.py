from core.application_data import ApplicationData
from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, try_parse_float


class CreatePackageCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 4)
        super().__init__(params, app_data)


    def execute(self):

        start_location, end_location, weight_float, customer_email = self._params
        weight = try_parse_float(weight_float)

        package = self.app_data.create_package(start_location, end_location, weight, customer_email)

        self.logger.info(f"Package with ID {package.id} created | Executed by: {self.app_data.logged_in_employee}")
        return f"Package with ID {package.id} was created!"
        self.logger.info(f"Package with ID {package.id} created" + self.ROW_SEP_SHORT)
        return f"Package with ID {package.id} was created!" + self.ROW_SEP_SHORT
