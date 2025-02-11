from application_data import ApplicationData
from commands.base_command import BaseCommand


class ShowPackages(BaseCommand):
    def __init__(self, params, app_data: ApplicationData):
        super().validate_params_count(params, 4)
        super().__init__(params, app_data)

    def execute(self):
        start_location, end_location, weight_float, customer_email = self._params


    # def _requires_login(self) -> bool:
    #     return True
    #
    # def _expected_params_count(self) -> int:
    #     return 1