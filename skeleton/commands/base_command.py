import logging
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class BaseCommand:
    """
    Base class for all commands in the application.

    This class provides common functionality for commands, such as parameter handling,
    logging, and validation for login requirements. It also defines constants for
    formatting output.

    Attributes:
        ROW_SEP (str): A separator for rows in output.
        TABLE_SEP (str): A separator for table formatting in output.
        _params (list): The command parameters.
        _app_data (ApplicationData): The shared application data.
        logger (logging.Logger): The logger instance for the command.
    """

    TABLE_SEP = "-" * 16 + "|" + "-" * 43
    ROW_SEP = "\n" + "=" * 60

    def __init__(self, params: list[str], app_data: ApplicationData):
        self._params = params
        self._app_data = app_data

        logging.basicConfig(
            filename="application.log",  # Log file name
            filemode="a",  # Append mode; use "w" to overwrite on each run
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%d:%m:%Y %H:%M",
            level=logging.INFO
        )

        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def params(self) -> tuple:
        """
        Gets the command parameters as a list.

        Returns:
            tuple: The command parameters.
        """
        return tuple(self._params)

    @property
    def app_data(self) -> ApplicationData:
        """
        Gets the shared application data.

        Returns:
            ApplicationData: The shared application data.
        """
        return self._app_data

    def execute(self) -> str:
        """
        Execute the command.

        This method checks if the command requires a logged-in user and validates
        the number of parameters. If any validation fails, an appropriate exception
        is raised.

        Returns:
            str: An empty string if the command executes successfully.

        Raises:
            ValueError: If the user is not logged in when required.
            ApplicationError: If the number of parameters is invalid.
        """
        if self._requires_login() and not self._app_data.has_logged_in_employee:
            self.logger.warning("Unauthorized access attempt detected.")
            raise ValueError("You are not logged in! Please login first!" + BaseCommand.ROW_SEP)

        expected_count = self._expected_params_count()
        if len(self._params) != expected_count:
            raise ApplicationError(
                f"Invalid number of arguments. Expected: {expected_count} / Received: {len(self._params)}."
            )

        return ""

    def _requires_login(self) -> bool:
        """
        Indicate whether the command requires a logged-in user.

        This method should be overridden in derived classes to specify if the command
        requires a logged-in user.

        Returns:
            bool: True if the command requires a logged-in user; otherwise, False.

        Raises:
            NotImplementedError: If the method is not overridden in a derived class.
        """
        raise NotImplementedError('Override in derived class')

    def _expected_params_count(self) -> int:
        """
        Return the expected number of parameters for the command.

        This method should be overridden in derived classes to specify the expected
        number of parameters.

        Returns:
            int: The expected number of parameters.

        Raises:
            NotImplementedError: If the method is not overridden in a derived class.
        """
        raise NotImplementedError('Override in derived class')

    def _throw_if_employee_logged_in(self):
        """
        Validates whether an employee is already logged in.

        Raises:
            ValueError: If an employee is already logged in.
        """
        if self._app_data.has_logged_in_employee:
            logged_employee = self._app_data.logged_in_employee
            self.logger.error(f"Attempt to log in while Employee {logged_employee.username} is already logged in.")
            raise ValueError(
                f"Employee {logged_employee.username} is logged in! Please log out first!" + BaseCommand.ROW_SEP*2
            )