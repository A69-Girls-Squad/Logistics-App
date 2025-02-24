import logging
from core.application_data import ApplicationData

class BaseCommand:
    """
    Base class for all commands in the application.

    This class provides common functionality for commands, such as parameter handling,
    logging, and validation for login requirements. It also defines constants for
    formatting output.

    Attributes:
        ROW_SEP_SHORT (str): A separator for short rows in output.
        ROW_SEP_LONG (str): A separator for long rows in output.
        TABLE_SEP (str): A separator for table formatting in output.
        _params (list): The command parameters.
        _app_data (ApplicationData): The shared application data.
        _requires_login (bool): Indicates whether the command requires a logged-in user.
        _logged_employee: The currently logged-in employee.
        logger (logging.Logger): The logger instance for the command.
    """

    TABLE_SEP = "-" * 16 + "|" + "-" * 43
    ROW_SEP = "\n" + "=" * 40

    def __init__(self, params, app_data: ApplicationData):
        """
         Initializes the BaseCommand with parameters and application data.

         Args:
             params (list): The command parameters.
             app_data (ApplicationData): The shared application data.
         """
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
        raise NotImplementedError("Execute method has to be overridden" + self.ROW_SEP)
        """
        Executes the command. This method must be overridden by subclasses.

        Returns:
            str: The result of the command execution.

        Raises:
            NotImplementedError: If the method is not overridden by a subclass.
        """
        raise NotImplementedError("Execute method has to be overridden" + self.ROW_SEP_SHORT)

    def requires_login(self) -> str:
        """
        Validates whether the command requires a logged-in user.

        Returns:
            str: An empty string if validation passes.

        Raises:
            ValueError: If the command requires a logged-in user but no user is logged in.
        """
        if self._requires_login and not self._app_data.has_logged_in_employee:
            self.logger.warning("Unauthorized access attempt detected.")
            raise ValueError("You are not logged in! Please login first!" + self.ROW_SEP)
        return ""

    def _throw_if_employee_logged_in(self):
        """
        Validates whether an employee is already logged in.

        Raises:
            ValueError: If an employee is already logged in.
        """
        if self._app_data.has_logged_in_employee:
            logged_employee = self._app_data.logged_in_employee
            self.logger.error(f"Attempt to log in while employee {logged_employee.username} is already logged in.")
            raise ValueError(
                f"Employee {logged_employee.username} is logged in! Please log out first!" + self.ROW_SEP*2
            )