from skeleton.core.application_data import ApplicationData
from skeleton.commands.base_command import BaseCommand
from skeleton.commands.validation_helpers import validate_params_count, try_parse_float


class CreatePackageCommand(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        validate_params_count(params, 4)
        super().__init__(params, app_data)

    def execute(self):
        '''
        Assigns available truck to a route.
        param: start_location: str
        param: end_location: str
        param: weight: float
        param: customer_email: str
        return: str

        '''
        start_location, end_location, weight_float, customer_email = self._params
        weight = try_parse_float(weight_float)

        package = self._app_data.create_package(start_location, end_location, weight, customer_email)

        self.logger.info(f'Package with ID {package.id} created')
        return f'Package with ID {package.id} was created!'
