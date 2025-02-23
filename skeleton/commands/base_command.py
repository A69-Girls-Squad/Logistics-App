import logging
from core.application_data import ApplicationData

class BaseCommand:
    ROW_SEP_SHORT = "\n" + "=" * 60
    ROW_SEP_LONG = "\n" + "=" * 40
    TABLE_SEP = "-" * 16 + "|" + "-" * 43

    def __init__(self, params, app_data: ApplicationData):
        self._params = params
        self._app_data = app_data
        self._requires_login = True
        self._logged_employee = self._app_data.logged_in_employee


        logging.basicConfig(
            filename="application.log",  # Log file name
            filemode="a",  # Append mode; use "w" to overwrite on each run
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%d:%m:%Y %H:%M",
            level=logging.INFO
        )

        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def params(self):
        return tuple(self._params)

    @property
    def app_data(self):
        return self._app_data

    def execute(self) -> str:
        raise NotImplementedError("Execute method has to be overridden" + self.ROW_SEP_SHORT)

    def requires_login(self):
        if self._requires_login and not self._app_data.has_logged_in_employee:
            self.logger.warning("Unauthorized access attempt detected.")
            raise ValueError("You are not logged in! Please login first!" + self.ROW_SEP_SHORT)
        return ""

    def _throw_if_employee_logged_in(self):
        if self._app_data.has_logged_in_employee:
            logged_employee = self._app_data.logged_in_employee
            self.logger.error(f"Attempt to log in while employee {logged_employee.username} is already logged in.")
            raise ValueError(
                f"Employee {logged_employee.username} is logged in! Please log out first!" + self.ROW_SEP_SHORT
            )