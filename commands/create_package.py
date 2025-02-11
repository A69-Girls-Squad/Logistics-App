from application_data import ApplicationData
from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count, try_parse_float


class CreatePackageCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        super().validate_params_count(params, 4) # choose validate from here or from the validation_helper?
        super().__init__(params, app_data)

    def execute(self):
        start_location, end_location, weight_float, customer_email = self._params
        weight = try_parse_float(weight_float) #?

        # if self._app_data.package_exists(package_id):
        #     raise ValueError(
        #         f'Package with ID {package_id} already exists!')
        #
        # self._app_data.create_package(start_location, end_location, weight, customer_email)
        #
        # def _requires_login(self) -> bool:
        #     return True
        #
        # def _expected_params_count(self) -> int:
        #     return 1
