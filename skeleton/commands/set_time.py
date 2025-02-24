from datetime import datetime
from core.application_time import ApplicationTime
from commands.validation_helpers import validate_params_count
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class SetTimeCommand(BaseCommand):
    """
    Command to set the current application time.

    This command validates the input parameter, sets the application time, and returns a confirmation message.
    """
    def __init__(self, params, app_data: ApplicationData):
        """
        Initializes the command with parameters and application data.

        Args:
            params: The command parameters (a single ISO-formatted datetime string).
            app_data: The shared application data.

        Raises:
            ValueError: If the number of parameters is invalid.
        """
        validate_params_count(params, 1)
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to set the current application time.

        Returns:
            str: A confirmation message indicating the new application time.

        Raises:
            ValueError: If the provided datetime string is invalid or not in ISO format.
        """
        chosen_time = datetime.fromisoformat(self.params[0])
        ApplicationTime.set_current(chosen_time)

        return f"Current application time set to: {chosen_time.strftime("%Y-%m-%dT%H:%M")}" + self.ROW_SEP*2
