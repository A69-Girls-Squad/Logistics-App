import logging
from core.application_data import ApplicationData


class BaseCommand:
    def __init__(self, params, app_data: ApplicationData):
        self._params = params
        self._app_data = app_data
        self._requires_login = True
        self._logged_employee = self._app_data.logged_in_employee

        self.logger = logging.getLogger(self.__class__.__name__)

        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(message)s",
            datefmt="%d:%m:%Y %H:%M",
            level=logging.INFO
        )

        # log to file instead of console

    @property
    def params(self):
        return tuple(self._params)

    @property
    def app_data(self):
        return self._app_data

    def execute(self) -> str:
        raise NotImplementedError("Execute method has to be overridden")

    def requires_login(self):
        if self._requires_login and not self._app_data.has_logged_in_employee:
            raise ValueError("You are not logged in! Please login first!")
        return ""

    def _throw_if_employee_logged_in(self):
        if self._app_data.has_logged_in_employee:
            logged_employee = self._app_data.logged_in_employee
            raise ValueError(
                f"Employee {logged_employee.username} is logged in! Please log out first!")
