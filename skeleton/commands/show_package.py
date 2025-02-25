from errors.application_error import ApplicationError
from commands.validation_helpers import try_parse_int
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class ShowPackageCommand(BaseCommand):
    """
    Command to display details of a specific package.

    This command validates the input parameter, retrieves the package by its ID,
    and returns its string representation.
    """

    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to display details of a specific package.

        Returns:
            str: The string representation of the package.

        Raises:
            ApplicationError: If no package is found with the provided ID.
        """
        super().execute()

        package_id = try_parse_int(self._params[0])
        package = self._app_data.find_package_by_id(package_id)
        if not package:
            raise ApplicationError("No Package found!")
        return str(package)

    def _requires_login(self) -> bool:
        return True

    def _expected_params_count(self) -> int:
        return 1