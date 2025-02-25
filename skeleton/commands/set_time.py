from datetime import datetime
from core.application_time import ApplicationTime
from commands.base_command import BaseCommand
from core.application_data import ApplicationData


class SetTimeCommand(BaseCommand):
    """
    Command to set the current application time.

    This command validates the input parameter, sets the application time, and returns a confirmation message.
    """
    def __init__(self, params, app_data: ApplicationData):
        super().__init__(params, app_data)

    def execute(self) -> str:
        """
        Executes the command to set the current application time.

        Returns:
            str: A confirmation message indicating the new application time.

        Raises:
            ValueError: If the provided datetime string is invalid or not in ISO format.
        """
        super().execute()

        chosen_time = datetime.fromisoformat(self.params[0])
        ApplicationTime.set_current(chosen_time)

        return f"Current application time set to: {chosen_time.strftime("%Y-%m-%d %H:%M")}"

    def _requires_login(self) -> bool:
        return False

    def _expected_params_count(self) -> int:
        return 1