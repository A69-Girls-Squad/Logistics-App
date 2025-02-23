from commands.base_command import BaseCommand
from commands.validation_helpers import validate_params_count
from core.application_data import ApplicationData
from errors.application_error import ApplicationError


class ShowPackageCommand(BaseCommand):
    """
    Command to display details of a specific package.

    This command validates the input parameter, retrieves the package by its ID,
    and returns its string representation.
    """

    def __init__(self, params, app_data: ApplicationData):
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (a single package ID).
            app_data: The shared application data.

        Raises:
            ValueError: If the number of parameters is invalid.
        """
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to display details of a specific package.

        Returns:
            str: The string representation of the package.

        Raises:
            ApplicationError: If no package is found with the provided ID.
        """
        package_id = self._params[0]
        package = self._app_data.find_package_by_id(package_id)
        if not package:
            raise ApplicationError("No package found!" + self.ROW_SEP_LONG)
        return str(package)